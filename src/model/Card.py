from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Any
from src import CardType


@dataclass
class StatConfig:
    """Data class to hold configs for an individual stat on a card."""

    show_max: Optional[bool] = None
    show_min: Optional[bool] = None
    subtext: Optional[str] = None
    display_name: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> StatConfig:
        return cls(
            show_max=data.get("show_max", None),
            show_min=data.get("show_min", None),
            subtext=data.get("subtext", None),
            display_name=data.get("display_name", None),
        )

    def to_dict(self) -> dict[str, Any]:
        config_dict: dict[str, Any] = {}
        if self.show_max is not None:
            config_dict["show_max"] = self.show_max
        if self.show_min is not None:
            config_dict["show_min"] = self.show_min
        if self.subtext is not None:
            config_dict["subtext"] = self.subtext
        if self.display_name is not None:
            config_dict["display_name"] = self.display_name

        return config_dict


class Card:

    def __init__(
        self,
        name: str,
        card_type: CardType,
        column: int,
        row: int,
        column_span: Optional[int] = None,
        row_span: Optional[int] = None,
        note_name: Optional[str] = None,
        stat_names: Optional[list[str]] = None,
        stat_configs: Optional[dict[str, StatConfig]] = None,
    ):

        # Instance variables stored in the JSON
        self.name: str = name
        """Name of the card."""
        self.card_type: CardType = card_type
        """Type of the card."""
        self.column: int = column
        """Top left column of the card if it is placed on the sheet."""
        self.row: int = row
        """Top left row of the card if it is placed on the sheet."""
        self.column_span: Optional[int] = column_span
        """Number of columns the card spans. Ignored by Stat cards."""
        self.row_span: Optional[int] = row_span
        """Number of rows the card spans. Ignored by Stat cards."""
        self.note_name: Optional[str] = note_name
        """If this is a note card, this is the name of the note displayed on it. None otherwise."""
        self.stat_names: Optional[list[str]] = stat_names
        """If this is a stat card, this is the list of names of the stats displayed on it. None otherwise."""
        self.stat_configs: Optional[dict[str, StatConfig]] = stat_configs
        """If this is a stat card, this is the config for each stat displayed on it. None otherwise."""

        # Other instance variables

    @classmethod
    def from_dict(cls, card_dict: dict[str, Any]) -> Optional[Card]:
        """
        Creates a Card object from a dict if possible.
        :param card_dict: Dictionary containing card attributes
        :param card_type: The type of the card
        :returns: Card object or None if required attributes are not present
        """
        # Ensure required attrs are present for a base card and set them
        if not all(
            required_attr in card_dict
            for required_attr in ["name", "card_type", "row", "column"]
        ):
            return None

        card: Card = cls(
            name=card_dict["name"],
            card_type=CardType(card_dict["card_type"]),
            column=card_dict["column"],
            row=card_dict["row"],
        )

        # Set optional fields
        if "column_span" in card_dict:
            card.column_span = card_dict["column_span"]
        if "row_span" in card_dict:
            card.row_span = card_dict["row_span"]

        # If this card is a stat card, ensure required attrs are present and set them
        if card.card_type == CardType.STAT:
            if "stat_names" not in card_dict:
                return None
            if "stat_configs" in card_dict:  # If stat_configs is present check its type
                if not isinstance(card_dict["stat_configs"], dict):
                    return None

            card.stat_names = card_dict["stat_names"]
            if "stat_configs" in card_dict:
                card.stat_configs = {
                    stat_name: StatConfig.from_dict(stat_config)  # type: ignore
                    for stat_name, stat_config in card_dict["stat_configs"].items()  # type: ignore
                }

        # If this card is a note card, ensure required attrs are present and set them
        elif card.card_type == CardType.NOTE:
            if "note_name" not in card_dict:
                return None

            card.note_name = card_dict["note_name"]

        # Something has gone very wrong...
        else:
            return None

        return card

    def to_dict(self) -> dict[str, Any]:
        """
        Converts the values to a dict.
        :returns: Dict containing this cards values
        """
        card_dict: dict[str, Any] = {
            "name": self.name,
            "card_type": self.card_type.value,
            "column": self.column,
            "row": self.row,
        }
        if self.column_span is not None:
            card_dict["column_span"] = self.column_span
        if self.row_span is not None:
            card_dict["row_span"] = self.row_span

        # Add stat attrs if this is a stat card
        if self.card_type == CardType.STAT:
            card_dict["stat_names"] = self.stat_names
            if self.stat_configs is not None:
                card_dict["stat_configs"] = {
                    stat_name: stat_config.to_dict()
                    for stat_name, stat_config in self.stat_configs.items()
                }

        # Add note attrs if this is a note card
        if self.card_type == CardType.NOTE:
            card_dict["note_name"] = self.note_name

        return card_dict

    def config_for_stat(self, stat_name: str) -> Optional[StatConfig]:
        """
        Returns the config for a stat on this card.
        :param stat_name: Name of the stat to get the config for
        :return: StatConfig object or None if the stat is not present
        """
        if self.stat_configs is None:
            return None
        return self.stat_configs.get(stat_name, None)

    def assign(self, other: Card) -> None:
        """
        Updates all instance variables to contain the values from the other card.
        :param other: Card to copy values from
        """
        self.name = other.name
        self.card_type = other.card_type
        self.column = other.column
        self.row = other.row
        self.column_span = other.column_span
        self.row_span = other.row_span
        self.note_name = other.note_name
        self.stat_names = other.stat_names.copy() if other.stat_names is not None else None
        if other.stat_configs is not None:
            self.stat_configs = {
                name: StatConfig(
                    show_max=config.show_max,
                    show_min=config.show_min,
                    subtext=config.subtext,
                    display_name=config.display_name,
                )
                for name, config in other.stat_configs.items()
            }
        else:
            self.stat_configs = None

    def __eq__(self, obj: object) -> bool:
        if not isinstance(obj, Card):
            return False

        return (
            self.name == obj.name
            and self.card_type == obj.card_type
            and self.column == obj.column
            and self.row == obj.row
            and self.column_span == obj.column_span
            and self.row_span == obj.row_span
            and self.note_name == obj.note_name
            and self.stat_names == obj.stat_names
            and self.stat_configs == obj.stat_configs
        )
