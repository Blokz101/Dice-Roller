from __future__ import annotations
from typing import Any, Optional
import json
from pathlib import Path
from src.model.Card import Card
from src.model.Stat import Stat
from src.model.Note import Note


class Sheet:
    """Represents a character sheet containing stats and notes."""

    def __init__(
        self,
        stat_list: Optional[list[Stat]] = None,
        note_list: Optional[list[Note]] = None,
        card_list: Optional[list[Card]] = None,
    ):
        self.stat_list: list[Stat] = stat_list if stat_list is not None else []
        """List of Stat data objects."""
        self.note_list: list[Note] = note_list if note_list is not None else []
        """List of Note data objects."""
        self.card_list: list[Card] = card_list if card_list is not None else []
        """List of Card objects on the sheet."""
        self.saved_to_file: bool = False
        """Indicates whether the sheet has been saved to a file."""

    @staticmethod
    def from_json(json_path: Path) -> Sheet:
        """
        Creates a sheet object from a JSON file.
        :param json_path: The path to the JSON file
        :return: A Sheet object
        """
        if not json_path.exists():
            raise FileNotFoundError(f"JSON file {json_path} does not exist.")
        if not json_path.suffix == ".json":
            raise ValueError(f"File {json_path} is not a JSON file.")

        json_as_dict: dict[str, Any]
        with open(json_path, "r", encoding="utf-8") as json_file:
            json_as_dict = json.load(json_file)

        return Sheet.from_dict(json_as_dict)

    @staticmethod
    def from_dict(sheet_dict: dict[str, Any]) -> Sheet:
        """
        Creates a sheet object from a dictionary.
        :param sheet_dict: The input dictionary
        :return: A Sheet object
        """

        # Ensure the dict has the required keys
        if not all(table in sheet_dict for table in ["stats", "notes", "cards"]):
            raise ValueError("Input dict is missing required keys.")

        # Ensure the required dict keys can be parsed
        if (
            not isinstance(sheet_dict["stats"], list)
            or not isinstance(sheet_dict["notes"], list)
            or not isinstance(sheet_dict["cards"], list)
        ):
            raise ValueError("Input dict has incorrect types for keys.")

        return Sheet(
            stat_list=[Stat.from_dict(stat_data) for stat_data in sheet_dict["stats"]],
            note_list=[Note.from_dict(note_data) for note_data in sheet_dict["notes"]],
            card_list=[Card.from_dict(card_data) for card_data in sheet_dict["cards"]],
        )

    def to_dict(self) -> dict[str, Any]:
        """
        Converts the values to a dict.
        :return: Dict containing sheet values
        """
        return {
            "stats": [stat.to_dict() for stat in self.stat_list],
            "notes": [note.to_dict() for note in self.note_list],
            "cards": [card.to_dict() for card in self.card_list],
        }

    def to_json(self, json_path: Path) -> None:
        """
        Converts the sheet object to a JSON file.
        :param json_path: The path to the JSON file
        """
        with open(json_path, "w", encoding="utf-8") as json_file:
            json.dump(self.to_dict(), json_file, ensure_ascii=False, indent=4)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Sheet):
            return NotImplemented
        return (
            self.stat_list == other.stat_list
            and self.note_list == other.note_list
            and self.card_list == other.card_list
        )
