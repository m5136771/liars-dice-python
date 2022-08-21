# Create players.
from random import randrange


class Player:
  def __init__(self, name, roll_result):
    self.name = name
    self.dice_cup = 0

# Give each a name and an empty dice_cup.
p1 = Player("enter name", 0)
b1 = Player("Bot 1", 0)
b2 = Player("Bot 2", 0)
b3 = Player("Bot 3", 0)

# Fill players' dice cups and let them roll.
def roll_dice():
    roll_result = randrange(1,7,1)
    return roll_result

x = roll_dice()
print(x)



# Start Game
#------------------------------------------------------------------------------

# 1. players roll 2 dice to determine turn order

def roll_for_turn():
    roll_result = randrange(1,7,1)
    print(roll_result)

roll_dice()

# 2. all players roll dice (get 5 values of 1-6)
# 3. player1 bids (choose a value, choose a quantity ex: five 2s)
# 4. next player chooses: A. raise quantity | B. Challenge bid
# A player may bid a higher quantity of the same face or the same quantity of a higher face.
# 5a. next player takes turn, repeat ^4.
# 
# 5b. IF challenge, THEN all players reveal dice
# GAME: count quantity of each value
# 
#
# 6b. IF bid matched or exceeded, bidding player wins ELSE challenging player wins
# 
# Cleanup. IF bidding player loses, remove 1d6
# New Round. losing player plays first 