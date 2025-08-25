from typing import Optional, Any
from copy import deepcopy
from PyQt6.QtWidgets import QDialog, QWidget, QAbstractItemView, QMessageBox
from PyQt6.QtCore import QAbstractTableModel, Qt, QModelIndex, QVariant
from src.model.Sheet import Sheet
from src.model.Stat import Stat
from src.view import STAT_EDITOR_TABLE_HEADERS, STAT_EDITOR_HISTORY_TABLE_HEADERS
from src.view.Ui_StatEditor import Ui_StatEditor


class StatEditor(QDialog, Ui_StatEditor):

    def __init__(self, sheet: Sheet, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self.sheet: Sheet = deepcopy(sheet)
        """Sheet being edited."""
        self.changed_stats: list[str] = []
        """List of changed stat names."""
        self.changed_names: dict[str, str] = {}
        """Dict of old names, and the new names they have been set to"""
        self.history_table_model: HistoryTableModel
        """Model for the history table view."""

        self.setupUi(self)

        # Configure models
        self.stat_table_view.setModel(StatEditorTableModel(self))
        self.stat_table_view.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
            | QAbstractItemView.EditTrigger.DoubleClicked
        )
        self.history_table_model = HistoryTableModel(self)
        self.history_table_view.setModel(self.history_table_model)
        self.history_table_view.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
            | QAbstractItemView.EditTrigger.DoubleClicked
        )

        # Configure widget
        self.stat_table_view.selectionModel().currentChanged.connect(
            self.current_changed_slot
        )

    def current_changed_slot(self, current: QModelIndex, previous: QModelIndex) -> None:
        """
        Slot called when the selection changes in the stat table view.
        :param current: The current index
        :param previous: The previous index
        """
        self.history_table_model.set_new_stat(self.sheet.stat_list[current.row()])

    def edits_made(self) -> bool:
        """
        Checks if any edits have been made to the stats.
        :returns: True if edits have been made, False otherwise
        """
        return len(self.changed_stats) > 0


class StatEditorTableModel(QAbstractTableModel):

    def __init__(self, editor: StatEditor):
        super().__init__(editor)

        self.editor: StatEditor = editor
        """Reference to the editor this model belongs to."""

    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        return (
            Qt.ItemFlag.ItemIsEnabled
            | Qt.ItemFlag.ItemIsSelectable
            | Qt.ItemFlag.ItemIsEditable
        )

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if role == Qt.ItemDataRole.DisplayRole:
            stat: Stat = self.editor.sheet.stat_list[index.row()]
            if index.column() == 0:  # Name
                return stat.name
            if index.column() == 1:  # Value
                return stat.value
            if index.column() == 2:  # Max
                return stat.max
            if index.column() == 3:  # Min
                return stat.min

        return QVariant()

    def setData(self, index: QModelIndex, value: Any, role: int) -> bool:
        if role != Qt.ItemDataRole.EditRole:
            return False

        stat: Stat = self.editor.sheet.stat_list[index.row()]

        try:
            if index.column() == 0:  # Name
                # Ensure the name is not already in use
                if str(value) in [stat.name for stat in self.editor.sheet.stat_list]:
                    QMessageBox.critical(
                        self.editor,
                        "Error",
                        "Failed to rename stat, is the name already in use?",
                    )
                    return False

                # Update the name changed list
                name_updated_previously: bool = False
                for old_name, new_name in self.editor.changed_names.items():

                    if new_name == stat.name:
                        self.editor.changed_names[old_name] = str(value)
                        name_updated_previously = True
                        break

                if not name_updated_previously:
                    self.editor.changed_names[stat.name] = str(value)

                # Remove old name from the changed_stats, the new name will be added at the end of this function
                if stat.name in self.editor.changed_stats:
                    self.editor.changed_stats.remove(stat.name)

                # Rename the stat in the sheet model
                self.editor.sheet.rename_stat(stat.name, str(value))
                stat.name = str(value)

            elif index.column() == 1:  # Value
                # TODO If the stat has a history and is being directly edited, show a warning
                stat.value = int(value)

            elif index.column() == 2:  # Max
                stat.max = int(value)

            elif index.column() == 3:  # Min
                stat.min = int(value)

            else:
                return False
        except ValueError:
            return False

        if stat.name not in self.editor.changed_stats:
            self.editor.changed_stats.append(stat.name)
        self.dataChanged.emit(index, index, [Qt.ItemDataRole.DisplayRole])
        return True

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self.editor.sheet.stat_list)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(STAT_EDITOR_TABLE_HEADERS)

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        if (
            role == Qt.ItemDataRole.DisplayRole
            and orientation == Qt.Orientation.Horizontal
        ):
            return STAT_EDITOR_TABLE_HEADERS[section]


class HistoryTableModel(QAbstractTableModel):

    def __init__(self, editor: StatEditor, stat: Optional[Stat] = None):
        super().__init__(editor)

        self.stat: Optional[Stat] = stat
        """Reference to the stat this model belongs to."""

    def flags(self, index):
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable

    def data(self, index: QModelIndex, role: int) -> Any:
        if self.stat is None:
            return QVariant()
        if role == Qt.ItemDataRole.DisplayRole:
            description: str
            edit: str
            description, edit = self.stat.history[index.row()]

            if index.column() == 0:  # Description
                return description
            if index.column() == 1:  # Edit
                return edit

        return QVariant()

    def rowCount(self, parent=QModelIndex()) -> int:
        if not self.stat or not self.stat.history:
            return 0
        return len(self.stat.history)

    def columnCount(self, parent=QModelIndex()) -> int:
        return len(STAT_EDITOR_HISTORY_TABLE_HEADERS)

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ):
        if (
            role == Qt.ItemDataRole.DisplayRole
            and orientation == Qt.Orientation.Horizontal
        ):
            return STAT_EDITOR_HISTORY_TABLE_HEADERS[section]

    def set_new_stat(self, new_stat: Optional[Stat]) -> None:
        """
        Sets a new stat for this model.
        :param new_stat: New stat whose history needs to be provided
        """
        self.stat = new_stat
        self.layoutChanged.emit()
