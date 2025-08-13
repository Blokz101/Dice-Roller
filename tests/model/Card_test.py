from src.model.Card import Card
from src import CardType


class TestCard:

    def test_from_dict_valid(self):
        dicts_list: list[str] = [
            {"name": "Test Card1", "card_type": 1},
        ]
        expected_card_list: list[Card] = [
            Card(name="Test Card1", card_type=CardType(1)),
        ]

        for card_dict, expected_card in zip(dicts_list, expected_card_list):
            card: Card = Card.from_dict(card_dict)
            assert expected_card == card
