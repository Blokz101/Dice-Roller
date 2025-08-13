import pytest
from typing import Any
from src.model.Sheet import Sheet
from src.model.Stat import Stat
from src.model.Note import Note


class TestSheet:

    def test_from_dict_valid(self):
        """Tests that valid dictionaries are converted to Sheet objects."""
        dicts_list: list[dict[str, Any]] = [
            {
                "stats": [
                    {"name": "Strength", "value": 10},
                    {"name": "Agility", "value": 12, "max": 20, "min": 5},
                ],
                "notes": [
                    {"name": "Test Note", "text": "This is a test note."},
                ],
            },
        ]
        expected_sheet_list: list[Sheet] = [
            Sheet(
                stat_list=[
                    Stat(name="Strength", initial_value=10),
                    Stat(name="Agility", initial_value=12, max_value=20, min_value=5),
                ],
                note_list=[
                    Note(name="Test Note", raw_text="This is a test note."),
                ],
            ),
        ]

        for sheet_dict, expected_sheet in zip(dicts_list, expected_sheet_list):
            actual_sheet: dict[str, Any] = Sheet.from_dict(sheet_dict)
            assert expected_sheet == actual_sheet

    def test_to_dict_valid(self):
        """Test that Stat objects are converted to dictionaries correctly."""
        expected_dicts_list: list[dict[str, Any]] = [
            {
                "stats": [
                    {"name": "Strength", "value": 10},
                    {"name": "Agility", "value": 12, "max": 20, "min": 5},
                ],
                "notes": [
                    {"name": "Test Note", "text": "This is a test note."},
                ],
            },
        ]
        sheet_list: list[Sheet] = [
            Sheet(
                stat_list=[
                    Stat(name="Strength", initial_value=10),
                    Stat(name="Agility", initial_value=12, max_value=20, min_value=5),
                ],
                note_list=[
                    Note(name="Test Note", raw_text="This is a test note."),
                ],
            ),
        ]

        for expected_dict, sheet in zip(expected_dicts_list, sheet_list):
            actual_dict: dict[str, Any] = sheet.to_dict()
            assert expected_dict == actual_dict
