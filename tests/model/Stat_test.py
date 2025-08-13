from typing import Any
from src.model.Stat import Stat


class TestStat:

    def test_from_dict_valid(self):
        """Tests that valid dictionaries are converted to Stat objects correctly."""
        dicts_list: list[dict[str, Any]] = [
            {"name": "Test Stat1", "card_type": 0, "value": 10},
            {"name": "Test Stat2", "card_type": 0, "value": 5, "column": 3},
            {"name": "Test Stat3", "card_type": 0, "value": 15, "row": 2},
            {"name": "Test Stat4", "card_type": 0, "value": 20, "max": 25},
            {"name": "Test Stat5", "card_type": 0, "value": 8, "min": 5},
            {
                "name": "Test Stat6",
                "card_type": 0,
                "value": 12,
                "history": [("2025-01-01", "+2")],
            },
            {
                "name": "Test Stat7",
                "card_type": 0,
                "value": 18,
                "max": 20,
                "min": 10,
                "column": 1,
                "row": 2,
                "column_span": 2,
                "row_span": 1,
                "history": [("2025-01-01", "+5"), ("2025-01-02", "+10")],
            },
        ]
        expected_stat_list: list[Stat] = [
            Stat(name="Test Stat1", initial_value=10),
            Stat(name="Test Stat2", initial_value=5, column=3),
            Stat(name="Test Stat3", initial_value=15, row=2),
            Stat(name="Test Stat4", initial_value=20, max_value=25),
            Stat(name="Test Stat5", initial_value=8, min_value=5),
            Stat(name="Test Stat6", initial_value=12),
            Stat(
                name="Test Stat7",
                initial_value=18,
                max_value=20,
                min_value=10,
                column=1,
                row=2,
                column_span=2,
                row_span=1,
            ),
        ]

        # Set history for Test Stat6 and Test Stat7
        expected_stat_list[5].history = [("2025-01-01", "+2")]
        expected_stat_list[6].history = [
            ("2025-01-01", "+5"),
            ("2025-01-02", "+10"),
        ]

        for stat_dict, expected_stat in zip(dicts_list, expected_stat_list):
            actual_stat: Stat = Stat.from_dict(stat_dict)
            assert expected_stat == actual_stat

    def test_from_dict_invalid(self):
        """Tests that invalid dictionaries return None."""
        invalid_dict_list: list[dict[str, Any]] = [
            {},  # Missing required name, card_type, and value
            {"name": "Invalid Stat1"},  # Missing required card_type and value
            {"card_type": 0},  # Missing required name and value
            {"name": "Invalid Stat2", "card_type": 0},  # Missing required value
            {"name": "Invalid Stat3", "value": 10},  # Missing required card_type
        ]

        for invalid_dict in invalid_dict_list:
            assert Stat.from_dict(invalid_dict) is None

    def test_to_dict_valid(self):
        """Tests that Stat objects are converted to dictionaries correctly."""
        expected_dict_list: list[dict[str, Any]] = [
            {"name": "Test Stat1", "card_type": 0, "value": 10},
            {"name": "Test Stat2", "card_type": 0, "value": 5, "column": 3},
            {"name": "Test Stat3", "card_type": 0, "value": 15, "row": 2},
            {"name": "Test Stat4", "card_type": 0, "value": 20, "max": 25},
            {"name": "Test Stat5", "card_type": 0, "value": 8, "min": 5},
            {
                "name": "Test Stat6",
                "card_type": 0,
                "value": 12,
                "history": [("2025-01-01", "+2")],
            },
            {
                "name": "Test Stat7",
                "card_type": 0,
                "value": 18,
                "max": 20,
                "min": 10,
                "column": 1,
                "row": 2,
                "column_span": 2,
                "row_span": 1,
                "history": [("2025-01-01", "+5"), ("2025-01-02", "+10")],
            },
        ]
        stat_list: list[Stat] = [
            Stat(name="Test Stat1", initial_value=10),
            Stat(name="Test Stat2", initial_value=5, column=3),
            Stat(name="Test Stat3", initial_value=15, row=2),
            Stat(name="Test Stat4", initial_value=20, max_value=25),
            Stat(name="Test Stat5", initial_value=8, min_value=5),
            Stat(name="Test Stat6", initial_value=12),
            Stat(
                name="Test Stat7",
                initial_value=18,
                max_value=20,
                min_value=10,
                column=1,
                row=2,
                column_span=2,
                row_span=1,
            ),
        ]

        # Set history for Test Stat6 and Test Stat7
        stat_list[5].history = [("2025-01-01", "+2")]
        stat_list[6].history = [
            ("2025-01-01", "+5"),
            ("2025-01-02", "+10"),
        ]

        for expected_dict, stat in zip(expected_dict_list, stat_list):
            actual_dict: dict[str, Any] = stat.to_dict()
            assert expected_dict == actual_dict
