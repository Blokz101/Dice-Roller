from __future__ import annotations
from typing import Optional, Self
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QFont
from src import GRID_SIZE
from src.model.Card import Card, StatConfig
from src.model.Stat import Stat
from src.model.Note import Note
from src.view.CardWidget import CardWidget
from src.view.StatCardConfig import StatCardConfig


class _SingleStatWidget(QWidget):

    def __init__(self, parent: StatWidget, stat: Stat):
        super().__init__(parent)

        # Instance vars
        self.card: Card = parent.card
        self.stat: Stat = stat
        self.value_label: QLabel
        self.subtext_label: QLabel
        self.name_label: QLabel

        self.build_new_layout()

    def build_new_layout(self):
        layout = QVBoxLayout()
        self.value_label = QLabel(
            str(self.stat.value)
        )  # TODO Process self.stat.value before using it in the future
        self.subtext_label = QLabel()
        self.name_label = QLabel(self.stat.name)

        # Set the subtext for each stat if it exists
        stat_config: Optional[StatConfig] = self.card.config_for_stat(self.stat.name)
        if stat_config is not None and stat_config.subtext is not None:
            self.subtext_label.setText(stat_config.subtext)
            self.subtext_label.setVisible(True)
        else:
            self.subtext_label.setVisible(False)

        # Configure font
        value_font: QFont = QFont()
        value_font.setPointSize(20)

        # Configure widgets
        self.value_label.setFont(value_font)
        self.value_label.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtext_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Configure layout
        layout.addWidget(self.value_label)
        layout.addWidget(self.subtext_label)
        layout.addWidget(self.name_label)

        self.setLayout(layout)


class StatWidget(CardWidget):

    def __init__(
        self, card: Card, stat_list: list[Stat], parent: Optional[QWidget] = None
    ):
        super().__init__(card, parent)

        # Model related instance vars
        self.stat_list: list[Stat] = stat_list
        """List of stats that are relevant to this widget."""

        # GUI related instance vars
        self.stat_layout: QHBoxLayout

        # Widget config
        self.build_new_layout()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

    def build_new_layout(self) -> None:
        """Discard the old contents of the layout and create a new layout with the current stats."""
        self.stat_layout = QHBoxLayout()

        # Add single stat widgets to the layout
        for stat in self.stat_list:
            single_stat_widget: _SingleStatWidget = _SingleStatWidget(self, stat)
            self.stat_layout.addWidget(single_stat_widget)

        # Configure layout
        self.stat_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.stat_layout)

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

        # Select all stats that are relevant to the card
        return cls(
            card, [stat for stat in stat_list if stat.name in (card.stat_names or [])]
        )

    def edit_card(self) -> None:
        config = StatCardConfig(self)
        config.exec()

    def cells_width(self):
        hinted_size: QSize = super().sizeHint()

        if hinted_size.width() == -1:
            return 1
        if hinted_size.width() % GRID_SIZE == 0 and hinted_size.width() > 0:
            return hinted_size.width() // GRID_SIZE
        return hinted_size.width() // GRID_SIZE + 1

    def cells_height(self):
        hinted_size: QSize = super().sizeHint()

        if hinted_size.height() == -1:
            return 1
        if hinted_size.height() % GRID_SIZE == 0 and hinted_size.height() > 0:
            return hinted_size.height() // GRID_SIZE
        return hinted_size.height() // GRID_SIZE + 1
