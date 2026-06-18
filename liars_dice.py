from random import randint
import random, sys, time

#---FUTURE FEATURES------------------------------------------------------------
# [DONE] fix grammar for 'one 1's' (we now say "1 die showing 4")
# [DONE] give the bots a basic strategy for bidding and challenging
# Make it type out die values (like "five 2's" -> "five twos")
# Add harder difficulty levels by making the bots even smarter
# Allow for adjusting the number of bots in game
# Allow for multiple human players
# [DONE] Add a GUI -- see liars_dice_gui.py (pixel-art pygame version)


# ---Information for Game------------------------------------------------------
# Every player (you and the bots) is built from this blueprint.
class Player:
  def __init__(self, name):
    self.name = name            # what we call this player
    self.dice_cup = []          # the dice they rolled this round (a list of numbers)
    self.roll_total = 0         # used only when we roll to see who goes first
    self.num_dice = 5           # how many dice they still have (you lose dice when you lose!)
    self.is_bot = name.startswith("Bot")   # True for bots, False for the human

# Make one human player and three bots to play against.
p1 = Player("Player 1")
b1 = Player("Bot 1")
b2 = Player("Bot 2")
b3 = Player("Bot 3")

# 'players' holds everyone still in the game. When a player runs out of
# dice, we remove them from this list.
players = [p1, b1, b2, b3]

# Game Info
dice_in_play = 0   # total number of dice on the table right now


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
      if value < 1 or value > 6:
        return die_value_input('Yarr.. don\'t ye know the rules? A die has 6 sides! Try again. A number between 1 and 6 this time!:\n')
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
      elif quantity < 1:
        return die_quantity_input('Are ye daft!? What do you think that clatterin noise inside everyone\'s cups be then?? Play for real! How many dice ye wager?:\n')
      return quantity
   except:
      return die_quantity_input('What are you saying?? Choose a number!\n')

# ---Dice Functions ---------------------------------------------------------
def count_dice():
    dice_total = 0
    for player in players:
        count = len(player.dice_cup)
        dice_total += count
    return dice_total

# Roll some dice for a given player the amount of times specified
def roll(player, num_dice):
  player.dice_cup = [randint(1, 6) for _ in range (num_dice)]
  player.roll_total = sum(player.dice_cup)
  
# Make every player still in the game roll all of their dice.
def roll_all():
    for player in players:
        player.dice_cup.clear()
        # The human gets to press ENTER to roll for dramatic effect.
        if not player.is_bot:
            print('\n' + player.name + '! Press ENTER to roll your ' + str(player.num_dice) + ' dice!')
            input("")
        roll(player, player.num_dice)
        print(player.name + ' rolls...')
        # Only the human is allowed to peek at their own dice!
        if not player.is_bot:
            print('Your dice are: ' + show_dice(player.dice_cup))

# ---Game Progression ---------------------------------------------------------
# Determine who goes first: everyone rolls 2 dice, highest roll wins.
def who_goes_first():
    highest_roller = None
    highest_roll = 0

    for player in players:
        roll(player, 2)
        print(player.name + ' rolls and gets ' + str(player.roll_total) + '...')

        # If this is the best roll so far, this player takes the lead.
        # (If there's a tie, whoever got there first keeps the lead.)
        if player.roll_total > highest_roll:
            highest_roll = player.roll_total
            highest_roller = player
            print(player.name + ' is now the highest roller!\n')

    print('\nThat\'s all the rolls! ' + highest_roller.name + ' will go first!\n\n')
    return highest_roller

# Find whose turn is next by stepping to the next player in the list.
# The % (modulo) wraps us back to the start when we reach the end.
def next_player(player):
    i = players.index(player)
    return players[(i + 1) % len(players)]

# ---BIDDING HELPERS-----------------------------------------------------------
# Turn a bid into nice readable text, like "3 dice showing 5".
# (This also fixes the awkward 'one 1's' grammar from earlier!)
def bid_text(quantity, value):
    word = 'die' if quantity == 1 else 'dice'
    return str(quantity) + ' ' + word + ' showing ' + str(value)

# Turn a list of dice into something pretty, like "[2] [5] [1]".
def show_dice(cup):
    return ' '.join('[' + str(d) + ']' for d in cup)

# A new bid must be HIGHER than the old one. That means either a bigger
# quantity, OR the same quantity with a bigger die value.
def is_higher_bid(new_q, new_v, old_q, old_v):
    if new_q > old_q:
        return True
    if new_q == old_q and new_v > old_v:
        return True
    return False

# ---TAKING A TURN-------------------------------------------------------------
# The very first bid of a round. The starting player can't challenge yet
# (there's nothing to challenge!), so they just make a bid.
def opening_bid(player):
    if player.is_bot:
        # The bot bids a value and a quantity loosely based on its own dice.
        value = randint(1, 6)
        quantity = player.dice_cup.count(value) + randint(0, 1)
        if quantity < 1:
            quantity = 1
        if quantity > dice_in_play:
            quantity = dice_in_play
        print('Ok ye bucket of bolts, ' + player.name + ' opens the bidding!')
        return quantity, value
    else:
        print('\nLucky you, ' + player.name + '! Ye make the first bid!')
        print('Your dice are: ' + show_dice(player.dice_cup))
        value = die_value_input('Choose a die value (1-6):\n')
        quantity = die_quantity_input('And how many do ye think there be in total?:\n')
        return quantity, value

# Ask the human what they want to do. Returns one of:
#   ('raise', quantity, value)   or   ('challenge', None, None)
def human_turn(player, cur_q, cur_v):
    print('The current bid is ' + bid_text(cur_q, cur_v) + '.')
    print('Your dice are: ' + show_dice(player.dice_cup))

    # Is a higher bid even possible? (You can't go past every die showing a 6.)
    higher_possible = cur_q < dice_in_play or cur_v < 6

    while True:
        choice = input('Will ye RAISE or CHALLENGE the last bid?\n1: RAISE\n2: CHALLENGE\n')

        if choice in {'1', 'one', 'One', 'raise', 'RAISE'}:
            if not higher_possible:
                print('There\'s no higher bid to be made, matey! Ye must CHALLENGE!')
                continue
            # Keep asking until they give a bid that is actually higher.
            while True:
                new_v = die_value_input('Choose a die value (1-6):\n')
                new_q = die_quantity_input('How many do ye think there be?:\n')
                if is_higher_bid(new_q, new_v, cur_q, cur_v):
                    print('Mm.. yes.. ye may be right. Good bid.')
                    return ('raise', new_q, new_v)
                else:
                    print('Yarr! Yer bid must be a HIGHER quantity, or the SAME quantity with a HIGHER die value! Try again!')

        elif choice in {'2', 'two', 'Two', 'challenge', 'CHALLENGE'}:
            return ('challenge', None, None)

        else:
            print('That\'s not a choice ye scallywag! Pick 1 or 2!')

# Let a bot decide what to do. Same return format as human_turn.
def bot_turn(player, cur_q, cur_v):
    # How many of the bid value does the bot already have in its own cup?
    own = player.dice_cup.count(cur_v)
    # Guess how many the OTHER players have (each die has a 1-in-6 chance).
    others = dice_in_play - len(player.dice_cup)
    expected = own + others / 6

    # Can a higher bid even be made?
    can_raise_quantity = cur_q < dice_in_play
    can_raise_value = cur_v < 6

    # Decide whether to challenge. The more the bid passes what we'd expect,
    # the more likely the bot thinks it's a big fat lie.
    if not can_raise_quantity and not can_raise_value:
        challenge = True                      # no higher bid is possible!
    elif cur_q > expected + 1:
        challenge = randint(1, 10) <= 8       # bid looks too greedy
    elif cur_q > expected:
        challenge = randint(1, 10) <= 3       # bid is a little high
    else:
        challenge = randint(1, 10) <= 1       # bid seems safe, rarely challenge

    if challenge:
        return ('challenge', None, None)

    # Otherwise the bot raises. Sometimes bump the value, otherwise the quantity.
    if can_raise_value and randint(1, 2) == 1:
        return ('raise', cur_q, cur_v + 1)
    elif can_raise_quantity:
        return ('raise', cur_q + 1, cur_v)
    else:
        return ('raise', cur_q, cur_v + 1)

# ---PLAYING A ROUND-----------------------------------------------------------
# Play one full round of bidding. Returns the player who loses a die.
def play_round(starting_player):
    global dice_in_play

    print('\n=========== NEW ROUND ===========')
    roll_all()
    dice_in_play = count_dice()
    print('\nThere are ' + str(dice_in_play) + ' dice in play this round.')

    # The starting player makes the opening bid.
    cur_q, cur_v = opening_bid(starting_player)
    bidder = starting_player
    print('\nThe first bid is in! ' + bidder.name + ' bids ' + bid_text(cur_q, cur_v) + '.')

    # Then we go around the table until someone challenges.
    player = next_player(starting_player)
    while True:
        print('\n--- It\'s ' + player.name + '\'s turn! ---')
        if player.is_bot:
            action, new_q, new_v = bot_turn(player, cur_q, cur_v)
        else:
            action, new_q, new_v = human_turn(player, cur_q, cur_v)

        if action == 'challenge':
            print('\nWe have a CHALLENGE! ' + player.name + ' doesn\'t believe ' + bidder.name + '!')
            print('That\'s it then, ye bilgerats! Show your dice!!')
            return reveal_dice(bidder, player, cur_q, cur_v)
        else:
            cur_q, cur_v = new_q, new_v
            bidder = player
            print(player.name + ' bids ' + bid_text(cur_q, cur_v) + '.')
            player = next_player(player)

# ---THE BIG REVEAL------------------------------------------------------------
# A bid was challenged! Show everyone's dice, count up the bid value, and
# figure out who was right. The loser of the argument loses a die.
def reveal_dice(bidder, challenger, cur_q, cur_v):
    print('\n*********** DICE REVEAL! ***********')
    total = 0
    for player in players:
        print(player.name + ' had: ' + show_dice(player.dice_cup))
        total += player.dice_cup.count(cur_v)   # add up the matching dice

    print('\nThere were ' + str(total) + ' dice showing ' + str(cur_v) + ' in total!')
    print('The bid was ' + bid_text(cur_q, cur_v) + '.')

    # If there were at least as many as the bid claimed, the bidder was right.
    if total >= cur_q:
        print('\nThe bid was GOOD! ' + bidder.name + ' was tellin\' the truth!')
        print(challenger.name + ' loses a die for the false challenge!')
        return challenger
    else:
        print('\nThe bid was a LIE! There just weren\'t enough!')
        print(bidder.name + ' gets caught and loses a die!')
        return bidder


# ---GAME ENDINGS--------------------------------------------------------------
# The happy ending: the human is the last pirate standing and wins!
def end_game_1():
    print_slower('\nBosun: Well, blow me down! Ye actually WON?!')
    print_slower('Ye stared the sea devils in the eye and out-lied every last one of \'em!')
    print_slower('Take yer gold and get off me ship before I change me mind! HAHAHA!')
    print('\n*** YOU WIN! Congratulations, ' + p1.name + '! ***')

# The not-so-happy ending: this is called at the very end of game_over().
def end_game_2():
    print('\n*** GAME OVER ***')
    print_slower('Ye lost all yer dice, and now ye scrub the decks of the Flying Dutchman for eternity... Arrr.')

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


# ---START THE GAME------------------------------------------------------------
# This function runs the whole game from start to finish.
def play_game():
    # Ask the human for their name.
    print('Player 1! What is your name?:')
    p1.name = input('')
    if p1.name == '':
        p1.name = 'Player 1'

    print('Great! Nice to meet you, ' + p1.name + '!')
    print('Arrr ye ready to play a game of Pirate\'s Dice!?')
    input('')
    print('Then stop yer lollygagging!! LET\'S PLAY!\n')
    print('Here be the rules: everyone hides their dice. On yer turn ye either')
    print('RAISE the bid (more dice, or a higher value) or CHALLENGE the last bid.')
    print('On a challenge, we count ALL the dice. Guess wrong and ye lose a die.')
    print('Lose all yer dice and ye be OUT. Last pirate standing wins!\n')

    print('Players! Roll to see who goes first!')
    print('Press ENTER to roll...')
    input('')

    # First, roll to see who starts.
    current_player = who_goes_first()

    # Keep playing rounds until only one pirate is left standing.
    while len(players) > 1:
        loser = play_round(current_player)

        # The loser of the round loses one die.
        loser.num_dice -= 1

        if loser.num_dice <= 0:
            # This player is out of dice and out of the game!
            print('\n' + loser.name + ' has lost their last die and is OUT of the game!')
            next_starter = next_player(loser)   # work out who's next BEFORE removing
            players.remove(loser)

            # If the human is knocked out, it's the Crazy Pete ending...
            if loser is p1:
                game_over()
                return

            current_player = next_starter
        else:
            # Still in the game! The loser starts the next round.
            print('\n' + loser.name + ' now has ' + str(loser.num_dice) + ' dice left.')
            current_player = loser

        # Is there only one pirate left? Then we have a winner!
        if len(players) == 1:
            if players[0] is p1:
                end_game_1()
            else:
                print('\n' + players[0].name + ' is the last pirate standing and wins!')
            return

# Actually start the game!
play_game()