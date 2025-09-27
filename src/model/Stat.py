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

    def set_value(self, new_value: int) -> None:
        """
        Sets the value and discards the history.
        :param new_value: New value to set for the stat
        """
        self.value = new_value
        self.history = [("Initial", str(new_value))]

    def calculate_value(self) -> list[Optional[int]]:
        """
        Sets self.value based on the history list.
        :returns: True if the value could be calculated and was set from the history"
        """
        # If there is no history
        if len(self.history) == 0:
            self.value = 0
            return [0]

        value_list: list[Optional[int]] = []
        for _, value_mod in self.history:

            prev_value: Optional[int] = 0 if len(value_list) == 0 else value_list[-1]

            # If the modifier is empty skip parsing it
            if value_mod == "":
                value_list.append(prev_value)
                continue

            try: 

                # If the modifier starts with an =, set it unconditionally 
                if value_mod[0] == "=" :
                    value_list.append(int(eval(value_mod[1:])))

                # If the modifier is a digit, addition to value is assumed
                elif value_mod[0].isdigit():
                    if prev_value is None:
                        value_list.append(None)
                    else:
                        value_list.append(prev_value + int(eval(value_mod)))

                # If the modifier is an operation, parse with the operator
                elif value_mod[0] in "+-*/":
                    if prev_value is None:
                        value_list.append(None)
                    else:
                        value_list.append(int(eval(f"{prev_value}{value_mod}")))

                # If the modifier starts with an unknown, it cannot be parsed
                else:
                    value_list.append(None)

            # If the modifier cannot be parsed to an int, it cannot be parsed
            except SyntaxError:
                value_list.append(None)
            except ValueError:
                value_list.append(None)
        
        # Set the value if possible and return the list
        if value_list[-1] is not None:
            self.value = value_list[-1]
        return value_list

    def remove_empty_history_rows(self) -> None:
        """Removes all empty history rows."""
        self.history = [row for row in self.history if row[0] != "" or row[1] != ""]

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
