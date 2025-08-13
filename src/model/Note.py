from __future__ import annotations
from typing import Optional, Any, cast
from src import CardType
from src.model.Card import Card
from src.model.Instruction import Instruction


class Note(Card):

    def __init__(
        self,
        name: str,
        raw_text: str = "",
        column: Optional[int] = None,
        row: Optional[int] = None,
        column_span: Optional[int] = None,
        row_span: Optional[int] = None,
    ):
        super().__init__(
            name=name,
            card_type=CardType.NOTE,
            column=column,
            row=row,
            column_span=column_span,
            row_span=row_span,
        )

        # Instance variables stored in JSON
        self.raw_text: str = raw_text

        # Instance variables parsed from raw_text
        self.text: str = ""
        self.inst_list: list[Instruction] = []

        # Parse raw text
        self.parse_raw_text()

    def parse_raw_text(self) -> None:
        """Parses self's text to populate text and inst_list values."""
        # TODO Implement this method

    @classmethod
    def from_dict(cls, card_dict: dict[str, Any]) -> Optional[Note]:
        if "text" not in card_dict.keys():
            return None

        card: Optional[Note] = super().base_from_dict(card_dict, CardType.NOTE)
        if card is None:
            return None
        card.raw_text = card_dict["text"]
        card.parse_raw_text()

        return card

    def to_dict(self) -> dict[str, Any]:
        note_dict: dict[str, Any] = super().to_dict()
        note_dict["text"] = self.raw_text
        return note_dict
