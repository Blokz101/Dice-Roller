from typing import Optional
from PyQt6.QtWidgets import QMainWindow, QWidget
from src.view.Ui_DiceRollerWindow import Ui_DiceRollerWindow
from src.view.Sheet import Sheet


class DiceRollerWindow(QMainWindow, Ui_DiceRollerWindow):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setupUi(self)

        # Signal and slot config
        self.sheet_tab_widget.tabCloseRequested.connect(self.tab_close_requested)

    def add_sheet(self, sheet: Sheet, name: str) -> None:
        self.sheet_tab_widget.addTab(sheet, name)

    def tab_close_requested(self, index: int) -> None:
        self.sheet_tab_widget.removeTab(index)
