from typing import Any
from src.model.Note import Note


class TestNote:

    def test_from_dict_valid(self):
        """Tests that valid dictionaries are converted to Note objects correctly."""
        dicts_list: list[dict[str, Any]] = [
            {"name": "Test Note1", "text": "Simple note text"},
            {"name": "Test Note2", "text": ""},
            {"name": "Test Note3", "text": "Multi-line\nnote text"},
            {"name": "Test Note4", "text": "Note with special chars: !@#$%^&*()"},
        ]
        expected_note_list: list[Note] = [
            Note(name="Test Note1", raw_text="Simple note text"),
            Note(name="Test Note2", raw_text=""),
            Note(name="Test Note3", raw_text="Multi-line\nnote text"),
            Note(name="Test Note4", raw_text="Note with special chars: !@#$%^&*()"),
        ]

        for note_dict, expected_note in zip(dicts_list, expected_note_list):
            actual_note: Note = Note.from_dict(note_dict)
            assert expected_note == actual_note

    def test_from_dict_invalid(self):
        """Tests that invalid dictionaries return None."""
        invalid_dict_list: list[dict[str, Any]] = [
            {},  # Missing required name and text
            {"name": "Invalid Note1"},  # Missing required text
            {"text": "Some text"},  # Missing required name
        ]

        for invalid_dict in invalid_dict_list:
            assert Note.from_dict(invalid_dict) is None

    def test_to_dict_valid(self):
        """Tests that Note objects are converted to dictionaries correctly."""
        expected_dict_list: list[dict[str, Any]] = [
            {"name": "Test Note1", "text": "Simple note text"},
            {"name": "Test Note2", "text": ""},
            {"name": "Test Note3", "text": "Multi-line\nnote text"},
            {"name": "Test Note4", "text": "Note with special chars: !@#$%^&*()"},
        ]
        note_list: list[Note] = [
            Note(name="Test Note1", raw_text="Simple note text"),
            Note(name="Test Note2", raw_text=""),
            Note(name="Test Note3", raw_text="Multi-line\nnote text"),
            Note(name="Test Note4", raw_text="Note with special chars: !@#$%^&*()"),
        ]

        for expected_dict, note in zip(expected_dict_list, note_list):
            actual_dict: dict[str, Any] = note.to_dict()
            assert expected_dict == actual_dict

    def test_assign(self) -> None:
        """Test the assign function."""
        # Create initial note
        actual_note: Note = Note(
            name="STAY STILL",
            raw_text="Source: Player's Handbook\n2nd-level enchantment\n\nCasting Time: 1 action\nRange: 60 feet\nComponents: V, S, M (a small, straight piece of iron)\nDuration: Concentration, up to 1 minute\n\nChoose a humanoid that you can see within range. The target must succeed on a Wisdom saving throw or be paralyzed for the duration. At the end of each of its turns, the target can make another Wisdom saving throw. On a success, the spell ends on the target.\n\nAt Higher Levels. When you cast this spell using a spell slot of 3rd level or higher, you can target one additional humanoid for each slot level above 2nd. The humanoids must be within 30 feet of each other when you target them.\n\nSpell Lists. Bard, Cleric, Druid, Sorcerer, Warlock, Wizard"
        )
        actual_note.parse_raw_text()
        
        # Create expected note with different values
        expected_note: Note = Note(
            name="BURNNN",
            raw_text="Source: Player's Handbook\n\nEvocation cantrip\n\nCasting Time: 1 action\nRange: 120 feet\nComponents: V, S\nDuration: Instantaneous\n\nYou hurl a mote of fire at a creature or object within range. Make a ranged spell attack against the target. On a hit, the target takes 1d10 fire damage. A flammable object hit by this spell ignites if it isn’t being worn or carried.\n\nAt Higher Levels. This spell’s damage increases by 1d10 when you reach 5th level (2d10), 11th level (3d10), and 17th level (4d10).\n\nSpell Lists. Artificer, Sorcerer, Wizard"
        )
        expected_note.parse_raw_text()
        
        # Test assign
        actual_note.assign(expected_note)
        assert actual_note == expected_note