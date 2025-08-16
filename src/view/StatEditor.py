from typing import Optional
from PyQt6.QtWidgets import QDialog, QWidget
from src.view.Ui_StatEditor import Ui_StatEditor


class StatEditor(QDialog, Ui_StatEditor):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setupUi(self)
