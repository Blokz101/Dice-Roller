from typing import Any
from src.model.Note import Note


class TestNote:

    def test_from_dict_valid(self):
        """Tests that valid dictionaries are converted to Note objects correctly."""
        dicts_list: list[dict[str, Any]] = [
            {"name": "Test Note1", "card_type": 1, "text": "Simple note text"},
            {
                "name": "Test Note2",
                "card_type": 1,
                "text": "Note with column",
                "column": 5,
            },
            {"name": "Test Note3", "card_type": 1, "text": "Note with row", "row": 3},
            {"name": "Test Note4", "card_type": 1, "text": "", "column_span": 2},
            {
                "name": "Test Note5",
                "card_type": 1,
                "text": "Multi-line\nnote text",
                "row_span": 4,
            },
            {
                "name": "Test Note6",
                "card_type": 1,
                "text": "Complete note with all fields",
                "column": 1,
                "row": 2,
                "column_span": 3,
                "row_span": 2,
            },
        ]
        expected_note_list: list[Note] = [
            Note(name="Test Note1", raw_text="Simple note text"),
            Note(name="Test Note2", raw_text="Note with column", column=5),
            Note(name="Test Note3", raw_text="Note with row", row=3),
            Note(name="Test Note4", raw_text="", column_span=2),
            Note(name="Test Note5", raw_text="Multi-line\nnote text", row_span=4),
            Note(
                name="Test Note6",
                raw_text="Complete note with all fields",
                column=1,
                row=2,
                column_span=3,
                row_span=2,
            ),
        ]

        for note_dict, expected_note in zip(dicts_list, expected_note_list):
            actual_note: Note = Note.from_dict(note_dict)
            assert expected_note == actual_note

    def test_from_dict_invalid(self):
        """Tests that invalid dictionaries return None."""
        invalid_dict_list: list[dict[str, Any]] = [
            {},  # Missing required name, card_type, and text
            {"name": "Invalid Note1"},  # Missing required card_type and text
            {"card_type": 1},  # Missing required name and text
            {"name": "Invalid Note2", "card_type": 1},  # Missing required text
            {
                "name": "Invalid Note3",
                "text": "Some text",
            },  # Missing required card_type
        ]

        for invalid_dict in invalid_dict_list:
            assert Note.from_dict(invalid_dict) is None

    def test_to_dict_valid(self):
        """Tests that Note objects are converted to dictionaries correctly."""
        expected_dict_list: list[dict[str, Any]] = [
            {"name": "Test Note1", "card_type": 1, "text": "Simple note text"},
            {
                "name": "Test Note2",
                "card_type": 1,
                "text": "Note with column",
                "column": 5,
            },
            {"name": "Test Note3", "card_type": 1, "text": "Note with row", "row": 3},
            {"name": "Test Note4", "card_type": 1, "text": "", "column_span": 2},
            {
                "name": "Test Note5",
                "card_type": 1,
                "text": "Multi-line\nnote text",
                "row_span": 4,
            },
            {
                "name": "Test Note6",
                "card_type": 1,
                "text": "Complete note with all fields",
                "column": 1,
                "row": 2,
                "column_span": 3,
                "row_span": 2,
            },
        ]
        note_list: list[Note] = [
            Note(name="Test Note1", raw_text="Simple note text"),
            Note(name="Test Note2", raw_text="Note with column", column=5),
            Note(name="Test Note3", raw_text="Note with row", row=3),
            Note(name="Test Note4", raw_text="", column_span=2),
            Note(name="Test Note5", raw_text="Multi-line\nnote text", row_span=4),
            Note(
                name="Test Note6",
                raw_text="Complete note with all fields",
                column=1,
                row=2,
                column_span=3,
                row_span=2,
            ),
        ]

        for expected_dict, note in zip(expected_dict_list, note_list):
            actual_dict: dict[str, Any] = note.to_dict()
            assert expected_dict == actual_dict
