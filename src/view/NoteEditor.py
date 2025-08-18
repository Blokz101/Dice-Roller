from typing import Optional
from PyQt6.QtWidgets import QDialog, QWidget
from src.model.Sheet import Sheet
from src.view.Ui_NoteEditor import Ui_NoteEditor


class NoteEditor(QDialog, Ui_NoteEditor):

    def __init__(self, sheet: Sheet, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setupUi(self)
