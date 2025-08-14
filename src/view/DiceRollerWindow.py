from pathlib import Path
from typing import Optional
from PyQt6.QtWidgets import QMainWindow, QWidget, QFileDialog
from src.view.Ui_DiceRollerWindow import Ui_DiceRollerWindow
from src.model.Sheet import Sheet
from src.view.SheetWidget import SheetWidget


class DiceRollerWindow(QMainWindow, Ui_DiceRollerWindow):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setupUi(self)  # type: ignore

        # Signal and slot config
        self.sheet_tab_widget.tabCloseRequested.connect(self.tab_close_requested)  # type: ignore
        self.action_open_sheet.triggered.connect(self.open_sheet_slot)  # type: ignore

    def add_sheet(self, sheet: SheetWidget) -> None:
        self.sheet_tab_widget.addTab(sheet, sheet.sheet.name)

    def tab_close_requested(self, index: int) -> None:
        self.sheet_tab_widget.removeTab(index)

    def open_sheet_slot(self) -> None:
        """Slot called when the open sheet action is triggered. Opens new sheets from JSON files."""
        file_names: list[str]
        file_names, _ = QFileDialog.getOpenFileNames(self, filter="JSON files (*.json)")
        for file in file_names:
            sheet: Sheet = Sheet.from_json(Path(file))
            self.add_sheet(SheetWidget(sheet))
