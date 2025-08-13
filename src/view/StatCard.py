from typing import Optional
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QSizePolicy
from src.view.Card import Card


class StatCard(Card):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        button: QPushButton = QPushButton("FOOOOOOOOOOBAR")
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout: QHBoxLayout = QHBoxLayout()
        layout.addWidget(button)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
