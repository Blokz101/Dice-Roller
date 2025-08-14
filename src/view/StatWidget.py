from typing import Optional, Self
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QSizePolicy
from PyQt6.QtCore import QSize
from src import GRID_SIZE
from src.model.Card import Card
from src.model.Stat import Stat
from src.model.Note import Note
from src.view.CardWidget import CardWidget


class StatWidget(CardWidget):

    def __init__(
        self, card: Card, stat_list: list[Stat], parent: Optional[QWidget] = None
    ):
        super().__init__(card, parent)

        # Model related instance vars
        self.stat_list: list[Stat] = stat_list
        """List of stats that are relevant to this widget."""

        button: QPushButton = QPushButton(self.card.name)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout: QHBoxLayout = QHBoxLayout()
        layout.addWidget(button)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    @classmethod
    def from_card(cls, card: Card, data_list: list[Stat | Note]) -> Self:
        """
        Creates a StatWidget from a Card model instance.
        :param card: Card model instance
        :param data_list: List of stats relevant to this widget
        :returns: StatWidget instance
        """
        stat_list: list[Stat] = []
        for data in data_list:
            if not isinstance(data, Stat):
                raise ValueError(
                    "Data list contains Note instance, expected only Stat."
                )
            stat_list.append(data)
        return cls(
            card, [stat for stat in stat_list if stat.name in (card.stat_names or [])]
        )

    def cells_width(self):
        hinted_size: QSize = super().sizeHint()

        if hinted_size.width() % GRID_SIZE == 0:
            return hinted_size.width() // GRID_SIZE
        return hinted_size.width() // GRID_SIZE + 1

    def cells_height(self):
        hinted_size: QSize = super().sizeHint()

        if hinted_size.height() % GRID_SIZE == 0:
            return hinted_size.height() // GRID_SIZE
        return hinted_size.height() // GRID_SIZE + 1
