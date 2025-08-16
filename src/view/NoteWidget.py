from typing import Optional, Self
from PyQt6.QtWidgets import QWidget, QTextBrowser, QPushButton, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from src.model.Stat import Stat
from src.model.Card import Card
from src.model.Note import Note
from src.view.CardWidget import CardWidget
from src.view.NoteCardConfig import NoteCardConfig


class NoteWidget(CardWidget):

    def __init__(self, card: Card, note: Note, parent: Optional[QWidget] = None):
        super().__init__(card, parent)

        # Model related instance vars
        self.note: Note = note
        """Note that is relevant to this widget."""

        # GUI related instance vars
        self.title_label: QLabel
        self.text_browser: QTextBrowser
        self.button_list: list[QPushButton]

        # Widget config
        self.build_new_layout()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

    def build_new_layout(self) -> None:
        layout: QVBoxLayout = QVBoxLayout()

        self.title_label = QLabel(self.card.name)

        self.text_browser = QTextBrowser()
        self.text_browser.setText(self.note.text)
        self.text_browser.setReadOnly(True)
        self.text_browser.setTextInteractionFlags(
            Qt.TextInteractionFlag.NoTextInteraction
        )
        self.text_browser.setOpenExternalLinks(True)
        self.text_browser.setOpenLinks(True)

        layout.addWidget(self.title_label)
        layout.addWidget(self.text_browser)
        # TODO Add code to add buttons to layout here

        self.setLayout(layout)

    @classmethod
    def from_card(cls, card: Card, data_list: list[Stat | Note]) -> Self:
        note: Optional[Note] = None
        for data in data_list:
            if not isinstance(data, Note):
                raise ValueError(
                    "Data list contains Stat instance, expected only Note."
                )
            if card.note_name == data.name:
                note = data
                break
        if note is None:
            raise ValueError(
                "data_list must contain a Note with name that matches card.note_name."
            )
        return cls(card, note)

    def edit_card(self) -> None:
        config = NoteCardConfig(self)
        config.exec()

    def cells_width(self) -> int:
        return self.card.column_span or 1

    def cells_height(self) -> int:
        return self.card.row_span or 1
