from typing import Any, Optional
from src.model.Stat import Stat


class TestStat:

    def create_stat_data(self) -> list[Stat]:
        """Creates a list of stats for testing purposes."""
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
        
        return stat_list

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
                "history": [["Increased by 2", "+2"]],
            },
            {
                "name": "Test Stat6",
                "value": 18,
                "max": 20,
                "min": 10,
                "history": [["Created", "+18"], ["Updated", "+0"]],
            },
        ]

        expected_stat_list: list[Stat] = self.create_stat_data()

        for stat_dict, expected_stat in zip(dicts_list, expected_stat_list):
            actual_stat: Optional[Stat] = Stat.from_dict(stat_dict)
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
        stat_list: list[Stat] = self.create_stat_data()
        
        for expected_dict, stat in zip(expected_dict_list, stat_list):
            actual_dict: dict[str, Any] = stat.to_dict()
            assert expected_dict == actual_dict

    def test_set_value_unchanged_values(self) -> None:
        """Test the set_value function with values that have not changed."""
        expected_stat_list: list[Stat] = self.create_stat_data()
        actual_stat_list: list[Stat] = self.create_stat_data()

        for actual_stat in expected_stat_list:
            actual_stat.set_value(actual_stat.value)

        for actual_stat, expected_stat in zip(actual_stat_list, expected_stat_list):
            assert expected_stat == actual_stat

    def test_set_value_changed_values(self) -> None:
        """Test the set_value function with values that have changed."""
        expected_stat_list: list[Stat] = self.create_stat_data()
        actual_stat_list: list[Stat] = self.create_stat_data()

        new_stat_value_list: list[int] = [21, 43, 10, 0, 5, 12]

        for new_value, actual_stat, expected_stat in zip(new_stat_value_list, actual_stat_list, expected_stat_list):
            expected_stat.value = new_value
            expected_stat.history = []
            actual_stat.set_value(new_value)

        for actual_stat, expected_stat in zip(actual_stat_list, expected_stat_list):
            assert expected_stat == actual_stat
            
    def test_calculate_value(self):
        """Tests the calculate value function."""
        stat_history_list: list[list[tuple[str, str]]] = [
            [("test", "+3")],
            [("test1", "3"), ("test2", "*5")],
            [("test1", "+3"), ("test2", "+3*2")],
            [("test1", "-3"), ("test2", ""), ("test3", "-2")],
            [("test1", "+5"), ("test2", "/2")],
            [("test1", "+3"), ("test2", "-2"), ("test3", "=10")],
            [("test1", "+3"), ("test2", "-2"), ("test3", "=8"), ("test4", "*2+6")],
            [("test1", "+6-2"), ("test2", "*2-5")],
            [("test1", "+6-2"), ("test2", "fead")]
        ]
        expected_values: list[tuple[int, bool]] = [
            (0+3, True),
            (0+3*5, True),
            (0+3+3*2, True),
            (0-3-2, True),
            (0+int(5/2), True),
            (10, True),
            (8*2+6, True),
            ((6-2)*2-5, True),
            (0, False),
        ]

        for history, (expected_value, expected_return) in zip(stat_history_list, expected_values):
            stat: Stat = Stat("test_stat")
            stat.history = history
            assert expected_return == stat.calculate_value()
            assert expected_value == stat.value

    def test_assign(self) -> None:
        """Test the assign function."""
        # Create initial stat with some values
        actual_stat: Stat = Stat(
            name="Original Stat",
            value=10,
            max_value=20,
            min_value=5,
        )
        actual_stat.history = [("Initial", "10"), ("Level 1", "15")]
        
        # Create expected stat with different values
        expected_stat: Stat = Stat(
            name="Updated Stat",
            value=25,
            max_value=30,
            min_value=0,
        )
        expected_stat.history = [("Start", "5"), ("Mid", "15"), ("End", "25")]
        
        # Test assign
        actual_stat.assign(expected_stat)
        assert actual_stat == expected_stat