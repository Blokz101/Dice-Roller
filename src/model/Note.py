from __future__ import annotations
from typing import Optional, Any
from src.model.Instruction import Instruction


class Note:

    def __init__(
        self,
        name: str,
        raw_text: str = "",
    ):
        # Instance variables stored in JSON
        self.name = name
        """Name of the note."""
        self.raw_text: str = raw_text
        """Raw text of the note."""

        # Instance variables parsed from raw_text
        self.text: str = ""
        """Text without button syntax."""
        self.button_data: list[tuple[str, str]] = []
        """List of data required for the button in the format (button name, instruction)."""

        # Parse raw text
        self.parse_raw_text()

    def parse_raw_text(self) -> None:
        """Parses self's text to populate text and inst_list values."""
        self.text = self.raw_text
        # TODO Implement this method

    @classmethod
    def from_dict(cls, card_dict: dict[str, Any]) -> Optional[Note]:
        if "name" not in card_dict or "text" not in card_dict:
            return None

        card: Note = Note(name=card_dict["name"], raw_text=card_dict["text"])
        card.parse_raw_text()

        return card

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "text": self.raw_text}

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Note):
            return False

        return self.name == other.name and self.raw_text == other.raw_text
