from typing import Any
from src.model.Card import Card, StatConfig
from src import CardType


class TestCard:

    def test_from_dict_valid_stat_card(self):
        """Tests that valid dictionaries are converted to Stat Card objects correctly."""
        dicts_list: list[dict[str, Any]] = [
            {
                "name": "Test Stat Card1",
                "card_type": 0,
                "column": 1,
                "row": 2,
                "stat_names": ["Health", "Mana"],
            },
            {
                "name": "Test Stat Card2",
                "card_type": 0,
                "column": 3,
                "row": 4,
                "column_span": 2,
                "stat_names": ["Strength"],
                "stat_configs": {"Strength": {"show_max": True, "show_min": False}},
            },
        ]
        expected_card_list: list[Card] = [
            Card(
                name="Test Stat Card1",
                card_type=CardType.STAT,
                column=1,
                row=2,
                stat_names=["Health", "Mana"],
            ),
            Card(
                name="Test Stat Card2",
                card_type=CardType.STAT,
                column=3,
                row=4,
                column_span=2,
                stat_names=["Strength"],
                stat_configs={"Strength": StatConfig(show_max=True, show_min=False)},
            ),
        ]

        for card_dict, expected_card in zip(dicts_list, expected_card_list):
            actual_card: Card = Card.from_dict(card_dict)
            assert expected_card == actual_card

    def test_from_dict_valid_note_card(self):
        """Tests that valid dictionaries are converted to Note Card objects correctly."""
        dicts_list: list[dict[str, Any]] = [
            {
                "name": "Test Note Card1",
                "card_type": 1,
                "column": 2,
                "row": 3,
                "note_name": "My Note",
            },
            {
                "name": "Test Note Card2",
                "card_type": 1,
                "column": 0,
                "row": 0,
                "row_span": 2,
                "note_name": "Another Note",
            },
        ]
        expected_card_list: list[Card] = [
            Card(
                name="Test Note Card1",
                card_type=CardType.NOTE,
                column=2,
                row=3,
                note_name="My Note",
            ),
            Card(
                name="Test Note Card2",
                card_type=CardType.NOTE,
                column=0,
                row=0,
                row_span=2,
                note_name="Another Note",
            ),
        ]

        for card_dict, expected_card in zip(dicts_list, expected_card_list):
            actual_card: Card = Card.from_dict(card_dict)
            assert expected_card == actual_card

    def test_from_dict_invalid(self):
        """Tests that invalid dictionaries return None."""
        invalid_dict_list: list[dict[str, Any]] = [
            {},  # Missing all required fields
            {"name": "Invalid Card1"},  # Missing card_type, column, row
            {"name": "Invalid Card2", "card_type": 0},  # Missing column, row
            {"name": "Invalid Card3", "card_type": 0, "column": 1},  # Missing row
            {
                "name": "Invalid Card4",
                "card_type": 0,
                "column": 1,
                "row": 2,
            },  # Missing stat_names for STAT card
            {
                "name": "Invalid Card5",
                "card_type": 1,
                "column": 1,
                "row": 2,
            },  # Missing note_name for NOTE card
        ]

        for invalid_dict in invalid_dict_list:
            assert Card.from_dict(invalid_dict) is None

    def test_to_dict_valid_stat_card(self):
        """Tests that Stat Card objects are converted to dictionaries correctly."""
        expected_dict_list: list[dict[str, Any]] = [
            {
                "name": "Test Stat Card1",
                "card_type": 0,
                "column": 1,
                "row": 2,
                "stat_names": ["Health", "Mana"],
            },
            {
                "name": "Test Stat Card2",
                "card_type": 0,
                "column": 3,
                "row": 4,
                "column_span": 2,
                "stat_names": ["Strength"],
                "stat_configs": {
                    "Strength": {
                        "show_max": True,
                        "show_min": False,
                    }
                },
            },
        ]
        card_list: list[Card] = [
            Card(
                name="Test Stat Card1",
                card_type=CardType.STAT,
                column=1,
                row=2,
                stat_names=["Health", "Mana"],
            ),
            Card(
                name="Test Stat Card2",
                card_type=CardType.STAT,
                column=3,
                row=4,
                column_span=2,
                stat_names=["Strength"],
                stat_configs={"Strength": StatConfig(show_max=True, show_min=False)},
            ),
        ]

        for expected_dict, card in zip(expected_dict_list, card_list):
            actual_dict: dict[str, Any] = card.to_dict()
            assert expected_dict == actual_dict

    def test_to_dict_valid_note_card(self):
        """Tests that Note Card objects are converted to dictionaries correctly."""
        expected_dict_list: list[dict[str, Any]] = [
            {
                "name": "Test Note Card1",
                "card_type": 1,
                "column": 2,
                "row": 3,
                "note_name": "My Note",
            },
            {
                "name": "Test Note Card2",
                "card_type": 1,
                "column": 0,
                "row": 0,
                "row_span": 2,
                "note_name": "Another Note",
            },
        ]
        card_list: list[Card] = [
            Card(
                name="Test Note Card1",
                card_type=CardType.NOTE,
                column=2,
                row=3,
                note_name="My Note",
            ),
            Card(
                name="Test Note Card2",
                card_type=CardType.NOTE,
                column=0,
                row=0,
                row_span=2,
                note_name="Another Note",
            ),
        ]

        for expected_dict, card in zip(expected_dict_list, card_list):
            actual_dict: dict[str, Any] = card.to_dict()
            assert expected_dict == actual_dict
