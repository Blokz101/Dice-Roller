import random
from typing import Optional
class DiceRoll:


    @staticmethod
    def get_rolls(num_dice, dice_value):
        results = []
        for i in range(0, num_dice):
            results.append(random.randint(1, dice_value))
        
        return results

    def __init__(self, num_dice: int, dice_value: int, dmg_type: str, keep_highest: int, keep_lowest: int, modifiers: Optional[list[int]]):
        
        self.num_dice = num_dice
        self.dice_value = dice_value
        self.dmg_type = dmg_type
        self.keep_highest = keep_highest
        self.keep_lowest = keep_lowest
        self.modifiers = modifiers

        self.rolls = DiceRoll.get_rolls(num_dice, dice_value)
        self.result = 0

        for i in self.rolls:
            self.result += i

        for i in self.modifiers:
            self.result += i
        
        


    


    
def main():
    print(DiceRoll.get_rolls(10, 4))
        
if __name__ == "__main__":
    main()