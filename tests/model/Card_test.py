from typing import Any
import pytest
from src.model.Card import Card
from src import CardType


class TestCard:

    def test_from_dict_valid(self):
        """Tests that valid dictionaries are converted to Card objects correctly."""
        dicts_list: list[str] = [
            {"name": "Test Card1", "card_type": 1},
            {"name": "Test Card2", "card_type": 0, "column": 5},
            {"name": "Test Card3", "card_type": 1, "row": 3},
            {"name": "Test Card4", "card_type": 0, "column_span": 2},
            {"name": "Test Card5", "card_type": 1, "row_span": 4},
            {
                "name": "Test Card6",
                "card_type": 0,
                "column": 1,
                "row": 2,
                "column_span": 3,
                "row_span": 2,
            },
        ]
        expected_card_list: list[Card] = [
            Card(name="Test Card1", card_type=CardType(1)),
            Card(name="Test Card2", card_type=CardType(0), column=5),
            Card(name="Test Card3", card_type=CardType(1), row=3),
            Card(name="Test Card4", card_type=CardType(0), column_span=2),
            Card(name="Test Card5", card_type=CardType(1), row_span=4),
            Card(
                name="Test Card6",
                card_type=CardType(0),
                column=1,
                row=2,
                column_span=3,
                row_span=2,
            ),
        ]

        for card_dict, expected_card in zip(dicts_list, expected_card_list):
            actual_card: Card = Card.from_dict(card_dict)
            assert expected_card == actual_card

    def test_from_dict_invalid(self):
        """Tests that invalid dictionaries return None."""
        invalid_dict_list: list[dict[str, Any]] = [
            {},  # Missing required name and card_type
            {"name": "Invalid Card1"},  # Missing required card_type
            {"card_type": 0},  # Missing required name
        ]

        for invalid_dict in invalid_dict_list:
            assert Card.from_dict(invalid_dict) is None

    def test_to_dict_valid(self):
        """Tests that Card objects are converted to dictionaries correctly."""
        expected_dict_list: list[str] = [
            {"name": "Test Card1", "card_type": 1},
            {"name": "Test Card2", "card_type": 0, "column": 5},
            {"name": "Test Card3", "card_type": 1, "row": 3},
            {"name": "Test Card4", "card_type": 0, "column_span": 2},
            {"name": "Test Card5", "card_type": 1, "row_span": 4},
            {
                "name": "Test Card6",
                "card_type": 0,
                "column": 1,
                "row": 2,
                "column_span": 3,
                "row_span": 2,
            },
        ]
        card_list: list[Card] = [
            Card(name="Test Card1", card_type=CardType(1)),
            Card(name="Test Card2", card_type=CardType(0), column=5),
            Card(name="Test Card3", card_type=CardType(1), row=3),
            Card(name="Test Card4", card_type=CardType(0), column_span=2),
            Card(name="Test Card5", card_type=CardType(1), row_span=4),
            Card(
                name="Test Card6",
                card_type=CardType(0),
                column=1,
                row=2,
                column_span=3,
                row_span=2,
            ),
        ]

        for expected_dict, card in zip(expected_dict_list, card_list):
            actual_dict: dict[str, Any] = card.to_dict()
            assert expected_dict == actual_dict
