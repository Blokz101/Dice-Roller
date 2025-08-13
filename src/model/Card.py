from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, Any, TypeVar, Type
from src import CardType

CardT = TypeVar("CardT", bound="Card")


class Card(ABC):

    def __init__(
        self,
        name: str,
        card_type: CardType,
        column: Optional[int] = None,
        row: Optional[int] = None,
        column_span: Optional[int] = None,
        row_span: Optional[int] = None,
    ):

        # Instance variables stored in the JSON
        self.name: int = name
        """Name of the card."""
        self.card_type: CardType = card_type
        """Type of the card."""
        self.column: Optional[int] = column
        """Top left column of the card if it is placed on the sheet."""
        self.row: Optional[int] = row
        """Top left row of the card if it is placed on the sheet."""
        self.column_span: Optional[int] = column_span
        """Number of columns the card spans. Ignored by Stat cards."""
        self.row_span: Optional[int] = row_span
        """Number of rows the card spans. Ignored by Stat cards."""

        # Other instance variables

    @classmethod
    @abstractmethod
    def from_dict(cls: Type[CardT], card_dict: dict[str, Any]) -> Optional[CardT]:
        """
        Creates a Card object from a dict if possible.
        :param card_dict: Dictionary containing card attributes
        :returns: Card object or None if required attributes are not present
        """

    @classmethod
    def base_from_dict(
        cls: Type[CardT], card_dict: dict[str, Any], card_type: CardType
    ) -> Optional[CardT]:
        """
        Creates a Card object from a dict if possible. Requires card type to be specified.
        :param card_dict: Dictionary containing card attributes
        :param card_type: The type of the card
        :returns: Card object or None if required attributes are not present
        """
        if "name" not in card_dict.keys():
            return None

        card: Card = cls(card_dict["name"], card_type)
        if "column" in card_dict.keys():
            card.column = card_dict["column"]
        if "row" in card_dict.keys():
            card.row = card_dict["row"]
        if "column_span" in card_dict.keys():
            card.column_span = card_dict["column_span"]
        if "row_span" in card_dict.keys():
            card.row_span = card_dict["row_span"]

        return card

    def to_dict(self) -> dict[str, Any]:
        """
        Converts the values to a dict.
        Should be overridden by subclasses.
        :returns: Dict containing this cards values
        """
        card_dict: dict[str, Any] = {"name": self.name}
        if self.column is not None:
            card_dict["column"] = self.column
        if self.row is not None:
            card_dict["row"] = self.row
        if self.column_span is not None:
            card_dict["column_span"] = self.column_span
        if self.row_span is not None:
            card_dict["row_span"] = self.row_span
        return card_dict

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
        )
