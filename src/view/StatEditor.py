from typing import Optional, Any
from PyQt6.QtWidgets import QDialog, QWidget
from PyQt6.QtCore import QAbstractTableModel, Qt, QModelIndex
from src.model.Sheet import Sheet
from src.view import STAT_EDITOR_TABLE_HEADERS, STAT_EDITOR_HISTORY_TABLE_HEADERS
from src.view.Ui_StatEditor import Ui_StatEditor


class StatEditor(QDialog, Ui_StatEditor):

    def __init__(self, sheet: Sheet, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setupUi(self)

        self.stat_table_view.setModel(StatEditorTableModel(sheet, self))
        self.history_table_view.setModel(HistoryTableModel(sheet, self))


class StatEditorTableModel(QAbstractTableModel):

    def __init__(self, sheet: Sheet, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self.sheet: Sheet = sheet
        """Sheet model instance."""

    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        pass

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self.sheet.stat_list)

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

    def __init__(self, sheet: Sheet, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self.sheet: Sheet = sheet
        """Sheet model instance."""

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
