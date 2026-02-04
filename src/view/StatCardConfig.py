from typing import Optional, Any
from copy import deepcopy
from PyQt6.QtWidgets import QDialog, QWidget, QAbstractItemView, QStyledItemDelegate, QStyleOptionViewItem, QCheckBox
from PyQt6.QtCore import QAbstractTableModel, QAbstractListModel, QModelIndex, Qt, QVariant, QItemSelectionModel, QAbstractItemModel
from src.view import CARD_CONFIG_STAT_TABLE_HEADERS
from src.view.Ui_StatCardConfig import Ui_StatCardConfig
from src.model.Sheet import Sheet
from src.model.Card import Card, StatConfig


class StatCardConfig(QDialog, Ui_StatCardConfig):

    def __init__(self, sheet: Sheet, card: Card, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self.sheet: Sheet = deepcopy(sheet)
        """Sheet being edited."""
        self.card: Card = card
        """Card being edited."""
        self.removed_configs: dict[str, StatConfig] = {}
        """List of stat configs that have been removed from the card. Used when the user adds a previously removed StatConfig. Previous values are replaced instead of creating blank StatConfig."""
        self.card_config_stat_table_model: CardConfigStatTableModel = CardConfigStatTableModel(self.card)
        """Model for the card stats table view."""
        self.stat_list_model: StatListModel = StatListModel(
            sorted(
                [
                    stat.name
                    for stat in sheet.stat_list
                    if stat.name not in (self.card.stat_names or [])
                ]
            )
        )
        """Model for the stat list view."""

        self.setupUi(self) # type: ignore

        self.card_config_stat_table_view.setModel(self.card_config_stat_table_model)
        self.stat_list_view.setModel(self.stat_list_model)

        self.stat_list_view.clicked.connect(self.stat_list_view_clicked_slot) # type: ignore
        self.order_up_button.clicked.connect(self.order_up_button_slot)  # type: ignore
        self.order_down_button.clicked.connect(self.order_down_button_slot)  # type: ignore
        self.delete_button.clicked.connect(self.delete_button_slot)  # type: ignore

        # Configure widgets
        self.card_config_stat_table_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.stat_list_view.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def order_up_button_slot(self) -> None:
        """Called when the order up button is clicked."""
        if self.card.stat_names is None:
            return
        selected_row_index: int = self.card_config_stat_table_view.currentIndex().row()
        if selected_row_index < 1:
            return
        self.card.swap_stats(selected_row_index, selected_row_index - 1)
        self.card_config_stat_table_model.layoutChanged.emit()
        self.card_config_stat_table_view.setCurrentIndex(
            self.card_config_stat_table_model.index(selected_row_index-1, 0)
        )

    def order_down_button_slot(self) -> None:
        """Called when the order down button is clicked."""
        if self.card.stat_names is None:
            return
        selected_row_index: int = self.card_config_stat_table_view.currentIndex().row()
        if selected_row_index > len(self.card.stat_names) - 2:
            return
        self.card.swap_stats(selected_row_index, selected_row_index + 1)
        self.card_config_stat_table_model.layoutChanged.emit()
        self.card_config_stat_table_view.setCurrentIndex(
            self.card_config_stat_table_model.index(selected_row_index+1, 0)
        )

    def delete_button_slot(self) -> None:
        """Called when the delete button is clicked."""
        if self.card.stat_names is None:
            return
        table_selection_model: Optional[QItemSelectionModel] = self.card_config_stat_table_view.selectionModel()
        if table_selection_model is None:
            return

        # Attempt to delete the stat
        for selected_stat_name in [self.card.stat_names[idx.row()] for idx in table_selection_model.selectedRows(0)]:
            deleted_stat: Optional[StatConfig] = self.card.delete_stat(selected_stat_name)
            if deleted_stat is None:
               continue 
            self.removed_configs[selected_stat_name] = deleted_stat
            self.stat_list_model.stat_name_list.append(selected_stat_name)
            self.stat_list_model.stat_name_list.sort()
            self.card_config_stat_table_model.layoutChanged.emit()
            self.stat_list_model.layoutChanged.emit()
        table_selection_model.clearSelection()

    def stat_list_view_clicked_slot(self, index: QModelIndex) -> None:
        """
        Called when a stat is selected from the add stats list view.
        :param index: Index of the clicked item
        """
        selected_stat_name: str = self.stat_list_model.stat_name_list[index.row()]

        self.stat_list_model.stat_name_list.remove(selected_stat_name)
        self.stat_list_model.layoutChanged.emit()

        self.card.add_stat(
            selected_stat_name,
            config=self.removed_configs.get(selected_stat_name)
        )
        self.card_config_stat_table_model.layoutChanged.emit()

class CardConfigStatTableModel(QAbstractTableModel):
    """Table model that displays the list of stats currently on the card."""

    def __init__(self, card: Card, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.card: Card = card
        """Card being edited."""
        
    def flags(self, index: QModelIndex):
        flag: Qt.ItemFlag = Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
        if index.column() in [1, 2]:
            flag = flag | Qt.ItemFlag.ItemIsEditable
        if index.column() in [3, 4]:
            flag = flag | Qt.ItemFlag.ItemIsUserCheckable
        return flag
        
    def data(self, index: QModelIndex, role: int) -> Any:
        if self.card.stat_names is None:
            return QVariant()
        stat_name: str = self.card.stat_names[index.row()]

        config: Optional[StatConfig] = self.card.config_for_stat(stat_name)
        if config is None:
            return QVariant()
        
        if role == Qt.ItemDataRole.DisplayRole:
            if index.column() == 0:  # Stat Name column
                return stat_name
            elif index.column() == 1:  # Display Name column
                return config.display_name
            elif index.column() == 2:  # Subtext column
                return config.subtext
            elif index.column() == 3:  # Max column
                return "True" if config.show_max else "False"
            elif index.column() == 4:  # Min column
                return "True" if config.show_min else "False"

        if role == Qt.ItemDataRole.CheckStateRole:
            if index.column() == 3:  # Max column
                return Qt.CheckState.Checked if config.show_max or False else Qt.CheckState.Unchecked
            elif index.column() == 4:  # Min column
                return Qt.CheckState.Checked if config.show_min or False else Qt.CheckState.Unchecked

        return QVariant()

    def setData(self, index: QModelIndex, value: Any, role: int) -> bool:
        if self.card.stat_names is None:
            return False
        stat_name: str = self.card.stat_names[index.row()]

        config: Optional[StatConfig] = self.card.config_for_stat(stat_name)
        if config is None:
            return False

        if role == Qt.ItemDataRole.EditRole:
            if index.column() == 1: # Display Name
                config.display_name = str(value)
                return True
            if index.column() == 2: # Subtext
                config.subtext = str(value)
                return True
            return False

        if role == Qt.ItemDataRole.CheckStateRole:
            if index.column() == 3:
                config.show_max = not config.show_max
                return True
            if index.column() == 4:
                config.show_min = not config.show_min
                return True
            return False

        return False 
    
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
    