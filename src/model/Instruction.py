from src.model.DiceRoll import DiceRoll


class Instruction:

    def __init__(self, name: str = "", raw_str: str = ""):
        self.name: str = name
        self.raw_str: str = raw_str
        self.roll_list: list[DiceRoll] = []

    def construct_dice_rolls(self) -> None:
        """Parses the raw_str to populate self's rolls_list."""

    def total(self) -> int:
        pass
