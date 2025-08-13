from __future__ import annotations
from typing import Optional, Any, cast
from src.model.Card import Card
from src import CardType


class Stat(Card):

    def __init__(
        self,
        name: str,
        initial_value: int = 0,
        max_value: Optional[int] = None,
        min_value: Optional[int] = None,
        column: Optional[int] = None,
        row: Optional[int] = None,
        column_span: Optional[int] = None,
        row_span: Optional[int] = None,
    ):
        super().__init__(
            name=name,
            card_type=CardType.STAT,
            column=column,
            row=row,
            column_span=column_span,
            row_span=row_span,
        )

        # Instance variables stored in the JSON
        self.value: int = initial_value
        """Current value of the stat."""
        self.max: Optional[int] = max_value
        """Maximum value of the stat."""
        self.min: Optional[int] = min_value
        """Minimum value of the stat."""
        self.history: list[tuple[str, str]] = []
        """History of changes to the stat. The first str is the description, the second str is the edit."""

    @classmethod
    def from_dict(cls, card_dict: dict[str, Any]) -> Optional[Stat]:
        if "value" not in card_dict.keys():
            return None

        card: Optional[Stat] = super().base_from_dict(card_dict, CardType.STAT)
        if card is None:
            return None
        card.value = card_dict["value"]
        if "max" in card_dict.keys():
            card.max = card_dict["max"]
        if "min" in card_dict.keys():
            card.min = card_dict["min"]
        if "history" in card_dict.keys():
            card.history = card_dict["history"]

        return card

    def to_dict(self) -> dict[str, Any]:
        card_dict: dict[str, Any] = super().to_dict()
        card_dict["value"] = self.value
        if self.max is not None:
            card_dict["max"] = self.max
        if self.min is not None:
            card_dict["min"] = self.min
        if len(self.history) > 0:
            card_dict["history"] = self.history
        return card_dict

    def has_history(self) -> bool:
        """
        Checks if the stat has a history of changes.
        :return: True if the stat has a history, False otherwise
        """
        return len(self.history) > 0

    def set_value(self, new_value: int) -> None:
        """
        Sets the value and discards the history.
        :param new_value: New value to set for the stat
        """
        self.value = new_value
        self.history = []

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Stat):
            return False

        return (
            super().__eq__(other)
            and self.value == other.value
            and self.max == other.max
            and self.min == other.min
            and self.history == other.history
        )
