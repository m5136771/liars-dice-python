# game played in pirates of the caribbean

# ---Materials---

# GOAL:DONE create 1 player and 2-3 bots
# Google: python create variable
player1 = "player1"
bot1 = "bot1"
bot2 = "bot2"
bot3 = "bot3"

# GOAL: create 5d6 per player
# Google: python variable range of values
""" for i in range(6):
    print(i) """

""" for i in range(6):
    die = (i+1) """

#i+1 = 1-6

""" for i in range(6):
    print(i+1) """

# Google: pyton set for loop variable
""" one, two, three = range(1, 4)
print(one, two, three) """

# this gives us multiple variables with one number each
# but we want one variable with multiple numbers
# Google: python one variable with multiple numbers
""" a = 1, 2, 3, 4, 5, 6

print(a) """

#die = 1, 2, 3, 4, 5, 6
# now I need five of these for each player
# Google: python give variable to another variable

""" spam = 42
cheese = spam
spam = 100
print(spam) """
# so variables can be continually reassgined and will hold most recent assignment
# but is cheese = spam working?

""" spam = 42
cheese = spam
print(cheese) """
# Yes! it is! So I can do..
""" die1 = 1, 2, 3, 4, 5, 6
die2 = 1, 2, 3, 4, 5, 6
die3 = 1, 2, 3, 4, 5, 6
die4 = 1, 2, 3, 4, 5, 6
die5 = 1, 2, 3, 4, 5, 6 """
""" player1Dice = die1, die2, die3, die4, die5, die5
bot1Dice = die1, die2, die3, die4, die5, die5
bot2Dice = die1, die2, die3, die4, die5, die5
bot3Dice = die1, die2, die3, die4, die5, die5 """
# print(bot2Dice)

# But I just realized... we don't want everyone to have the same dice, they need their own
# do I have to make variables all the way up to die20 then? That would work...
# Google: python make lots of variables
# Google: python dictionaries
""" thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964,
  "year": 2020
}
print(thisdict) """
# so let me make a die like this

""" die1 = {
  "values": 1, 2, 3, 4, 5, 6,

}
print(thisdict) """
# hm, but that's giving an error
# Google: python dictionary one key multiple values
""" die1 = {
    "values": [1, 2, 3, 4, 5, 6],
}
print(die1) """
# it worked! so can I make multiple dice in the same line like before?

""" die1, die2, die3, die4, die5 = {
    "values": [1, 2, 3, 4, 5, 6],
}
print(die3) """
# ValueError: not enough values to unpack (expected 5, got 1)
# so it sounds like it wants a value for each of the variables.
# I guess that is the same as before. I forgot. So let's try...

""" die1, die2, die3, die4, die5 = {
    "values": [1, 2, 3, 4, 5, 6],
    "values": [1, 2, 3, 4, 5, 6],
    "values": [1, 2, 3, 4, 5, 6],
    "values": [1, 2, 3, 4, 5, 6],
    "values": [1, 2, 3, 4, 5, 6],
}
print(die3) """
# ValueError: not enough values to unpack (expected 5, got 1)
# hm.. so.. is it because I gave every key the same name?

""" die1, die2, die3, die4, die5 = {
    'valuesDie1': [1, 2, 3, 4, 5, 6],
    'valuesDie2': [1, 2, 3, 4, 5, 6],
    "valuesDie3": [1, 2, 3, 4, 5, 6],
    "valuesDie4": [1, 2, 3, 4, 5, 6],
    "valuesDie5": [1, 2, 3, 4, 5, 6],
} """
# print(die3)
# Got it!!
# just to make sure..

# print(die1, die2, die3, die4, die5)
# line 56, in <module> player1Dice = die1, die2, die3, die4, die5, die5 NameError: name 'die1' is not defined. Did you mean: 'die'?
# ohh because I'm defining die1 now but tried to use it earlier..
# I'll just go comment that out and try again

#print(die1, die2, die3, die4, die5)
# Well that fixed that! But now..
# It's giving me the name of each, but not the numbers..
# how do I access the numbers?
# Google: python access numbers in dictionary

#print(dict.values())
#TypeError: unbound method dict.values() needs an argument
# keep reading

""" player_data = {"Ronaldo": 7, "Messi": 10, "Bale": 9}
values = player_data.values() """
# so the name of my dictionary is 'die1'
# I want to do something like..

""" values = die1.values()
print(values) """
# AttributeError: 'str' object has no attribute 'values'
# Ah.. because the values are named something else. Let's try..

""" values = die1.valuesDie1()
print(values) """
# AttributeError: 'str' object has no attribute 'valuesDie1'
# keep reading
# maybe try this..
# dict.get(key)
# which would look like.. 

""" die1.get(valuesDie1)
print(valuesDie1) """
# but my syntax says valuesDie1 is undefined..
# what if I add quotes?

""" die1.get('valuesDie1')
print('valuesDie1') """
# AttributeError: 'str' object has no attribute 'get'
# nope.. what if the key values shouldn't have quotes?
# nope.. syntax says that's wrong. so..
# step back, what's the problem? 
# I want to read the number values stored within one key which is attached to a variable.
# Is the key assigned to the variable like I think?

#print(die1, die2, die3)
# yeah, they are. ok, so..
# if printing die1 = 'valuesDie1', then that's the value of die1
# what I really want is the value of that value.
# how do I read the value of 'valuesDie1' which is assigned to the variable die1?
# Google: python read value of key in variable
# found an example, let's alter it

""" # Initialize dictionary
die1 = {'valuesDie1' : 1}
  
# printing original dictionary
print("The original dictionary : " +  str(die1))
  
# Using items()
# Extracting key-value of dictionary in variables
# key, val = die1.items()[0]
  
# printing result  """
""" print("The 1st key of dictionary is : " + str(key))
print("The 1st value of dictionary is : " + str(val)) """
# TypeError: 'dict_items' object is not subscriptable
# Google: TypeError: 'dict_items' object is not subscriptable
# To solve the error, convert the dict_items object to a list, before accessing an index, e.g. list(my_dict. items())[0]

""" key, val= list(die1. items())[0]
print("The 1st key of dictionary is : " + str(key))
print("The 1st value of dictionary is : " + str(val)) """
# Yes! Got it! Ok.. now what was I trying to accomplish?
# Line 12: # GOAL: DONE create 5d6 per player
# wow.. well we've learned a lot. let's start over now using all we know
# the dictionary seemed helpful if I needed a name for each set of values, but I don't.. so why not just make a simple list without naming it?

# first make a die with list of values
die = [1, 2, 3, 4, 5, 6]

# now make a cup with 5 dice, which is a list of all the dice
# diceCup = [die]

# can I duplicate variables somehow?
# Google: python use same values in variable for several more variables
# use 'consecutively'

die1 = die2 = die3 = die4 = die5= die # die is at end because it's the 'value' we're assigning. put it at the front and see what happens
diceCup = [die1, die2, die3, die4, die5]
# print(diceCup)
# Got it! Now give a set to each player

playerDiceCup = diceCup # not redefining diceCup, creating a new var and giving it the same value
bot1DiceCup = bot2DiceCup = bot3DiceCup = diceCup
# print(bot2DiceCup, playerDiceCup)
# Beautiful! Ok.. what's next?


# GOAL: DONE 1 dice cup for each player
# GOAL: thinking about it.. the dice cup will eventually be used to do stuff with the dice, so we should have a function for it
# Google: python functions

def dice_cup_function():
  print("Hello from a function")

dice_cup_function()
# It worked! ok.. so let's just leave this here for now. We have a dice cup made.
# Side note.. I also just learned the proper convention for naming variables in python, so I'll use that going forward.


# OK! We have our players, our dice, and our dice cups. Let's play!


# 1. players roll 2 dice to determine turn order
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

print()