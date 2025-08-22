from typing import Optional, Any
from PyQt6.QtWidgets import QDialog, QWidget, QAbstractItemView
from PyQt6.QtCore import QAbstractTableModel, Qt, QModelIndex, QVariant
from src.model.Sheet import Sheet
from src.model.Stat import Stat
from src.view import STAT_EDITOR_TABLE_HEADERS, STAT_EDITOR_HISTORY_TABLE_HEADERS
from src.view.Ui_StatEditor import Ui_StatEditor


class StatEditor(QDialog, Ui_StatEditor):

    def __init__(self, sheet: Sheet, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self.stat_list: list[Stat] = sheet.stat_list
        """List of stats."""
        self.changed_stats: list[str] = []
        """List of changed stat names."""

        self.setupUi(self)

        self.stat_table_view.setModel(StatEditorTableModel(self))
        self.stat_table_view.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
            | QAbstractItemView.EditTrigger.DoubleClicked
        )
        self.history_table_view.setModel(HistoryTableModel(self))
        self.history_table_view.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
            | QAbstractItemView.EditTrigger.DoubleClicked
        )

    def edits_made(self) -> bool:
        """
        Check if any edits have been made.
        :returns: True if edits have been made, False otherwise.
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
            stat: Stat = self.editor.stat_list[index.row()]
            if index.column() == 0:  # Name
                # TODO If the stat name is changed the stat configs in every card should be updated as well
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

        stat: Stat = self.editor.stat_list[index.row()]

        try:
            if index.column() == 0:  # Name
                stat.name = str(value)
            elif index.column() == 1:  # Value
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
        return len(self.editor.stat_list)

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

    def __init__(self, editor: StatEditor):
        super().__init__(editor)

        self.editor: StatEditor = editor
        """Reference to the editor this model belongs to."""

    def flags(self, index):
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable

    def rowCount(self, parent=QModelIndex()) -> int:
        return 0

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
