from typing import Any
from src.model.Stat import Stat


class TestStat:

    def test_from_dict_valid(self):
        """Tests that valid dictionaries are converted to Stat objects correctly."""
        dicts_list: list[dict[str, Any]] = [
            {"name": "Test Stat1", "value": 10},
            {"name": "Test Stat2", "value": 5, "max": 15},
            {"name": "Test Stat3", "value": 8, "min": 5},
            {"name": "Test Stat4", "value": 20, "max": 25, "min": 10},
            {
                "name": "Test Stat5",
                "value": 12,
                "history": [("Increased by 2", "+2")],
            },
            {
                "name": "Test Stat6",
                "value": 18,
                "max": 20,
                "min": 10,
                "history": [("Created", "+18"), ("Updated", "+0")],
            },
        ]
        expected_stat_list: list[Stat] = [
            Stat(name="Test Stat1", value=10),
            Stat(name="Test Stat2", value=5, max_value=15),
            Stat(name="Test Stat3", value=8, min_value=5),
            Stat(name="Test Stat4", value=20, max_value=25, min_value=10),
            Stat(name="Test Stat5", value=12),
            Stat(name="Test Stat6", value=18, max_value=20, min_value=10),
        ]

        # Set history for Test Stat5 and Test Stat6
        expected_stat_list[4].history = [("Increased by 2", "+2")]
        expected_stat_list[5].history = [("Created", "+18"), ("Updated", "+0")]

        for stat_dict, expected_stat in zip(dicts_list, expected_stat_list):
            actual_stat: Stat = Stat.from_dict(stat_dict)
            assert expected_stat == actual_stat

    def test_from_dict_invalid(self):
        """Tests that invalid dictionaries return None."""
        invalid_dict_list: list[dict[str, Any]] = [
            {},  # Missing required name and value
            {"name": "Invalid Stat1"},  # Missing required value
            {"value": 10},  # Missing required name
        ]

        for invalid_dict in invalid_dict_list:
            assert Stat.from_dict(invalid_dict) is None

    def test_to_dict_valid(self):
        """Tests that Stat objects are converted to dictionaries correctly."""
        expected_dict_list: list[dict[str, Any]] = [
            {"name": "Test Stat1", "value": 10},
            {"name": "Test Stat2", "value": 5, "max": 15},
            {"name": "Test Stat3", "value": 8, "min": 5},
            {"name": "Test Stat4", "value": 20, "max": 25, "min": 10},
            {
                "name": "Test Stat5",
                "value": 12,
                "history": [("Increased by 2", "+2")],
            },
            {
                "name": "Test Stat6",
                "value": 18,
                "max": 20,
                "min": 10,
                "history": [("Created", "+18"), ("Updated", "+0")],
            },
        ]
        stat_list: list[Stat] = [
            Stat(name="Test Stat1", value=10),
            Stat(name="Test Stat2", value=5, max_value=15),
            Stat(name="Test Stat3", value=8, min_value=5),
            Stat(name="Test Stat4", value=20, max_value=25, min_value=10),
            Stat(name="Test Stat5", value=12),
            Stat(name="Test Stat6", value=18, max_value=20, min_value=10),
        ]

        # Set history for Test Stat5 and Test Stat6
        stat_list[4].history = [("Increased by 2", "+2")]
        stat_list[5].history = [("Created", "+18"), ("Updated", "+0")]

        for expected_dict, stat in zip(expected_dict_list, stat_list):
            actual_dict: dict[str, Any] = stat.to_dict()
            assert expected_dict == actual_dict
