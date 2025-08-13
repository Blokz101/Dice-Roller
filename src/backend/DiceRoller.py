import random

class DiceRoller:

    @staticmethod
    def get_rolls(num_dice, dice_value):
        results = []
        for i in range(0, num_dice):
            results.append(random.randint(1, dice_value))
        
        return results


    
def main():
    print(DiceRoller.get_rolls(10, 4))
        
if __name__ == "__main__":
    main()