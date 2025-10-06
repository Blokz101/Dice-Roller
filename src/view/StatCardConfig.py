from typing import Optional, Any
from copy import deepcopy
from PyQt6.QtWidgets import QDialog, QWidget, QAbstractItemView
from PyQt6.QtCore import QAbstractTableModel, QAbstractListModel, QModelIndex, Qt, QVariant, QItemSelection
from src.view import CARD_CONFIG_STAT_TABLE_HEADERS
from src.view.Ui_StatCardConfig import Ui_StatCardConfig
from src.model.Sheet import Sheet
from src.model.Card import Card, StatConfig


class StatCardConfig(QDialog, Ui_StatCardConfig):

    def __init__(self, sheet: Sheet, card: Card, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self.sheet: Sheet = deepcopy(sheet)
        """Card being edited."""
        self.card: Card = card
        self.card_config_stat_model: CardConfigStatTableModel = CardConfigStatTableModel(self.card)
        """Model for the card stats table view."""
        self.stat_list_model: StatListModel = StatListModel([stat.name for stat in sheet.stat_list])
        """Model for the stat list view."""

        self.setupUi(self) # type: ignore

        self.card_config_stat_view.setModel(self.card_config_stat_model)
        self.stat_list_view.setModel(self.stat_list_model)

        self.stat_list_view.clicked.connect(self.stat_list_view_clicked_slot) # type: ignore
        self.order_up_button.clicked.connect(self.order_up_button_slot)  # type: ignore
        self.order_down_button.clicked.connect(self.order_down_button_slot)  # type: ignore
        self.delete_button.clicked.connect(self.delete_button_slot)  # type: ignore

        # Configure widgets
        self.card_config_stat_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

    def order_up_button_slot(self) -> None:
        """Called when the order up button is clicked."""

    def order_down_button_slot(self) -> None:
        """Called when the order down button is clicked."""

    def delete_button_slot(self) -> None:
        """Called when the delete button is clicked."""

    def stat_list_view_clicked_slot(self, index: QModelIndex) -> None:
        """
        Called when a stat is selected from the add stats list view.
        :param index: Index of the clicked item
        """
        selected_stat_name: str = self.stat_list_model.stat_name_list[index.row()]

class CardConfigStatTableModel(QAbstractTableModel):
    """Table model that displays the list of stats currently on the card."""

    def __init__(self, card: Card, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.card: Card = card
        """Card being edited."""
        
    def flags(self, index: QModelIndex):
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable

    def data(self, index: QModelIndex, role: int) -> Any:
        if self.card.stat_names is None or role != Qt.ItemDataRole.DisplayRole:
            return QVariant()
        stat_name: str = self.card.stat_names[index.row()]

        config: Optional[StatConfig] = self.card.config_for_stat(stat_name)
        if config is None:
            return QVariant()
        
        if index.column() == 0:  # Stat Name column
            return stat_name
        elif index.column() == 1:  # Display Name column
            return config.display_name
        elif index.column() == 2:  # Subtext column
            return config.subtext
        elif index.column() == 3:  # Max column
            return config.show_max or "False"
        elif index.column() == 4:  # Min column
            return config.show_min or "False"
        else:  # No match, unknown column
            return QVariant()

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return CARD_CONFIG_STAT_TABLE_HEADERS[section]

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(CARD_CONFIG_STAT_TABLE_HEADERS)

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        if not self.card.stat_names:
            return 0
        return len(self.card.stat_names)
    
class StatListModel(QAbstractListModel):
    """Model to display a list of stat names the user can click on to add stats to the stat card."""

    def __init__(self, stat_name_list: list[str], parent: Optional[QWidget] = None):
        super().__init__(parent)

        self.stat_name_list: list[str] = stat_name_list
        """List of stat names that can be added"""

    def flags(self, index: QModelIndex):
        return Qt.ItemFlag.ItemIsEnabled

    def data(self, index: QModelIndex, role: int) -> Any:
        if role == Qt.ItemDataRole.DisplayRole:
            return self.stat_name_list[index.row()]

        return QVariant()

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int: 
        return len(self.stat_name_list)
    