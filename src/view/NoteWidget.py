from typing import Optional, Self
from PyQt6.QtWidgets import QWidget
from src.model.Stat import Stat
from src.model.Card import Card
from src.model.Note import Note
from src.view.CardWidget import CardWidget


class NoteWidget(CardWidget):

    def __init__(self, card: Card, note: Note, parent: Optional[QWidget] = None):
        super().__init__(card, parent)

        # Model related instance vars
        self.note: Note = note
        """Note that is relevant to this widget."""

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

    def cells_width(self) -> int:
        return self.card.column_span or 1

    def cells_height(self) -> int:
        return self.card.row_span or 1
