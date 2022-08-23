from random import randrange
import random, sys, time

#---FUTURE FEATURES------------------------------------------------------------
# Make it type out die values
# fix grammar for 'one 1's'
# Add difficulty levels by making the bots more 'strategic'
# Allow for adjusting the number of bots in game
# Allow for multiple human players
# Add a GUI


# ---Information for Game------------------------------------------------------
# Create players.
class Player:
  def __init__(self, name, dice_cup, roll_total, bid_value, bid_quantity):
    self.name = name
    self.dice_cup = dice_cup
    self.roll_total = roll_total
    self.bid_value = bid_value
    self.bid_quantity = bid_quantity    

# Give each a name and an empty dice_cup.
p1 = Player("Player 1", [], 0, 0, 0)
b1 = Player("Bot 1", [], 0, 0, 0)
b2 = Player("Bot 2", [], 0, 0, 0)
b3 = Player("Bot 3", [], 0, 0, 0)

all_players = [p1, b1, b2, b3]
first_bid = None
current_player = None


# ---Helper Functions ---------------------------------------------------------
# Just for fun
typing_speed = 100 #wpm
def print_slow(t):
    for l in t:
        sys.stdout.write(l)
        sys.stdout.flush()
        time.sleep(random.random()*10.0/typing_speed)
    print('')

def print_slower(t):
    typing_speed = 50 #wpm
    for l in t:
        sys.stdout.write(l)
        sys.stdout.flush()
        time.sleep(random.random()*10.0/typing_speed)
    print('')

# Input Helpers
def die_value_input(message):
   try:
      value = int(input(message))
      if value > 6:
        return die_value_input('Yarr.. don\'t ye know the rules? A die only has 6 sides! Try again. A number between 1 and 6 this time!:\n')
      else:
        return value
   except:
      return die_value_input('What are ye sayin matey?? Choose a number between 1-6!\n')

def die_quantity_input(message):
   try:
      quantity = int(input(message))
      if quantity > dice_in_play:
        print('There aren\'t even that many dice! Be reasonable! The number of dice in play is', dice_in_play)
        return die_quantity_input('Try again!:\n')
      return quantity
   except:
      return die_quantity_input('What are you saying?? Choose a number!\n')

# Dice functions
# Init global variables
dice_in_play = 0

def count_dice():
    dice_total = 0
    for player in all_players:
        count = len(player.dice_cup)
        dice_total += count
    return dice_total

# Roll one die one time for a given player
def roll_once(player):
    dice_in_play = count_dice()
    roll_result = randrange(1,7,1)
    dice_in_play += 1
    player.dice_cup.insert(0, roll_result)

# Roll one die for a given player the amount of times specified
def roll(player, times):
    for _ in range(times):
        roll_once(player)

# Determine who goes first
def who_goes_first():
    highest_roller = None
    highest_roll = 0

    for player in all_players:
        roll(player, 2)
        player.roll_total = sum(player.dice_cup)
        print(player.name + ' rolls and gets ' + str(player.roll_total) + '...')
        #time.sleep(1)

        if player.roll_total > highest_roll & highest_roll !=0:
            highest_roll = player.roll_total
            highest_roller = player
            print(player.name + ' is now the highest roller!\n')
            #time.sleep(.5)

        elif player.roll_total > highest_roll:
            highest_roll = player.roll_total
            highest_roller = player
            print(player.name + ' is now the highest roller!\n')
            #time.sleep(.5)

        elif player.roll_total == 12:
            print('Wow! Two max rolls! I\'ll make them both roll again!')
            #time.sleep(.5)
            highest_roller.dice_cup = []
            player.dice_cup = []
            
            roll(highest_roller, 2)
            highest_roller.roll_total = sum(highest_roller.dice_cup)
            print('The previous highest roller, ' + highest_roller.name + ', rolls and gets ' + str(highest_roller.roll_total) + '.')
            #time.sleep(.5)
            
            roll(player, 2)
            player.roll_total = sum(player.dice_cup)
            print('The challenger, ' + player.name + ', rolls and gets ' + str(player.roll_total) + '.')
            #time.sleep(.5)
            
            if highest_roller.roll_total > player.roll_total:
                print(highest_roller.name + ' holds on to first!')
                #time.sleep(.5)
            elif highest_roller.roll_total == player.roll_total:
                print('No way! They tied again! I\'m letting ' + highest_roller.name + ' keep first!')
                #time.sleep(.5)
            else:
                print(player.name + ' stole first!')
                #time.sleep(.5)


        elif player.roll_total == highest_roll:
            print('There was a tie, so I\'ll make ' + player.name + ' roll again.')
            #time.sleep(1)
            player.dice_cup = []
            roll(player, 2)
            player.roll_total = sum(player.dice_cup)
            print('This time they rolled a ' + str(player.roll_total) + '.')
            #time.sleep(.5)

            if player.roll_total > highest_roll:
                highest_roll = player.roll_total
                highest_roller = player
                print('Good roll! ' + player.name + ' stole first!')
                #time.sleep(.5)

            elif player.roll_total == highest_roll:
                print('You won\'t believe this, but they tied again! so I\'m letting ' + player.name + ' have first now.')
                #time.sleep(.5)
                highest_roll = player.roll_total
                highest_roller = player
            else:
                print('Sorry, ' + player.name + '. No dice! haha! ' + highest_roller.name + ' holds on to first!')
                #time.sleep(.5)

    print('\nThat\'s all the rolls! ' + highest_roller.name + ' will go first!\n\n')
    return highest_roller

# Determine who goes next
def next_player(player):
    if player == p1:
        player = b1
    elif player == b1:
        player = b2
    elif player == b2:
        player = b3
    else:
        player = p1
    
    print('It\'s ' + player.name + '\'s turn next!')
    return player

# Make all players roll
def roll_5():
    for player in all_players:
        player.dice_cup.clear()
        if player == p1:
            print(p1.name + '! Press ENTER to roll!')
            input()
            roll(player, 5)
            print(player.name + ' rolls...')
            #time.sleep(1)
        else:
            roll(player, 5)
            print(player.name + ' rolls...')
            #time.sleep(1)

# For the first turn
def first_turn(player):
    if player == p1:
        print('Lucky you, ' + player.name + '! Make your bid!!')
        player.bid_value = die_value_input('Choose a die value:\n')
        player.bid_quantity = die_quantity_input('And how many do you think there are?:\n')

    else:
        print('Ok ye bucket of bolts! ' + player.name + '! Choose a die value:\n')
        #time.sleep(1)
        player.bid_value = randrange(1, 7, 1)
        print(player.bid_value)
        #time.sleep(1)
        print('Now how many Arrr there? (That\'s a pirate joke.. I have a lot of them..):\n')
        player.bid_quantity = randrange(1, 5, 1)
        print(player.bid_quantity)
        #time.sleep(1)
    
    return player.bid_quantity, player.bid_value

def raise_bid_value(player, current_bid):
    player.bid_value = die_value_input('Choose a die value the same or higher:\n')
    
    if player.bid_value < current_bid[0]:
        print('Yarr.. don\'t ye know the rules? Your bid has to be the SAME or HIGHER than the current bid! Try again!:\n')
        raise_bid_value(player, current_bid)
    else:
        print('Mm.. yes.. you may be right. Good bid.')
    return player.bid_value 

def raise_bid_quantity(player, current_bid):
    player.bid_quantity = die_quantity_input('How many do you think there are?:\n')
    
    if player.bid_quantity < current_bid[1]:
        print('Yarr.. don\'t ye know the rules? Your bid has to be the SAME or HIGHER than the current bid! Try again!:')
        raise_bid_quantity(player, current_bid)
    else:
        print('Mm.. yes.. you may be right. Good bid.')
    return player.bid_quantity 

# Turn Protocol
# next_turn(current_player, first_bid)
def next_turn(player, bid):
    current_bid = bid
    choice = 0
    player.bid = [0, 0]

    if player == p1:
        choice = input('Ok ' + player.name + '! Will you RAISE or CHALLENGE the last bid?\n1: RAISE\n2: CHALLENGE\n')
        if choice in {'1', 'one', 'One'}:
            print('Very well.. the current bid is ' + str(current_bid[1]) + ' ' + str(current_bid[0]) + '\'s.')
            player.bid[0] = raise_bid_value(player, current_bid)
            player.bid[1] = raise_bid_quantity(player, current_bid)
            current_bid = player.bid
            new_player = next_player(player)
            next_turn(new_player, current_bid)

        elif choice in {'2', 'two', 'Two'}:
            print('We have a CHALLENGE! hahaha! That\'s it then, ye bilgerats! Show your dice!!')
            reveal_dice()
        else:
            print('That\'s not a choice ye scallywag! Make a real choice or its to the plank with you!!')
            choice = input('Ok ' + player.name + '! NOW WILL YE *RAISE* or *CHALLENGE* THE LAST BID!?\n1: RAISE\n2: CHALLENGE\n')
            if choice in {'1', 'one', 'One'}:
                print('Very well.. the current bid is ' + str(current_bid[1]) + ' ' + str(current_bid[0]) + '\'s.')
                player.bid_value = raise_bid_value(player, current_bid)
                player.bid_quantity = raise_bid_quantity(player, current_bid)
                current_bid = [player.bid_value, player.bid_quantity]
                new_player = next_player(player)
                next_turn(new_player, current_bid)
                    
            elif choice in {'2', 'two', 'Two'}:
                print('We have a CHALLENGE! hahaha! That\'s it then, ye bilgerats! Show your dice!!')
                reveal_dice()
            else:
                print('THAT\'S IT LANDLUBBER!!\n' + player.name + ', YOU are a LIAR and you will spend ETERNITY ON THIS SHIP!!')
                game_over()

    else:
        print('Ok ' + player.name + '! Will you RAISE or CHALLENGE the last bid?')
        choice = randrange(1,11,1)
        if choice < 9:
            print('Ok, so what\'s your bid?')
            player.bid[0] = current_bid[0] + randrange(1,2)
            if current_bid[0] > 6:
                current_bid[0] = 6
            player.bid[1] = current_bid[1] + randrange(1,4)
            if player.bid[1] > dice_in_play:
                player.bid[1] = dice_in_play
            print('The bid is in... ' + player.name + ' thinks there be ' + str(player.bid[0]) + ' ' + str(player.bid[1]) + '\'s!')
            current_bid = player.bid
            new_player = next_player(player)
            next_turn(new_player, current_bid)
        else:
            print('We have a CHALLENGE! hahaha! That\'s it then, ye bilgerats! Show your dice!!')
            reveal_dice()

# Define what happens when the last bid is challenged and dice are revealed
# count quantity of each value

# Cleanup. IF bidding player loses, remove 1d6
# if challenger loses, remove 1d6
# New Round. losing player plays first 
def reveal_dice():
    print('DICE REVEAL!')
    """ if 1:
        reset_game_1()
    elif 2:
        reset_game_2()
    elif 3:
        end_game_1()
    else:
        end_game_2() """

# Define if challenger is right
""" def reset_game_1():
    print('code here')
    next_player() """

# Define if challenger is wrong
""" def reset_game_2():
    print('code here')
    next_player() """


# ---GAME ENDINGS--------------------------------------------------------------
def end_game_1():
    print('You did it!')

def end_game_2():
    print('You also did it!')

# When you just can't be a team player...
def game_over():
    print_slower('Bosun: Well.. you really made a mistake...\nNow you\'re stuck here with us for the rest of forever..\nI hope you like Crazy Pete.. because you\'ll be listening to him for a loooooooong time! hahahahaahahaha!')
    print_slower('You are escorted to the lower level and given a toothbrush to start scrubbing the floor. As you get closer, you begin hearing someone talking...')
    print_slower('Busun: Have fun! hahahahaaha HEY CRAZY PETE! I got a new friend for ye! They want to hear ALL of your stories! hahahahaha')
    print_slower('Crazy Pete: I go to the store. A car is parked. Many cars are parked or moving. Some are blue. Some are tan. They have windows. In the store, there are items for sale. These include such things as soap, detergent, magazines, and lettuce. You can enhance your life with these products. Soap can be used for bathing, be it in a bathtub or in a shower. Apply the soap to your body and rinse. Detergent is used to wash clothes. Place your dirty clothes into a washing machine and add some detergent as directed on the box. Select the appropriate settings on your washing machine and you should be ready to begin. Magazines are stapled reading material made with glossy paper, and they cover a wide variety of topics, ranging from news and politics to business and stock market information. Some magazines are concerned with more recreational topics, like sports card collecting or different kinds of hairstyles. Lettuce is a vegetable. It is usually green and leafy, and is the main ingredient of salads. You may have an appliance at home that can quickly shred lettuce for use in salads. Lettuce is also used as an optional item for hamburgers and deli sandwiches. Some people even eat lettuce by itself. I have not done this. So you can purchase many types of things at stores...')
    print_slower('Will this go on forever?')
    print_slower('Crazy Pete: If I drive around, I sometimes notice the houses and buildings all around. There are also pieces of farm land that are very large. Houses can be built from different kinds of materials. The most common types are brick, wood, and vinyl or synthetic siding. Houses have lawns that need to be tended. Lawns need to be mowed regularly. Most people use riding lawnmowers to do this. You can also use a push mower. These come in two varieties: gas-powered and manual. You don’t see manual push-mowers very much anymore, but they are a good option if you do not want to pollute the air with smoke from a gas-powered lawnmower. I notice that many families designate the lawnmowing responsibility to a teenager in the household. Many of these teenagers are provided with an allowance for mowing the yard, as well as performing other chores, like taking out the trash, washing the dishes, making their bed, and keeping the house organized. Allowances are small amounts of money given by parents to their children, usually on a weekly basis. These usually range from 5 dollars to 15 dollars, sometimes even 20 dollars. Many parents feel that teenagers can learn financial responsibility with this system...')
    print_slower('You should have just chosen 1 or 2....')
    print_slower('Crazy Pete: Now I will talk about farm land. Farm land can be identified by some common features. They almost always consist of a very large patch of dirt with small green plants lined up in very long rows. You may sometimes see farm equipment riding over these rows, like tractors or combines. These machines help farmers grow more crops in less time. They are a very helpful invention. Some different types of crops are soybeans, cotton, corn, tomatoes, tobacco, and lettuce (which I mentioned earlier). Most crops are used as food, and can be defined as either fruits or vegetables. Some are commonly eaten raw, after being rinsed in water to remove any dirt. Some are often cooked, which helps give them a more pleasant taste and makes them easier to chew. A very versatile vegetable is the potato. It can be eaten raw, or it can be cooked in a variety of ways. They can be baked, and many people like to add butter to them. They can be mashed, and a lot of times brown gravy or milk gravy is poured on top of them. They can be cut into thin strips and fried. Typically a large amount of grease is required to prepare potatoes in this style, but they are easy to make and easy to eat. You can order them at several fast-food restaurants. Potatoes can also be boiled, stewed, and scalloped. There is a wide variety of options available to you when cooking potatoes....')
    print_slower('Seriously.. he has to stop to breathe at some point, doesn\'t he?')
    print_slower('Crazy Pete: Some other types of crops grown on farm land are used for other purposes. Cotton is used to make clothing (which I also mentioned earlier). It is a very versatile and inexpensive material for clothes. Such items as shirts, pants, socks, and underwear can be made from cotton. The process of converting cotton from a cotton plant to clothing is fairly complicated. Today, cotton is harvested more efficiently through the use of the cotton gin, invented by Eli Whitney many years ago....')
    print_slower('He\'s still talking.. how is this possible? What will you do now?')
    input("")
    print_slower('IT DOESN\'NT MATTER WHAT YOU WANT TO DO! YOU\'RE HERE FOR ETERNITY, REMEMBER!?')
    print_slower('Crazy Pete: Tobacco is another type of crop. It is used in making cigarettes. A lot of people smoke cigarettes, even though many medical sources have identified them as harmful to people’s health. Warnings are printed on cigarette packages reminding people of possible dangers resulting from smoking. Cigarettes are available in several brands, including Marlboro, Salem, and Virginia Slims. There is a brand called Kool, but I don’t know whether they are still available at most outlets. Tobacco farming is a large industry, and currently there is debate about it. Recently the government decided on some regulations that cost tobacco companies a large amount of money....')
    print_slower('You: Please... make it stop, PLEASE!')
    print_slower('What will you do?')
    input("")
    print_slower('hahahahahahahahahahahahahahahahahaha')
    print_slower('Crazy Pete: If you notice, some farm lands have animals living on them. Most of these are cows, and there are also pigs, sheep, and goats living on farms. Some are raised for the milk they provide. This milk goes through several processes to ensure that it is not contaminated before it is made available to consumers at stores (which I mentioned earlier). Another use for farm animals is meat. Three popular types of meat are beef, pork, and chicken. Beef comes from cows. Pork comes from pigs. Chicken comes from chickens, but you probably knew that. These animals are raised to become plump and healthy, then they are killed, sometimes at slaughter houses. The meat is then removed from their bodies, cleaned, and made available at a variety of stores and restaurants. Sometimes this process can seem gross, but it is part of an advanced ecological food chain on earth. Just like birds eat worms and tigers eat deer, human beings eat cows and pigs. The main difference is that we don’t eat animals raw. We cook the meat to remove blood, fat, and germs from it. We also season our meat with salt or different kinds of sauces. The end result is food that is very tasty and is healthy for us....')
    print_slower('The hatch to the upper deck opens and the Bosun sticks his head in.')
    print_slower('Well? hahahaha Have you had enough?')
    print_slower('1: Yes! Please! Let me out of here!\n2: Actually, young Peter and I are best of friends now, so your punishment isn\'t working..')
    choice = input("")
    if choice == '1':
        print_slower('Bosun: HAHAHAHAHA WELCOME TO THE FLYING DUTCHMAN!')
        print_slower('The hatch shuts and you go back to scrubbing, Crazy Pete talking in the background.. I guess this is just life now...')
        end_game_2()
    elif choice == '2':
        print_slower('Bosun: HAHAHAHAHA Me heart be warmed to know of your new friendship! HAHAHA WELCOME TO THE FLYING DUTCHMAN!')
        print_slower('The hatch shuts and you go back to scrubbing, Crazy Pete talking in the background.. I guess this is just life now...')
        end_game_2()
    else:
        print_slower('Bosun: I CAN\'NT BELIEVE ME EARS! YOU REALLY HAVEN\'T LEARNED YOUR LESSON YET!? WHY IS IT SO HARD TO CHOOSE 1 OR 2???')
        print_slower('The hatch shuts and you go back to scrubbing, Crazy Pete talking in the background.. I guess this is just life now...')
        print_slower('Crazy Pete: ....Farmers do not like trespassers. If a farmer sees one, he will sometimes shoot at them with a shotgun that he owns. Trespassing is against the law. Laws are created by government to prevent people from living in fear. They are meant to provide safety for citizens. Our government in America consists of a legislative branch, an executive branch, and a judicial branch. The legislative branch makes laws based on the concerns of citizens they represent. The executive branch consists of the President. This person enforces the law, and he has certain other duties like declaring war and approving bills prepared by members of the legislative branch. The President is also considered the leader of our country. The judicial branch interprets the laws. This branch consists of the courts and the trials held in them. Here a judge and jury determine from evidence presented by lawyers whether someone is guilty of breaking a law. Initial law enforcement takes place among police officers. They are the first people to encounter situations where a law is being broken. If a criminal (law-breaker) becomes too violent or hostile, they will use guns or mace or nightsticks to administer immediate punishment. Their goal is to bring the criminal under control, so that he can receive a punishment determined by members of the judicial branch of government. Punishments mostly include time in jail, but they can also include fines and, in extreme cases, the death penalty. There is controversy surrounding the death penalty. Children play with toys. This is common to almost all kids. Toys come in a very wide variety. Boys tend to like cars, action figures, and toy weapons. Girls tend to like dolls, toy kitchens, and make-up. Both of them like building or assembling things, be it with Legos, blocks, Play-Doh, or something similar. Toys can be found at most stores, and these days entire stores are dedicated to selling only toys. The most popular of these is Toys \'R\' Us (with a backwards “R”). Their mascot is Geoffrey the Giraffe. Children love to go to Toys \'R\' Us and look at the wide variety of toys available. Most children receive the greatest quanitity of toys on their birthdays, or during the holiday season in December. For the majority of children, this holiday is Christmas. For Jewish children, the holiday is Channakuh. Either way, the kid gets presents during this time, and most of these presents are toys. Christmas is a holiday which has gradually become centered around the character “Santa Claus” and his elves and reindeer. Children are told that Santa\'s elves build their toys, and Santa delivers them personally to each house in the world by riding in an airborne sleigh hauled by nine reindeer, including Rudolph the red-nosed reindeer, who leads the way. Another popular Christmas character is Frosty the Snowman. Frosty is basically any snowman that comes to life. So during Christmas, many children build snowmen, and some of them hope that theirs might come to life. But all of these characters are myths. The true origin of Christmas is a celebration of the birth of Jesus, who founded the religion of Christianity a couple of thousand years ago. Many popular Christmas carols deal with his story, such as “Joy to the World” and “Silent Night.” Other holidays include Thanksgiving, Halloween, and Independence Day. Thanksgiving has become a tradition of preparing large quantities of food for a large gathering of people, mainly family and friends. This meal usually features turkey or ham as the main course. Turkey and ham are both kinds of meat (which I mentioned earlier). The meal usually also consists of dressing and a wide assortment of vegetables (which I also mentioned earlier). The origin of Thanksgiving is usually traced to the days of the pilgrims, who were the first settlers in America. They made peace with the native people, the Indians, and together enjoyed a large feast, thanking God for providing them with such an abundance. (Their concepts of God were probably very different.)Halloween is the holiday when people dress in costumes to look like other characters. Most of these are children, who go from door to door in different neighborhoods to request candy from the people living there. They usually say “trick or treat” then receive a treat. Very rarely does the person in the house respond with a trick. Halloween has some sort of demonic origin that I am not quite sure about, but the name derives from “All Hallow\'s Eve.” I will not say much about Independence Day, but it is the day Americans celebrate the anniversary of our independence from Britain. Most families purchase fireworks during this holiday and set them off in their lawns (which I mentioned earlier). America gained independence from Britain in the late 1700\'s after the Revolutionary War. Britain was hoping to extend its empire across the Atlantic Ocean, but the colonists who settled the territory did not want to be under Britain\'s control, with their various taxes and regulations. Both sides were very passionate about their position on the issue, so a war occurred. This war featured a few heroes, including George Washington and Paul Revere. George Washington became America\'s first president when we gained independence. I am not sure what happened to Paul Revere. The Declaration of Independence was written before the war by Thomas Jefferson in 1776 and made clear the position of the colonists. It was signed by many important people, including Ben Franklin and John Hancock. Ben Franklin is well-known for many things. One of these is inventing electrical conductors in the form of lightning rods. A famous tale is that he flew a kite with a small piece of metal somewhere on the string during a lightning storm. This was an effective way to test his theory. Another thing Ben Franklin is known for is publishing Poor Richards Almanac. This was like a magazine and contained some of his famous writings and quotations. One famous quote was “Tell me, I forget. Teach me, I remember. Involve me, I learn.” Maybe this had something to do with why he flew that kite. Trees are one of our most important natural resources. They are made of wood, and wood can be made into a variety of products. Some of the more obvious kinds are furniture, houses, and toothpicks. However, wood can also be made into paper. When I first heard this, I was skeptical, but it is true. Paper is a very important product in our society. Writers and artists have greatly benefited from the invention of paper. With only some paper and a pen or pencil, a writer can produce stories and poems that can captivate readers. They can also write down historical facts about their society. Actually, these writings don\'t become historical until years later. At the time, the writings could probably be considered news. Artists use paper for their drawings and paintings. They can also use canvas. Drawings and paintings can be very beautiful. They can depict a wide variety of subjects, including flowers, animals, landscapes, and people. They can be realistic or impressionistic. Some paintings also attempt to convey emotions merely by the way the colors are combined and the brushstrokes are applied. This is a modern or contemporary approach to art. Many people think this approach does not require as much talent as the realistic styles. I will end my writing here. I have tried to make it very boring, and I hope I have succeeded. There are plenty of boring documents available for you to read. Check your public library for more information. You can also find boring materials at a bookstore or on websites. Sometimes this information can be found in magazines (which I mentioned earlier)...........')
        end_game_2()


# Start Game
#------------------------------------------------------------------------------
print("Player 1! What is your name?:")
p1.name = input("")
if p1.name == "":
    p1.name = 'Player 1'

print('Great! Nice to meet you, ' + p1.name + '!\nArrr you ready to play a game of Pirate\'s Dice!? ')
input("")
print('Then stop your lollygagging!! LET\'S PLAY!\n\nPlayers! Roll to see who goes first!\n')
print('Press ENTER to roll...')
input("")

# 1. players roll 2 dice to determine who goes first
current_player = who_goes_first()

# 2. all players roll dice (get 5 values of 1-6)
print('\nFIRST TURN!\nEveryone ROLLLLLL!!')
#time.sleep(1)
all_dice_cups = roll_5()
dice_in_play = count_dice()
print('The rolls are done! Get ready for the first bid!')
#time.sleep(1)

# 3. first player bids (choose a value, choose a quantity ex: five 2s)
first_bid = first_turn(current_player)
print('\nThe first bid is in!\n' + current_player.name + ' bids ' + str(first_bid[1]) + ' ' + str(first_bid[0]) + '\'s.')
#time.sleep(1)

# 4. next player chooses: A. raise quantity or B. Challenge bid
current_player = next_player(current_player)
next_turn(current_player, first_bid)