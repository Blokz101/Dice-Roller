from __future__ import annotations
from typing import Optional, Any


class Stat:

    def __init__(
        self,
        name: str,
        value: int = 0,
        max_value: Optional[int] = None,
        min_value: Optional[int] = None,
    ):
        # Instance variables stored in the JSON
        self.name: str = name
        """Name of the stat."""
        self.value: int = value
        """Current value of the stat."""
        self.max: Optional[int] = max_value
        """Maximum value of the stat."""
        self.min: Optional[int] = min_value
        """Minimum value of the stat."""
        self.history: list[tuple[str, str]] = []
        """History of changes to the stat. The first str is the description, the second str is the edit."""

    @classmethod
    def from_dict(cls, card_dict: dict[str, Any]) -> Optional[Stat]:
        if not all(required_attr in card_dict for required_attr in ["name", "value"]):
            return None

        card: Stat = Stat(card_dict["name"], card_dict["value"])
        if "max" in card_dict:
            card.max = card_dict["max"]
        if "min" in card_dict:
            card.min = card_dict["min"]
        if "history" in card_dict:
            entry: Any
            for entry in card_dict["history"]:
                if not isinstance(entry, list) or not len(entry) == 2:  # type: ignore
                    return None
                card.history.append((entry[0], entry[1]))  # type: ignore

        return card

    def to_dict(self) -> dict[str, Any]:
        card_dict: dict[str, Any] = {"name": self.name, "value": self.value}
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

    def set_value(self, new_value: int) -> bool:
        """
        Sets the value and discards the history.
        :param new_value: New value to set for the stat
        :returns: True if new_value was different and set, false otherwise
        """
        if new_value == self.value:
            return False
        self.value = new_value
        self.history = []
        return True

    def assign(self, other: Stat) -> None:
        """
        Updates all instance variables to contain the values from the other stat.
        :param other: Stat to copy values from
        """
        self.name = other.name
        self.value = other.value
        self.max = other.max
        self.min = other.min
        self.history = other.history.copy()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Stat):
            return False

        return (
            self.name == other.name
            and self.value == other.value
            and self.max == other.max
            and self.min == other.min
            and self.history == other.history
        )
