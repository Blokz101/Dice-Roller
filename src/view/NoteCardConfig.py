from typing import Optional
from PyQt6.QtWidgets import QDialog, QWidget
from src.view.Ui_NoteCardConfig import Ui_NoteCardConfig


class NoteCardConfig(QDialog, Ui_NoteCardConfig):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setupUi(self)
