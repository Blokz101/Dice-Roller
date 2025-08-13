from typing import Optional
from PyQt6.QtWidgets import QWidget
from src.view.Ui_HomeSheet import Ui_HomeSheet


class HomeSheet(QWidget, Ui_HomeSheet):

    def __init__(self, parent: Optional[QWidget]):
        super().__init__(parent)
        self.setupUi(self)
