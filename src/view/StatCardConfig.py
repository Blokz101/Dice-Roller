from typing import Optional
from PyQt6.QtWidgets import QDialog, QWidget
from src.view.Ui_StatCardConfig import Ui_StatCardConfig


class StatCardConfig(QDialog, Ui_StatCardConfig):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setupUi(self)
