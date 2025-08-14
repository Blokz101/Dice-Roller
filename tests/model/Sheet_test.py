import pytest
from typing import Any
from src.model.Sheet import Sheet
from src.model.Card import Card, StatConfig
from src.model.Stat import Stat
from src.model.Note import Note
from src import CardType
from tests import SAMPLE1_JSON_PATH


class TestSheet:

    def test_from_json_with_sample1(self) -> None:
        # Create expected stats from the sample JSON
        expected_stats = [
            Stat(name="Strength", value=10),
            Stat(name="Dexterity", value=19),
            Stat(name="Constitution", value=13),
            Stat(name="Intelligence", value=17),
            Stat(name="Wisdom", value=11),
            Stat(name="Charisma", value=9),
            Stat(name="Arrows", value=45),
        ]

        # Set history for stats that have it
        expected_stats[0].history = [("Initial", "10"), ("Level One", "11")]
        expected_stats[1].history = [("Initial", "10"), ("Level Two", "19")]
        expected_stats[2].history = [("Initial", "10"), ("Level One", "13")]
        expected_stats[3].history = [("Initial", "10"), ("Level One", "17")]
        expected_stats[4].history = [("Initial", "10"), ("Level One", "11")]
        expected_stats[5].history = [("Initial", "10"), ("Level One", "9")]

        # Create expected notes from the sample JSON
        expected_notes = [
            Note(
                name="FIREBALL",
                raw_text="Casting Time: 1 action\\nRange: 150 feet\\nComponents: V, S, M (a tiny ball of bat guano and sulfur)\\nDuration: Instantaneous\\n\\nA bright streak flashes from your pointing finger to a point you choose within range then blossoms with a low roar into an explosion of flame. Each creature in a 20-foot radius must make a Dexterity saving throw. A target takes 8d6 fire damage on a failed save, or half as much damage on a successful one. The fire spreads around corners. It ignites flammable objects in the area that aren't being worn or carried.\\n\\nAt Higher Levels. When you cast this spell using a spell slot of 4th level or higher, the damage increases by 1d6 for each slot level above 3rd.\\n\\nSpell Lists. Sorcerer, Wizard",
            )
        ]

        # Create expected cards from the sample JSON
        expected_cards = [
            Card(
                name="Core Stats",
                card_type=CardType.STAT,
                column=0,
                row=0,
                stat_names=[
                    "Strength",
                    "Dexterity",
                    "Constitution",
                    "Intelligence",
                    "Wisdom",
                    "Charisma",
                ],
                stat_configs={
                    "Strength": StatConfig(subtext="+0"),
                    "Dexterity": StatConfig(subtext="+4"),
                    "Constitution": StatConfig(subtext="+1"),
                    "Intelligence": StatConfig(subtext="+3"),
                    "Wisdom": StatConfig(subtext="+0"),
                    "Charisma": StatConfig(subtext="-1"),
                },
            ),
            Card(
                name="Ammunition",
                card_type=CardType.STAT,
                column=0,
                row=1,
                stat_names=["Arrows"],
                stat_configs={"Arrows": StatConfig(show_max=True, show_min=True)},
            ),
        ]

        expected_sheet: Sheet = Sheet(
            name="Tim the Schizophrenic Assassin",
            stat_list=expected_stats,
            note_list=expected_notes,
            card_list=expected_cards,
        )
        actual_sheet: Sheet = Sheet.from_json(SAMPLE1_JSON_PATH)

        assert expected_sheet == actual_sheet

    def test_to_dict_with_sample1(self):
        # Create expected stats from the sample JSON
        stats = [
            Stat(name="Strength", value=10),
            Stat(name="Dexterity", value=19),
            Stat(name="Constitution", value=13),
            Stat(name="Intelligence", value=17),
            Stat(name="Wisdom", value=11),
            Stat(name="Charisma", value=9),
            Stat(name="Arrows", value=45),
        ]

        # Set history for stats that have it
        stats[0].history = [("Initial", "10"), ("Level One", "11")]
        stats[1].history = [("Initial", "10"), ("Level Two", "19")]
        stats[2].history = [("Initial", "10"), ("Level One", "13")]
        stats[3].history = [("Initial", "10"), ("Level One", "17")]
        stats[4].history = [("Initial", "10"), ("Level One", "11")]
        stats[5].history = [("Initial", "10"), ("Level One", "9")]

        # Create expected notes from the sample JSON
        notes = [
            Note(
                name="FIREBALL",
                raw_text="Casting Time: 1 action\\nRange: 150 feet\\nComponents: V, S, M (a tiny ball of bat guano and sulfur)\\nDuration: Instantaneous\\n\\nA bright streak flashes from your pointing finger to a point you choose within range then blossoms with a low roar into an explosion of flame. Each creature in a 20-foot radius must make a Dexterity saving throw. A target takes 8d6 fire damage on a failed save, or half as much damage on a successful one. The fire spreads around corners. It ignites flammable objects in the area that aren't being worn or carried.\\n\\nAt Higher Levels. When you cast this spell using a spell slot of 4th level or higher, the damage increases by 1d6 for each slot level above 3rd.\\n\\nSpell Lists. Sorcerer, Wizard",
            )
        ]

        # Create expected cards from the sample JSON
        cards = [
            Card(
                name="Core Stats",
                card_type=CardType.STAT,
                column=0,
                row=0,
                stat_names=[
                    "Strength",
                    "Dexterity",
                    "Constitution",
                    "Intelligence",
                    "Wisdom",
                    "Charisma",
                ],
                stat_configs={
                    "Strength": StatConfig(subtext="+0"),
                    "Dexterity": StatConfig(subtext="+4"),
                    "Constitution": StatConfig(subtext="+1"),
                    "Intelligence": StatConfig(subtext="+3"),
                    "Wisdom": StatConfig(subtext="+0"),
                    "Charisma": StatConfig(subtext="-1"),
                },
            ),
            Card(
                name="Ammunition",
                card_type=CardType.STAT,
                column=0,
                row=1,
                stat_names=["Arrows"],
                stat_configs={"Arrows": StatConfig(show_max=True, show_min=True)},
            ),
        ]

        sheet: Sheet = Sheet(
            name="Tim the Schizophrenic Assassin",
            stat_list=stats,
            note_list=notes,
            card_list=cards,
        )

        expected_dict: dict[str, Any] = {
            "name": "Tim the Schizophrenic Assassin",
            "stats": [
                {
                    "name": "Strength",
                    "value": 10,
                    "history": [("Initial", "10"), ("Level One", "11")],
                },
                {
                    "name": "Dexterity",
                    "value": 19,
                    "history": [("Initial", "10"), ("Level Two", "19")],
                },
                {
                    "name": "Constitution",
                    "value": 13,
                    "history": [("Initial", "10"), ("Level One", "13")],
                },
                {
                    "name": "Intelligence",
                    "value": 17,
                    "history": [("Initial", "10"), ("Level One", "17")],
                },
                {
                    "name": "Wisdom",
                    "value": 11,
                    "history": [("Initial", "10"), ("Level One", "11")],
                },
                {
                    "name": "Charisma",
                    "value": 9,
                    "history": [("Initial", "10"), ("Level One", "9")],
                },
                {"name": "Arrows", "value": 45},
            ],
            "notes": [
                {
                    "name": "FIREBALL",
                    "text": "Casting Time: 1 action\\nRange: 150 feet\\nComponents: V, S, M (a tiny ball of bat guano and sulfur)\\nDuration: Instantaneous\\n\\nA bright streak flashes from your pointing finger to a point you choose within range then blossoms with a low roar into an explosion of flame. Each creature in a 20-foot radius must make a Dexterity saving throw. A target takes 8d6 fire damage on a failed save, or half as much damage on a successful one. The fire spreads around corners. It ignites flammable objects in the area that aren't being worn or carried.\\n\\nAt Higher Levels. When you cast this spell using a spell slot of 4th level or higher, the damage increases by 1d6 for each slot level above 3rd.\\n\\nSpell Lists. Sorcerer, Wizard",
                }
            ],
            "cards": [
                {
                    "name": "Core Stats",
                    "card_type": 0,
                    "column": 0,
                    "row": 0,
                    "stat_names": [
                        "Strength",
                        "Dexterity",
                        "Constitution",
                        "Intelligence",
                        "Wisdom",
                        "Charisma",
                    ],
                    "stat_configs": {
                        "Strength": {"subtext": "+0"},
                        "Dexterity": {"subtext": "+4"},
                        "Constitution": {"subtext": "+1"},
                        "Intelligence": {"subtext": "+3"},
                        "Wisdom": {"subtext": "+0"},
                        "Charisma": {"subtext": "-1"},
                    },
                },
                {
                    "name": "Ammunition",
                    "card_type": 0,
                    "column": 0,
                    "row": 1,
                    "stat_names": ["Arrows"],
                    "stat_configs": {"Arrows": {"show_max": True, "show_min": True}},
                },
            ],
        }

        assert expected_dict == sheet.to_dict()

    def test_sheet_name_default(self) -> None:
        """Test that a Sheet gets a default name when none is provided."""
        sheet = Sheet()
        assert sheet.name == "New Sheet"

    def test_sheet_name_assignment(self) -> None:
        """Test that a Sheet can be created with a custom name."""
        custom_name = "My Custom Sheet"
        sheet = Sheet(name=custom_name)
        assert sheet.name == custom_name

    def test_sheet_name_in_to_dict(self) -> None:
        """Test that the name is included in the to_dict output."""
        custom_name = "Test Sheet Name"
        sheet = Sheet(name=custom_name)
        result = sheet.to_dict()
        assert "name" in result
        assert result["name"] == custom_name

    def test_sheet_name_from_dict(self) -> None:
        """Test that from_dict correctly parses the name field."""
        test_data = {
            "name": "Test Character Sheet",
            "stats": [],
            "notes": [],
            "cards": [],
        }
        sheet = Sheet.from_dict(test_data)
        assert sheet.name == "Test Character Sheet"

    def test_from_dict_missing_name_raises_error(self) -> None:
        """Test that from_dict raises an error when name is missing."""
        test_data = {"stats": [], "notes": [], "cards": []}
        with pytest.raises(ValueError, match="Input dict is missing required keys"):
            Sheet.from_dict(test_data)

    def test_from_dict_invalid_name_type_raises_error(self) -> None:
        """Test that from_dict raises an error when name is not a string."""
        test_data = {
            "name": 123,  # Should be string, not int
            "stats": [],
            "notes": [],
            "cards": [],
        }
        with pytest.raises(ValueError, match="Input dict has incorrect types for keys"):
            Sheet.from_dict(test_data)

    def test_sheet_equality_with_different_names(self) -> None:
        """Test that sheets with different names but identical content are not equal."""
        stats = [Stat(name="Test Stat", value=10)]
        sheet1 = Sheet(name="Sheet 1", stat_list=stats)
        sheet2 = Sheet(name="Sheet 2", stat_list=stats)
        assert sheet1 != sheet2

    def test_sheet_equality_with_same_names(self) -> None:
        """Test that sheets with same names and identical content are equal."""
        stats = [Stat(name="Test Stat", value=10)]
        sheet1 = Sheet(name="Same Name", stat_list=stats)
        sheet2 = Sheet(name="Same Name", stat_list=stats)
        assert sheet1 == sheet2
