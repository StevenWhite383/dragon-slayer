import random, time, sys
#############[Dev Notes]#############
#
# User should always be able to access inventory.
#
# To start a battle, add a monster_name, monster_health and monster_level.
# Then call the battle_start() function.
# 
# Character choice should change their max_health, armour, inventory,
# and battle_options.
# 
# Items: Book of (S)pells, (C)loak, S(t)aff, (D)agger, B(o)w,
#        (L)ockpick, S(w)ord, Shi(e)ld, (A)rmour, (H)ealth Potion,
#        (G)rimoire, (I)nvisibility Potion
#
#####################################

def typingPrint(text):
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.02)

def typingInput(text):
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.02)
    value = input()
    return value

#############[Global variables]#############
area = 0                # Every time the player progresses, this should increment.
checkpoint = 0          # This will be used if the player goes back to the town.
health = 100            # Sets the player's health to 100 at the start.
max_health = 100        # Sets the player's max health to 100 at the start.
upgrades = 0            # Sets the default upgrades to 0.
gold = 0                # Sets the default gold to 0.
armour = 0              # Sets the default armour rating to 0.
player_level = 1        # Sets the default player level to 0.
player_xp = 0           # Sets the default player xp to 0.
xp_needed = 15 * player_level
player_name = ""
monster_name = ""
monster_health = 1
monster_level = 1
character = ""
inventory = ["(B)ack"]
cloak = 0
burn = False
spells = ["(F)ireball", "Free(z)e", "(H)eal"]
battle_options = ["(F)ight", "(I)nventory", "(R)un"]
in_battle = False
knights = False
lvl1_choices = ["(L)eft", "(F)orwards", "(R)ight", "(I)nventory"]
encountered_town = False
encountered_troll = False
encountered_library = False
encountered_tavern = False
encountered_alchemist = False
encountered_blacksmith = False
boss_fight = False


#############[Characters]#############

# When the player selects a character, this
# function should run. It should give the player
# the items that are specific to each character.
# It should also give them different stats.
def char_chosen():
    global character
    global max_health
    global health
    global armour
    global inventory
    
    if character == "knight":
        max_health = 120
        health = max_health
        armour = 6
        inventory.extend(("S(w)ord", "Shi(e)ld", "(A)rmour"))
        inventory.sort()
        
    if character == "thief":
        max_health = 100
        health = max_health
        armour = 2
        inventory.extend(("(D)agger", "B(o)w", "(L)ockpick", "(L)ockpick", "(L)ockpick"))
        inventory.sort()
        
    if character == "wizard":
        max_health = 110
        health = max_health
        armour = 0
        inventory.extend(("Book of (S)pells", "(C)loak", "S(t)aff"))
        inventory.sort()


#############[Battle Mechanics]#############

# When the player attacks, a random damage
# value is calculated. Changes if they have
# weapon upgrades or land a critical hit.
# There is also a small chance to miss.
# The different characters should have
# different strength stats and different
# critical hit chances. The Wizard will
# also have a spellbook to use.
def dmg_given():
    global monster_name
    global monster_health
    global upgrades
    global burn
    # Knight battle
    # High damage, low crit chance
    if character == "knight":
        dmg = random.randint(8, 26)
        miss_crit = random.randint(1, 11)
        if miss_crit == 1: #10% chance to miss
            dmg = 0
            print()
            print("You missed!")
            print(f"The {monster_name} took no damage.")
            print()
            input()
            dmg_taken()
        elif miss_crit == 10: #10% chance to crit
            dmg = int((dmg + upgrades + (player_level - 1)) * 1.25)
            print()
            print(f"A critical hit! You hit for {dmg} damage!")
            print()
            monster_health = (monster_health - dmg)
            if knights == True:
                print(f"The knights attack the {monster_name} for 3 damage!")
                monster_health = monster_health - 3
                input()
            else:
                print()
            if monster_health <= 0:
                battle_won()
            else:
                print(f"The {monster_name} has {monster_health}HP left.")
                input()
                dmg_taken()
        else:
            dmg = int(dmg + upgrades + (player_level - 1))
            print()
            print(f"You hit for {dmg} damage!")
            print()
            monster_health = (monster_health - dmg)
            if knights == True:
                print(f"The knights attack the {monster_name} for 3 damage!")
                monster_health = monster_health - 3
                input()
            else:
                print()
            if monster_health <= 0:
                battle_won()
            else:
                print(f"The {monster_name} has {monster_health}HP left.")
                input()
                dmg_taken()


    # Thief normal hit
    # Low damage, high crit chance
    elif character == "thief":
        dmg = random.randint(1, 11)
        miss_crit = random.randint(1, 11)
        if miss_crit == 1: #10% chance to miss
            dmg = 0
            print()
            print("You missed!")
            print(f"The {monster_name} took no damage.")
            print()
            input()
            dmg_taken()
        elif miss_crit >= 6: #40% chance to crit
            dmg = int((dmg + upgrades + (player_level - 1)) * 1.25)
            print()
            print(f"A critical hit! You hit for {dmg} damage!")
            print()
            monster_health = ((monster_health - dmg))
            if monster_health <= 0:
                battle_won()
            else:
                print(f"The {monster_name} has {monster_health}HP left.")
                input()
                dmg_taken()
        else:
            dmg = int(dmg + upgrades + (player_level - 1))
            print()
            print(f"You hit for {dmg} damage!")
            print()
            monster_health = (monster_health - dmg)
            if monster_health <= 0:
                battle_won()
            else:
                print(f"The {monster_name} has {monster_health}HP left.")
                input()
                dmg_taken()

    # Wizard normal hit
    # Medium damage, medium crit chance, Fireball adds burn, Freeze removes burn
    elif character == "wizard":
        dmg = random.randint(3, 15)
        miss_crit = random.randint(1, 11)
        if miss_crit == 1: #10% chance to miss
            dmg = 0
            print()
            print("You missed!")
            print(f"The {monster_name} took no damage.")
            print()
            input()
            dmg_taken()
        elif miss_crit >= 9: #20% chance to crit
            dmg = int((dmg + upgrades + (player_level - 1)) * 1.25)
            print()
            print(f"A critical hit! You hit for {dmg} damage!")
            print()
            monster_health = (monster_health - dmg)
            if burn == True:
                print(f"The {monster_name} is on fire and takes 3 damage from the burn!")
                monster_health = monster_health - 3
                input()
            else:
                print()
            if monster_health <= 0:
                battle_won()
            else:
                print(f"The {monster_name} has {monster_health}HP left.")
                input()
                dmg_taken()
        else:
            dmg = int(dmg + upgrades + (player_level - 1))
            print()
            print(f"You hit for {dmg} damage!")
            print()
            monster_health = (monster_health - dmg)
            if burn == True:
                print(f"The {monster_name} is on fire and takes 3 damage from the burn!")
                monster_health = monster_health - 3
                input()
            else:
                print()
            if monster_health <= 0:
                battle_won()
            else:
                print(f"The {monster_name} has {monster_health}HP left.")
                input()
                dmg_taken()
    else:
        print()


# When the player is in a battle,
# depending on the enemy level,
# the player will take a random amount
# of damage. The enemy cannot critical
# hit, but they can miss.
# Armour will reduce damage.
def dmg_taken():
    global monster_name
    global monster_level
    global health
    global cloak
    dmg = random.randint(1, 6)
    hit = random.randint(1, 11)
    if hit == 10: #10% chance to miss
        dmg = 0
        print()
        print(f"The {monster_name} missed!")
        print()
        input()
        battle_start()
    else:
        dmg = ((dmg * monster_level) - armour)
        if dmg < 0:
            dmg = 0
            print()
            print(f"The {monster_name} hit you for {dmg}")
            print(f"You have {health}HP left.")
            print()
            input()
            battle_start()
        else:
            if cloak > 0:
                cloak = cloak - 1
                dmg = int(dmg * 0.2)
                print()
                print("Your cloak protected you!")
                print(f"The {monster_name} hit you for {dmg}")
                health = health - dmg
                if health <= 0:
                    game_over()
                else:
                    print(f"You have {health}HP left.")
                    print()
                    input()
                    battle_start()
            else:
                print()
                print(f"The {monster_name} hit you for {dmg}")
                health = health - dmg
                if health <= 0:
                    game_over()
                else:
                    print(f"You have {health}HP left.")
                    print()
                    input()
                    battle_start()


# If the player wins a battle
# they are rewarded with a random
# amount of coins and have a small
# chance to find loot.
# They will also get some XP and if they
# get enough, they will level up and
# gain some stats.
def battle_won():
    global monster_name
    global monster_level
    global gold
    global xp_needed
    global player_level
    global player_xp
    global in_battle
    global max_health
    global area
    global boss_fight
    
    in_battle = False
    print()
    print(f"Congratulations! You killed the {monster_name}!")
    gold_reward = random.randint(1, 11)                         #Gold reward
    print(f"The {monster_name} dropped {gold_reward} gold!")
    gold = (gold + gold_reward)
    item_drop = random.randint(1, 21)                           #Item reward
    if item_drop == 20:
        print(f"The {monster_name} dropped a health potion too! Lucky!")
        inventory.append("Health Potion")
        inventory.sort()
        print()
        input()
    else:
        print()
    xp_drop = random.randint(5, 21)                             #XP reward
    xp_drop = int((xp_drop * (monster_level * 0.5)))
    print(f"You gained {xp_drop}XP!")
    player_xp = player_xp + xp_drop
    if player_xp < xp_needed:
        xp_needed = xp_needed - xp_drop
        print(f"You need {xp_needed} more XP to level up.")
        input()
    else:
        xp_needed = 15 * player_level
        player_level = player_level + 1
        max_health = max_health + (player_level * 5)
        print(f"Congratulations! You are now level {player_level}!")
        print(f"Your damage has increased and your maximum health is now {max_health}.")
        input()
    area = (area + 1)
    boss_fight = False
    adventure()


# When a player enters a battle, they
# will have the choice to fight,
# access their inventory or run away.
def battle_start():
    global access_inventory
    global in_battle
    global area
    global boss_fight
    
    in_battle = True
    print()
    print("Please select an option:")
    print(battle_options)
    chosen_option = input("").upper()
    if chosen_option == "F":
        dmg_given()
    elif chosen_option == "I":
        print()
        access_inventory()
    elif chosen_option == "R":
        if boss_fight == True:
            print()
            print("You cannot run from this battle!")
            input()
            battle_start()
        else:
            print()
            escape = random.randint(1, 10)
            print(f"You try to run! Roll a {escape} or lower to succeed.")
            print(f"Chance of escape: {escape}0%")
            input()
            roll = random.randint(1, 10)
            if roll > escape:
                print(f"You rolled a {roll}")
                print("You failed to escape...")
                input()
                dmg_taken()
            else:
                print(f"You rolled a {roll}!")
                print("You managed to escape!")
                print()
                input()
                in_battle = False
                area += 1
                adventure()
    else:
        print("That is not a valid input")
        battle_start()


# If the player loses all their
# health, they will game over.
# This must show to the user
# that they died and they need
# to restart the game to play more.
def game_over():
    global player_level
    global gold
    print()
    print("GAME OVER!")
    print("You have died")
    input()
    print(f"You reached LVL {player_level} and earned {gold} gold.")
    input()
    print("Please press 'Enter' to go back to the menu...")
    input()
    print()
    menu()

# This should display the player's
# inventory and allow them to use
# items. If the player is in battle
# and they use an item, they should
# then get hit by the enemy, as using
# the item was their turn.
def access_inventory():
    global cloak
    
    print()
    print("_______________________________")
    print(f"{player_name} the {character}")
    print(f"LVL {player_level}")
    print(f"Health: {health}/{max_health}")
    print(f"Gold: {gold}")
    print()
    print(inventory)
    print("_______________________________")
    print()
    item_use = input("Which item would you like to use? ").upper()
    
    # Global inventory
    if item_use == "B":
        if in_battle == True:
            print()
            battle_start()
        else:
            print()
            adventure()
    elif item_use == "H":
        if "(H)ealth Potion" in inventory:
            inventory.remove("(H)ealth Potion")
            heal()
        else:
            print("You do not have a health potion.")
            input()
            access_inventory()
    elif item_use == "G":
        if "(G)rimoire" in inventory:
            print()
            print("A powerful book, said to contain spells of Master level and beyond\nSomeone might want this...")
            print()
            input()
            access_inventory()
        else:
            print()
            print("You do not have this item yet.")
            input()
            access_inventory()
    elif item_use == "I":
        if "(I)nvisibility Potion" in inventory:
            print()
            print("An extremely rare potion that can turn the person who drinks it invisible for 30 seconds\nSomeone might want this...")
            print()
            input()
            access_inventory()
        else:
            print()
            print("You do not have this item yet.")
            input()
            access_inventory()
        
    # Knight inventory
    elif character == "knight":
        print()
        if item_use == "W":
            print()
            print(f"A sharp, metal sword. It has been upgraded {upgrades} times.\nSelect 'Fight' to use it.")
            print()
            input()
            access_inventory()
        elif item_use == "E":
            print()
            print("A sturdy shield. This reduces the damage you take.")
            print()
            input()
            access_inventory()
        elif item_use == "A":
            print()
            print("Heavy metal armour given to the honourable. This protects you from damage well.")
            print()
            input()
            access_inventory()
        else:
            print()
            print("Input not recognised")
            input()
            access_inventory()

    # Thief inventory
    elif character == "thief":
        if item_use == "D":
            print()
            print(f"Your trusty dagger - This has gotten you into and out of many dangerous situations.\nIt has been upgraded {upgrades} times.\nSelect 'Fight' to use it.")
            print()
            input()
            access_inventory()
        elif item_use == "O":
            if in_battle == False:
                print()
                print("This bow never misses, but cannot critical hit.")
                print()
                input()
                access_inventory()
            else:
                bow()
        elif item_use == "L":
            if in_battle == True:
                print()
                print("You cannot use that here.")
                print()
                input()
                access_inventory()
            else:
                if "(L)ockpick" in inventory:
                    print()
                    print("Can unlock chests without the need of a key.")
                    print()
                    input()
                    access_inventory()
                else:
                    print()
                    print("You have run out of lockpicks")
                    print()
                    input()
                    access_inventory()
        else:
            print()
            print("Input not recognised")
            print()
            input()
            access_inventory()
    
    # Wizard inventory
    elif character == "wizard":
        if item_use == "S":
            spellbook()
        elif item_use == "C":
            if in_battle == True:
                cloak = 3
                print()
                print("Cloak equipped! The next 3 attacks will do heavily reduced damage!")
                print()
                input()
                dmg_taken()
            else:
                print()
                print("It sways in the wind but is surprisingly sturdy. Equip in battle to heavily reduce damage from the next 3 attacks.")
                print()
                input()
                access_inventory()
        elif item_use == "T":
            print()
            print(f"A powerful staff passed down from your late master.\nYou can hit things with it, but it won't do much damage.\nIt has been upgraded {upgrades} times.\nSelect 'Fight' to use it.")
            print()
            input()
            access_inventory()
        else:
            print()
            print("Input not recognised")
            print()
            input()
            access_inventory()

    else:
        print()
        input("Input not recognised.")
        print()
        access_inventory()


# For the heal potion and
# heal spell. If it heals past the
# player's max health, it should set
# the player's health to the max.
def heal():
    global health
    global max_health
    global in_battle

    health = health + 50
    if health > max_health:
        health = max_health
        print(f"You have healed 50HP! Your health is now {health}/{max_health}")
        input()
    else:
        print(f"You have healed 50HP! Your health is now {health}/{max_health}")
        input()
    if in_battle == True:
        dmg_taken()
        battle_start()
    else:
        adventure()


# If the thief uses the bow in a battle,
# It should do a bit of damage, and never
# miss.
def bow():
    global monster_health
    global monster_name
    dmg = random.randint(3, 16)
    dmg = int(dmg + upgrades + (player_level - 1))
    print()
    print(f"You hit for {dmg} damage!")
    print()
    monster_health = ((monster_health - dmg))
    if monster_health <= 0:
        battle_won()
    else:
        print(f"The {monster_name} has {monster_health}HP left.")
        input()
        dmg_taken()


# The Wizard's Spell book.
# Damage spells do fixed damage.
# The Wizard can also heal.
def spellbook():
    global in_battle
    global monster_name
    global monster_health
    global burn
    print()
    print()
    print("_______________________________")
    print("Spellbook:")
    print()
    print(spells)
    print()
    print("_______________________________")
    print()
    
    # If in battle, use the spells against the enemy.
    if in_battle == True:
        print("Choose a spell:")
        cast = input().upper()
        
        # Fireball
        if cast == "F":
            print(f"You cast a Fireball at the {monster_name} for 8 damage!")
            print("The Fireball applies burn!")
            input()
            monster_health = monster_health - 8
            burn = True
            if monster_health <= 0:
                battle_won()
            else:
                print(f"The {monster_name} has {monster_health}HP left.")
                input()
                dmg_taken()
                
        # Freeze
        elif cast == "Z":
            print(f"You cast Freeze on the {monster_name} for 16 damage!")
            input()
            monster_health = monster_health - 16
            burn = False
            if monster_health <= 0:
                battle_won()
            else:
                print(f"The {monster_name} has {monster_health}HP left.")
                input()
                dmg_taken()
        
        # Heal
        elif cast == "H":
            heal()
        
        elif cast == "B":
            print()
            battle_start()
        
        else:
            print("That is not a valid spell.")
            input()
            spellbook()
    
    # If not in battle, describe the spells.
    else:
        print("Choose a spell:")
        cast = input().upper()
        
        if cast == "F":
            print()
            print("Launch a fireball at the enemy that hits for 8 damage and applies burn.\nBurn does an additional 3 damage every turn.")
            input()
            print()
            access_inventory()
        elif cast == "Z":
            print()
            print("Hit the enemy with an incredibly cold gust. Does 16 damage. Removes burn effect.")
            input()
            print()
            access_inventory()
        elif cast == "H":
            heal()
        elif cast == "B":
            print()
            adventure()
        else:
            print("That is not a valid spell.")
            input()
            spellbook()


#############[Knight interactions]#############

def start_scenario_knight1():
    print()
    options = ["1. Greet the knights politely and walk on.", "2. Ask the knights to assist you on your quest.", "3. Challenge the knights to a fight."]
    
    for option in options:
        print(option)
    
    choice = typingInput("\nEnter the number of your choice: ")
    
    if choice == "1":
        greet_scenariok1()
    elif choice == "2":
        help_scenariok1()
    elif choice == "3":
        fight_scenariok1()
    else:
        alternative_scenariok1()

def greet_scenariok1():
    typingPrint("Hail, good men How fare thee on this fine day.\n")
    typingPrint("Knights: Hail, good sir, very well thank you, and a fine day to you.\n")
    input()
    start_scenario_knight1()
    # Add a specific scenario details for the bypass option
    

def help_scenariok1():
    global knights

    typingPrint("Hail, good men! I beseech your aid to be granted.\n")
    typingPrint("Knights: Very well, we shall assist you in your quest.\n")
    typingPrint("Excellent, the more the merrier.\n")
    typingPrint("The knights join you on your journey and will now assist you in battle!")
    knights = True
    # Add a specific scenario details for the help option

def fight_scenariok1():
    global monster_level
    global monster_health
    global monster_name
    
    typingPrint("Out of my way or feel the edge of my sword, knights.\n")
    print(r"""
              />
             / <
O[\\\\\\\\\(O):::<=============================================-
             \ <
              \>

            """)
    typingPrint("Very well........have at you then.........")
    print(r"""
               />
             / <
O[\\\\\\\\\(O):::<=============================================-
             \ <
              \>

            """)
    
    monster_name = "knights"
    monster_health = 120
    monster_level = 5
    battle_start()
    # Start fight scenario with the knights

def alternative_scenariok1():
    typingPrint("You didn't choose any of the available options and return to town.\n")
    input()
    town()


#############[Mini-games]#############

# These are all the gambling mini-games
# you can play in the tavern to win
# (or lose) gold.

# ROULETTE

    # Function to simulate spinning the roulette wheel
def spin_roulette():
    numbers = list(range(0, 37))  # List of numbers on the wheel
    colours = ['red', 'black']  # Possible colours on the wheel
    winning_number = random.choice(numbers)  # Randomly select a winning number using random.choice()
    winning_colour = random.choice(colours)  # Randomly select a winning colour using random.choice()

    # Determine if the winning number is odd or even using if-elif-else statement
    if winning_number == 0:  # Check if the winning number is 0
        number_type = 'neither odd nor even'
    elif winning_number % 2 == 0:  # Check if the winning number is even using modulus operator %
        number_type = 'even'
    else:
        number_type = 'odd'

    # Print the winning number, colour, and number type using f-string formatting
    print(f'Winning number: {winning_number}')
    print(f'Winning colour: {winning_colour}')
    print(f'Number type: {number_type}')

    return winning_number, winning_colour, number_type

# Function to take the user's bet
def take_bet(balance):
    bet_dict = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 'numbers': []}  # Dictionary to store the bet amounts
    while True:  # Use a while loop to repeatedly prompt the user for input
        try:
            bet_type = int(input('Select bet type (1: Number, 2: Red, 3: Black, 4: Odd, 5: Even) (or 0 to finish): '))
                       #converts input, from a string, into an integer.
            if bet_type == 0:  # Check if the user wants to finish betting and exit the loop
                break
            elif bet_type == 1:  # Check if the user wants to bet on a specific number
                numbers_input = input('Enter the numbers you want to bet on (separated by commas): ')
                numbers = [int(num.strip()) for num in numbers_input.split(',') if num.strip()]  # Use lisot comprehension to convert input string to a list of integers
                bet = int(input('Place your bet: '))

                # Check if the total bet amount exceeds the balance using sum() function and list comprehension
                if sum([bet_dict['numbers'][i]['bet'] for i in range(len(bet_dict['numbers']))]) + (bet * len(numbers)) > balance:
                    print('Sorry, you do not have enough gold to place that bet.')
                
                for number in numbers:  # Iterate over the numbers in the list
                    bet_dict['numbers'].append({'number': number, 'bet': bet})  # Add each number and its corresponding bet to the bet_dict
            elif bet_type in bet_dict:  # Check if the bet type is valid
                bet = int(input('Place your bet:'))

                # Check if the bet amount exceeds the balance
                if bet_dict[bet_type] + bet > balance:
                    print('Sorry, you do not have enough gold to place that bet.')
                    continue

                bet_dict[bet_type] += bet  # Update the bet amount in the bet_dict
            else:
                print('Invalid bet. Please choose again.')
        except ValueError:
            print('Invalid choice. Please try again.')
        
    return bet_dict

# Function to calculate the payout based on the bet and the winning result
def calculate_payout(bet_dict, winning_number, winning_colour, number_type):
    payout = 0

    # function to update the payout based on the bet type and multiplier
    def update_payout(bet_type, multiplier):
        nonlocal payout
        payout += bet_dict[bet_type] * multiplier

    # Update the payout based on the winning colour and number type using if-else statements
    update_payout(2, 2) if winning_colour == 'red' else None
    update_payout(3, 2) if winning_colour == 'black' else None
    update_payout(4, 2) if number_type == 'odd' else None
    update_payout(5, 2) if number_type == 'even' else None

    for number_bet in bet_dict['numbers']:  # Iterate over the list of number bets
        if number_bet['number'] == winning_number:  # Check if the bet matches the winning number
            payout += number_bet['bet'] * 36  # Calculate the payout for the number bet using multiplication

    return payout

def cash_out():
    global gold

    print(f'You have {gold} gold.')
    print('Thank you for playing!')
    play_again = input('Do you want to play again? (y/n): ')
    if play_again.lower() != 'y':
        town()
    else:
        play_roulette()

# Function to play the roulette game
def play_roulette():
    global gold

    balance = gold
    while True:  # Use a while loop to keep the game running until the player chooses to cash out or runs out of balance
        print('\nWelcome to Roulette! Are you ready to win big?')
        print('1. Spin the wheel')
        print('2. Cash out')
        choice = input('Enter your choice: ')

        if choice == '1':  # Check if the player chooses to spin the wheel
            bet = take_bet(balance)  # Call the take_bet() function to get the player's bet
            winning_number, winning_colour, number_type = spin_roulette()  # Call the spin_roulette() function to get the winning result
            payout = calculate_payout(bet, winning_number, winning_colour, number_type)  # Calculate the payout based on the bet and the winning result

            if payout > 0:  # Check if the player has won
                win_amount = payout - sum([num_bet['bet'] for num_bet in bet['numbers']])  # Calculate the win amount
                balance += win_amount  # Update the balance with the win amount
                print(f'Well done, you won: {win_amount}')
            else:
                balance -= sum([num_bet['bet'] for num_bet in bet['numbers']])  # Subtract the total bet amount from the balance
                print('You lost!')

            print(f'Current balance: {balance}')

            if balance <= 0:  # Check if the player has run out of balance
                print('Oh no! You have run out of gold.')
                break

        elif choice == '2':  # Check if the player chooses to cash out
            cash_out()  # Call the cash_out() function to display the final balance and end the game
            break

        else:
            print('Invalid choice. Please try again.')


# ROCK, PAPER, SCISSORS

def rps():
    options = ("rock", "paper", "scissors")
    running = True

    while running:
        player = None
        computer = random.choice(options)

        while player not in options:
            player = input("Enter a choice (rock, paper, scissors): ")

        print(f"Player: {player}")
        print(f"Computer: {computer}")

        if player == computer:
            print("It's a draw")
        elif (player == "rock" and computer == "scissors") or (player == "paper" and computer == "rock") or (player == "scissors" and computer == "paper"):
            gold += 1
            print("You win 1 gold coin")
        else:
            print("You lose")

        if input("Play again? (y/n): ").lower() != "y":
            running = False
            print()
            print("You head back to the town square.")
            input()
            town()


# BLACKJACK

def deal_card():
    """Deal a random card from the deck."""
    cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4
    card = random.choice(cards)
    return card

def calculate_score(hand):
    """Calculate the total score of a hand."""
    if sum(hand) == 21 and len(hand) == 2:
        return 0  # Blackjack (win with a score of 0)

    if 11 in hand and sum(hand) > 21:
        hand.remove(11)
        hand.append(1)

    return sum(hand)

def compare_scores(player_score, computer_score, bet):
    """Compare the scores and determine the winner."""
    if player_score == computer_score:
        return f"It's a tie! You lose {bet} gold.\n"
    elif computer_score == 0:
        return f"You lose {bet} gold! The dealer has a Blackjack.\n"
    elif player_score == 0:
        return f"Congratulations! You win {bet} gold with a Blackjack.\n"
    elif player_score > 21:
        return f"You bust. Sorry, you lose {bet} gold.\n"
    elif computer_score > 21:
        return f"The dealer bust. You win {bet} gold!\n"
    elif player_score > computer_score:
        return f"You win {bet} gold!\n"
    else:
        return f"You lose {bet} gold!\n"

def blackjack():
    global gold

    """Play a game of Blackjack."""
    typingPrint("Welcome to blackjack - The aim is to not exceed 21 points and to score higher than the dealer.\n")
    typingPrint("In the event of a tie, the dealer always wins!!!\n")
    typingPrint("Good luck!")

    player_hand = []
    computer_hand = []
    game_over = False

    for _ in range(2):
        player_hand.append(deal_card())
        computer_hand.append(deal_card())

    # Betting
    typingPrint(f"\nYou have {gold} gold.\n")
    bet = int(typingInput("Place your bet: "))
    while bet > gold:
        typingPrint("Invalid bet. You don't have enough gold.\n")
        bet = int(typingInput(" Place your bet:\n"))

    while not game_over:
        player_score = calculate_score(player_hand)
        computer_score = calculate_score(computer_hand)

        typingPrint(f"\nYour cards: {player_hand}, current score: {player_score}\n")
        typingPrint(f"Dealer's first card: {computer_hand[0]}")

        if player_score == 0 or computer_score == 0 or player_score > 21:
            game_over = True
        else:
            should_continue = typingInput("\nDo you want to draw another card? Type 'y' or 'n': ")
            if should_continue == 'y':
                player_hand.append(deal_card())
            else:
                game_over = True

    while computer_score != 0 and computer_score < 17:
        computer_hand.append(deal_card())
        computer_score = calculate_score(computer_hand)

    typingPrint(f"\nYour final hand: {player_hand}, \nfinal score: {player_score}\n")
    typingPrint(f"\nDealer's final hand: {computer_hand}, final score: {computer_score}\n")

    result = compare_scores(player_score, computer_score, bet)

    if "win" in result:
        bet *= 2  # Double the bet
        gold += bet
    else:
        gold -= bet

    typingPrint(result)
    typingPrint(f"\nTotal gold: {gold}\n")

    play_again = typingInput("\n\nPlay again.. (Y/N)?\n").upper()
    if play_again == "Y":
        blackjack()
    else:
        typingPrint("Good day!!")
        input()
        town()


# HIGHER OR LOWER

def deal_card():
    """Deal a random card from the deck."""
    cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14] * 4
    card = random.choice(cards)
    return card

def compare_cards(card1, card2):
    """Compare two cards and return the result."""
    if card1 == card2:
        return "equal"
    elif card1 < card2:
        return "higher"
    else:
        return "lower"

def higher_lower():
    global gold
    
    """Play the card game."""
    gold = 50
    playing = True

    while playing:
        typingPrint(f"******Welcome to higher or lower******\n")
        typingPrint(f"************Good Luck!****************\n")
        typingPrint(f"****You win or lose the difference****\n")
        typingPrint(f"Your current balance: {gold} gold coins\n")

        # Check if the player wants to cash out
        cash_out = typingInput("\nDo you want to cash out(c) or play on(p)?: ")
        if cash_out == "c":
            playing = False
            break

        # Deal the first card and ask for the player's guess
        current_card = deal_card()
        typingPrint(f"\nCurrent card: {current_card}")
        guess = typingInput("\nWill the next card be higher, lower? (h/l): ")

        # Deal the second card
        next_card = deal_card()
        typingPrint(f"\nNext card: {next_card}")

        # Compare the cards and determine the result
        result = compare_cards(current_card, next_card)

        if result == "equal":
            # Cards are equal
            print("\nThe cards are equal. No gold coins are won or lost.")
        elif (result == "higher" and guess == "h") or (result == "lower" and guess == "l"):
            # Player wins
            difference = abs(current_card - next_card)
            gold += difference
            print(f"\nYou win! You gained {difference} gold coins.\n")
        else:
            # Player loses
            difference = abs(current_card - next_card)
            gold -= difference
            if gold <= 0:
                gold = 0
                print("\nSorry, you lose! You lost all your gold coins.\n")
                playing = False
            else:
                print(f"\nSorry, you lose! You lost {difference} gold coins.\n")
            higher_lower

    typingPrint(f"\nYour final balance: {gold} gold coins\n")
    typingPrint("Thank you for playing!\n")
    input()
    town()


#############[Town Locations]#############

# The town is the hub area. The player should
# be able to visit shops here.
# The intro should only be played on first visit
# to each location.
# The player should be able to come back here from
# later levels, and then resume their progress when
# they choose to go back into the mountains.
def town():
    global area
    global encountered_town
    global town_choices

    encountered_town = True
    if area == 3:
        print("As you proceed forward, your eyes scanning the horizon, a glimpse of a distant town catches your attention. Intrigued by its presence, you feel an undeniable pull to explore the mysteries it holds. Following your instincts, you make your way towards the town, eager to uncover its secrets and immerse yourself in its vibrant atmosphere.")
        input()
        print("As you step into the town, a wave of sensations washes over you. The bustling energy of the market square captivates your senses, with vibrant colors, enticing aromas, and the lively chatter of locals filling the air. Narrow streets lined with charming buildings beckon you to wander deeper, as if each corner holds a new adventure waiting to unfold. Whether it's the cozy tavern radiating warmth and laughter, the mystical aura emanating from the alchemist's dwelling, or the rhythmic clang of the blacksmith's hammer, the town presents a captivating tapestry of sights and sounds that awaken your wanderlust.")
        input()
        area = 4

    while encountered_town == True:
        town_choices = ["(A)lchemist", "(B)lacksmith", "(L)ibrary", "(M)ountains", "(T)avern", "(I)nventory"]
        print("_______________________________")
        print("Where would you like to go?")
        print()
        print(town_choices)
        print()
        choice = input("").upper()
        if choice == "I":
            access_inventory()
        elif choice == "A":
            alchemist()
        elif choice == "B":
            blacksmith()
        elif choice == "L":
            library()
        elif choice == "M":
            mountains()
        elif choice == "T":
            tavern()
        else:
            print()
            print("That is not a valid choice.")
            input()


# The player should get the option to
# purchase the Grimoire - A magical book
# that, if acquired, could later be used
# to get the wizard on your side.
# If you play as the wizard, it has no use.
# Should check if the player has enough gold.
def library():
    global gold
    global encountered_library

    choice = ""
    pay = ""
    if encountered_library == False:
        encountered_library = True
        print()
        print("As you step through the ornate entrance of the library, a sense of awe washes over you. Sunlight streams through stained glass windows, casting a kaleidoscope of colors across rows upon rows of ancient books and scrolls. The air is filled with the delicate scent of aged parchment and the hushed whispers of knowledge that seem to linger in every corner.")
        input()
        print("At the heart of the library stands the owner, a figure who exudes wisdom and warmth. Their gentle eyes hold the reflection of countless stories and their presence seems to bridge the gap between the past and present. Dressed in flowing robes adorned with intricate symbols, the owner's demeanor radiates a serene and profound aura, as if they are a guardian of the accumulated knowledge within the library's walls.")
        input()
        print("With a welcoming smile, the owner extends a hand and greets you, their voice carrying a melodic timbre that seems to echo through the ages. Their passion for the written word is palpable, and their genuine enthusiasm for sharing knowledge shines through in every word and gesture.")
        input()
        print("\"Welcome, welcome!\", says the owner.")
        print("\"Please, take a look around. Let me know if I can help you with anything.\"")
        input()
        print("You take a look around the library. Dust dances in the variegated light. As you reach the back of the library, your eyes are drawn to a particular grimoire displayed on a velvet-lined pedestal. Its ancient pages, adorned with mystical symbols and delicate illustrations, seem to whisper secrets of forgotten realms. Sensing your fascination, the owner approaches with a knowing smile and offers to sell you the grimoire.")
        input()
    
    else:
        print()
        print("\"Welcome back!\". The owner greets you with a smile.")
        print()
        
    if "(G)rimoire" not in inventory:
        while choice != "Y" or choice != "N":
            print("Would you like to buy the grimoire? (Y/N)")
            print()
            choice = input("").upper()
            if choice == "Y":
                print()
                print("\"Excellent! That will be 10 gold coins.\"")
                print()
                print("(P)ay or (L)eave:")
                print()
                pay = input("").upper()
                if pay == "P":
                    if gold >= 10:
                        gold = gold - 10
                        inventory.append("(G)rimoire")
                        inventory.sort()
                        print()
                        print("\"Thank you!\", says the owner, gleefully.")
                        print(f"The grimoire has been added to your inventory. You have {gold} gold left.")
                        print()
                        input()
                        town()
                    else:
                        print()
                        print("\"I'm sorry, you don't have enough gold for that...\"")
                        input()
                        print("You head back to the town.")
                        input()
                        town()
                elif pay == "L":
                        print("You head back to the town.")
                        input()
                        town()
                else:
                    print()
                    print("That is not a valid input.")
                    choice = ""
                    input()
                    library()
            elif choice == "N":
                        print("You head back to the town.")
                        input()
                        town()
            else:
                print()
                print("That is not a valid input.")
                choice = ""
                input()
                library()
    
    else:
        print()
        print("You cannot buy anything else from here.")
        print("You head back to the town.")
        print()
        input()
        town()


########################################################
def tavern():
    global encountered_tavern
    global knights

    choice = ""
    if encountered_tavern == False:
        encountered_tavern = True
        print()
        print("As you push open the creaking doors of the tavern, a symphony of laughter, clinking glasses, and boisterous conversations envelops you. The warm glow of flickering candlelight illuminates a scene alive with revelry and camaraderie. Your eyes are immediately drawn to a group of knights, adorned in shining armor, gathered at the bar, regaling each other with tales of valor and adventure. Their presence exudes an aura of noble strength, their swords resting by their sides, ready to defend honor at a moment's notice.")
        input()
        print("Glancing across the bustling tavern, your gaze falls upon tables filled with people engaged in animated games of chance. The clatter of dice and the shuffling of cards create a symphony of anticipation and excitement. The air is thick with the aroma of hearty meals and the heady scent of ale, as mugs are raised in celebration or in consolation. The tavern serves as a vibrant hub of socializing and shared experiences, where stories are woven together, and friendships are forged over mugs of frothy brew.")
        input()
    else:
        if knights == False:
            print()
            print("You enter the tavern: The tables are packed with gambling games, and the knights chatting away at the bar.")
            input()
        else:
            print()
            print("You enter the tavern: The tables are packed with gambling games, and your knights go to the bar to drink.")
            input()
    
    while choice == "":
        if knights == False:
            print("Would you like to go (G)ambling, talk to the (K)nights, or (L)eave?")
            choice = input("").upper()
        else:
            print("Would you like to go (G)ambling, or (L)eave?")
            choice = input("").upper()
            
        if choice == "L":
            print()
            print("You leave the tavern.")
            input()
            town()
            
        elif choice == "G":
            print()
            print(f"You have {gold} gold.")
            print("What game would you like to play?")
            print("(R)oulette")
            print("(B)lackjack")
            print("(H)igher or Lower")
            print("Rock, (P)aper, Scissors")
            print("(L)eave")
            game = input("").upper()
            if game == "R":
                play_roulette()
            elif game == "P":
                rps()
            elif game == "B":
                blackjack()
            elif game == "H":
                higher_lower()
            elif game == "L":
                print()
                print("You leave the tavern.")
                input()
                town()
            else:
                print()
                print("That is not a valid input.")
                input()
                tavern()
        
        elif choice == "K":
            if character == "knight":
                print()
                typingPrint("You encounter a group of fellow knights.\n")
                typingPrint("What do you say to them?\n")
                start_scenario_knight1()
            else:
                print()
                print("You approach the knights. Their formidable presence is undeniable, their armor gleaming under the warm tavern lights. As you draw nearer, their conversations briefly pause, and they cast you a discerning glance. Yet, their demeanor soon softens, recognizing a fellow traveler in their midst. With a nod of acknowledgement, they welcome you into their circle, ready to share tales of heroic quests, battles fought, and lands traversed.")
                input()
                print("What would you like to say to the knights?")
                options = ["1. Would you like to join me on my quest?", "2. Leave"]
                for option in options:
                    print(option)
                choice = typingInput("\nEnter the number of your choice: ")
                if choice == "2":
                    print()
                    print("You wish the knights well and head out of the tavern, back to the town square.")
                    input()
                    town()                  
                elif choice == "1":
                    print()
                    print("You explain your mission to the knights. As you talk, they consider your request, your ambition, your goals. After a short while, and some murmuring, they speak thus:")
                    input()
                    print("\"Very well, Adventurer! We shall join you on your mission! You can count on us to aid you when you need it most.\"")
                    input()
                    knights = True
                    print("You go back to the town square.")
                    input()
                    town()
                else:
                    print()
                    print("That is not a valid input.")
                    input()
                    tavern()
        
        else:
            print()
            print("That is not a valid input.")
            input()
            tavern()


########################################################
def alchemist():
    global gold
    global player_name
    global encountered_alchemist

    choice = ""
    pay = ""
    if encountered_alchemist == False:
        encountered_alchemist = True
        print()
        print("As you step into the peculiar realm of the alchemist's shop, a burst of aromatic herbs and exotic concoctions fills your senses. The owner, a woman of intriguing eccentricity, greets you with an effervescent energy that seems to dance around her. Her wild, unkempt hair frames a face adorned with smudges of various potions, showcasing her devotion to the alchemical arts. With mismatched clothing and a mischievous twinkle in her eyes, she embodies a delightful quirkiness that sets her apart from the ordinary.")
        input()
        print("This enigmatic alchemist is a character of boundless curiosity and an unapologetic lack of boundaries. Her words flow with an unabashed enthusiasm as she imparts her knowledge, often veering off on tangents and sharing anecdotes from her own alchemical experiments. With each interaction, she unintentionally invades personal space, examining your belongings or even reaching out to touch an intriguing trinket you carry. Yet, her infectious passion and genuine desire to share her craft overshadow any sense of discomfort, leaving you both bemused and enchanted by her endearing idiosyncrasies.")
        input()
        print("\"I'm sure an adventurer like you must be looking for some health potions! Or maybe... Maybe this suuuuuuuper rare potion that I recently got ahold of... An invisibility potion!\"")
        input()
    else:
        print()
        print(f"\"Hey, {player_name}! It's lovely to see you again!\"")

    while choice == "":
        print()
        print("(H)ealth potion, (I)nvisibility potion, (L)eave?")
        print()
        choice = input("").upper()
        # Player chooses the health potion
        if choice == "H":
            choice = ""
            print()
            print("\"A health potion! A good choice! That will be 2 gold coins, please!\"")
            print("(P)ay, (L)eave")
            print()
            pay = input("").upper()
            if pay == "P":
                if gold >= 2:
                    gold = gold - 2
                    inventory.append("(H)ealth Potion")
                    inventory.sort()
                    print()
                    print("\"Thank you!!\", says the woman, excitedly.")
                    print(f"The health potion has been added to your inventory. You have {gold} gold left.")
                    print()
                    input()
                    print("\"Would you like to buy anything else?\"")
                    alchemist()
                else:
                    print()
                    print("\"I'm sorry, you don't have enough gold for that...\"")
                    input()
                    alchemist()
            elif pay == "L":
                alchemist()
            else:
                print()
                print("That is not a valid input.")
                input()
                alchemist()
        
        # Player chooses the invisibility potion.
        elif choice == "I":
            choice = ""
            if "(I)nvisibility Potion" in inventory:
                print()
                print("\"Sorry! You have already purchased my last invisibility potion!\"")
                input()
                alchemist()
            else:
                print()
                print("\"Interested in the rare invisibility potion, eh?\", the owner smirks.")
                print("\"This should be super expensive, but just for you, I'll sell it at a special price!\"")
                print("\"12 gold coins!\"")
                print("(P)ay, (L)eave")
                print()
                pay = input("").upper()
                if pay == "P":
                    if gold >= 12:
                        gold = gold - 12
                        inventory.append("(I)nvisibility Potion")
                        inventory.sort()
                        print()
                        print("\"Thank you!!\", says the woman, excitedly.")
                        print(f"The invisibility potion has been added to your inventory. You have {gold} gold left.")
                        print()
                        input()
                        print("\"Would you like to buy anything else?\"")
                        alchemist()
                    else:
                        print()
                        print("\"I'm sorry, you don't have enough gold for that...\"")
                        input()
                        alchemist()
                elif pay == "L":
                    alchemist()
                else:
                    print()
                    print("That is not a valid input.")
                    input()
                    alchemist()
        
        # Player chooses to leave.
        elif choice == "L":
                print()
                print("\"Come back soon!\"")
                input()
                town()
        
        else:
            print()
            print("That is not a valid input.")
            input()
            alchemist()


########################################################
def blacksmith():
    global gold
    global upgrades
    global encountered_blacksmith
    
    choice = ""
    pay = ""
    if encountered_blacksmith == False:
        encountered_blacksmith = True
        print()
        print("As you approach the outdoor blacksmith's shop, the vibrant glow of the forge illuminates the surrounding area, casting flickering shadows upon the weathered wooden structures. Standing amidst billowing smoke and flying sparks, the owner, a rugged male dwarf, commands attention with his stout stature and fiery red beard that seems to mirror the flames dancing before him.")
        input()
        print("The dwarf blacksmith exudes an undeniable strength, both physical and spiritual. Every swing of his mighty hammer carries the weight of experience, as he deftly shapes the raw metal into magnificent works of art. His rough hands, scarred and calloused, are a testament to his tireless dedication to his craft. Despite the grueling nature of his work, a warm smile frequently graces his face, revealing a genuine passion for his trade and a welcoming spirit that invites you into his realm of creation and craftsmanship.")
        input()
        print("\"'Ello, Travella'. Welcome to ma blacksmith. A can upgrade those weapons ya got there if ya want. It'll cost ya though, hahaha! Whad'ya say?\"")
    else:
        print()
        print("\"Welcome back, what can a do fo' ya?\"")
        print()

    while choice == "":
        print("(U)pgrade equipment, (L)eave")
        choice = input("").upper()
        if choice == "U":
            choice = ""
            if upgrades >= 3:
                print()
                print("\"A can't upgrade ya weapon any further than that. That weapon's ma pride 'n' joy!\"")
                input()
            else:
                upgrade_cost = (5 * (upgrades + 1))
                print()
                print(f"\"That'll be {upgrade_cost} gold. That okay? (Y/N)\"")
                pay = input("").upper()
                if pay == "Y":
                    if gold >= upgrade_cost:
                        print()
                        print("The dwarf gets to work on upgrading your weapon. He places the weapon on his forge and brings his hammer down on it hard. At first it looks like he's going to break your weapon, but upon further inspection, you see that every swing is methodically placed.")
                        input()
                        print("Your weapon has been upgraded and will now do a little more damage.")
                        upgrades = upgrades + 1
                        gold = gold - upgrade_cost
                        input()
                        blacksmith()
                    else:
                        print()
                        print("\"Maybe come back when yav got more gold...\"")
                        input()
                        blacksmith()
                elif pay == "N":
                    blacksmith()
                else:
                    print()
                    print("That is not a valid input.")
                    input()
                    blacksmith()
        elif choice == "L":
            print()
            print("\"Yep, yep.\"")
            input()
            town()
        
        else:
            print()
            print("That is not a valid input.")
            input()
            blacksmith()


########################################################

# Takes advantage of the 'checkpoint' variable
# to send the player back to where they were
# in the story. Can send the player anywhere
# as long as they have been there before.
# This allows the user to come and go from
# the town whenever they want.
def mountains():
    global checkpoint
    global area
    
# Add checkpoint checks for every level that is added.
    print()
    print("Are you sure you want to procceed into the mountains? (Y/N)")
    choice = input("").upper()
    if choice == "Y":
        if checkpoint == 0:
            area = 5
            adventure()
        if checkpoint == 1:
            area = 6
            adventure()
# If we had more than 1 level, they would be added like this:
#       if checkpoint == 2:
#       area = 7
#       adventure()


    elif choice == "N":
        town()
    else:
        print()
        print("That is not a valid input")
        mountains()


#############[Level 1]#############

def adventure():
    global encountered_troll
    global monster_name
    global monster_level
    global monster_health
    global area
    global checkpoint
    global gold
    global player_level
    global max_health
    global xp_needed
    global boss_fight

# First encounter
    if area == 1:
        print()
        print("As you awaken, the verdant embrace of a dense forest surrounds you, its towering trees casting dappled shadows on the forest floor. The air is filled with the earthy scent of moss and the distant symphony of wildlife.\nBefore you, three distinct paths unfurl: one veering left, alongside a tranquil river; another meandering to the right, promising ancient ruins and loot; and the third, leading straight ahead, disappearing into mist-shrouded hills.")
        print()
        print(lvl1_choices)
        print()
        choice = input("").upper()
        if choice == "I":
            access_inventory()
            
    # Player goes left
        elif choice == "L" and encountered_troll == False:
            print()
            print("You head left.")
            print("As you approach the tranquil river, the ambient sounds of the forest fade, replaced by the gentle symphony of flowing water. Crystal-clear and serene, the river glimmers under the soft caress of sunlight. Its surface ripples with playful dances as it meanders through the lush surroundings, reflecting the vibrant greens of overhanging branches and delicate wildflowers.")
            print()
            print("Lost in the beauty of the scene, your eyes wander and stumble upon a quaint bridge spanning the river. Its weathered planks bear the marks of time and nature's embrace, yet it stands sturdy, inviting you to explore the other side. Determined, you take a step forward, only to be halted by a hulking troll emerging from beneath the bridge.")
            print()
            print("With a toothy grin, the troll's voice rings out in mischievous rhymes, demanding your attention. \"Answer my riddle, mortal soul, or turn back and forsake your goal. If wit eludes, your steps reverse, else cross the bridge and quench your thirst.\" The challenge is set, and the fate of your journey lies in your ability to unravel the troll's cunning riddle. The troll speaks:")
            print()
            print("I am an odd number. Take away a letter and I become even. What number am I?")
            print()
            answer = input("").lower()
            if answer == "seven" or answer == "7":
                print()
                print("The troll growls a low hum. \"Correct...\", he says.\n\"Well how about this one?!\"")
                print()
                print("Davids father has three sons: Snap, Crackle, and _____?")
                print()
                answer = input("").lower()
                if answer == "david":
                    print()
                    print("The troll bares his teeth and swings his arm out in front of him, missing your face by mere inches. His grown causes the earth to shake beneath your feet.")
                    print()
                    print("\"...Correct...\"")
                    print()
                    print("\"Fine!\", shouts the troll. You can pass...\nThe troll hands you a gold coin for getting his riddles correct. As he retreats back under the bridge you notice a slight smirk corrupt his monstrous mouth.\nMaybe he wasn't angry that you got his riddles correct after all.")
                    print()
                    input()
                    gold = gold + 1
                    area = 2
                    adventure()
                else:
                    print()
                    print("The troll erupts into laughter.")
                    print("\"HAHAHA! Stupid human!\"")
                    print("The troll creeps closer, hands up, teeth glaring. His shadow turns what was once a magical, sunny day into the darkest of nights. This is a fight you cannot win.")
                    print()
                    print("As fast as your legs can take you, you bolt back up the river and into the forest. You cannot go left again.")
                    print()
                    lvl1_choices.remove("(L)eft")
                    encountered_troll = True
                    adventure()
            else:
                    print()
                    print("The troll erupts into laughter.")
                    print("\"HAHAHA! Stupid human!\"")
                    print("The troll creeps closer, hands up, teeth glaring. His shadow turns what was once a magical, sunny day into the darkest of nights. This is a fight you cannot win.")
                    print()
                    print("As fast as your legs can take you, you bolt back up the river and into the forest. You cannot go left again.")
                    input("Press 'Enter' to continue...")
                    lvl1_choices.remove("(L)eft")
                    encountered_troll = True
                    adventure()
        elif choice == "L" and encountered_troll == True:
            print()
            print("You cannot go left again.")
            print()
            input()
            adventure()
        
    # Player goes right
        elif choice == "R":
            print()
            print("As you approach the small ruins nestled within the forest, a sense of curiosity fills the air. The weathered stones stand as silent witnesses to a forgotten past. Overgrown with ivy and surrounded by an aura of mystery, the ruins exude an ancient charm. Within this intriguing scene, you spot two closed chests, each bearing a sense of anticipation. One chest rests slightly ajar, tempting you with its unknown contents, while the other remains securely locked, adorned with a sturdy padlock. The choice is yours, adventurer, to explore the mysteries within the partially opened chest or to test your skills and unlock the secrets held within the securely locked one.")
            print()
            while area == 1:
                print("Do you look inside the (O)pen chest, or try to open the (L)ocked chest?")
                choice = input("").upper()
                if choice == "O":
                    print()
                    print("You head over to the unlocked chest with anticipation. As you open the chest you are...")
                    input()
                    print("Disappointed to find just 2 gold coins...")
                    print("Better than nothing, at least!")
                    input()
                    gold = gold + 2
                    area = 2
                    adventure()
                    
                elif choice == "L" and character != "thief":
                    print()
                    print("You poke and prod at the chest to no avail. The lock is old but sturdy. Maybe if you had a key or lockpick...")
                    print()
                    input()
                    
                elif choice == "L" and character == "thief":
                    print()
                    print("You creep over to the locked chest and instantly recognise this type of lock. You've picked this type of lock thousands of times!\nWould you like to unlock the chest? (Y/N)")
                    print()
                    pick = input("").upper()
                    if pick == "Y":
                        print()
                        print("With deft precision, you effortlessly picked the lock, your skilled fingers swiftly maneuvering the tools to bypass the mechanism. In a matter of moments, the padlock surrendered, granting access to the hidden treasures within.")
                        print()
                        print("Inside the chest you find 7 gold coins!")
                        print("They have been added to your inventory.")
                        print()
                        input()
                        inventory.remove("(L)ockpick")
                        gold = gold + 7
                        area = 2
                        adventure()
                        
                else:
                    print()
                    print("That is not a valid option.")
                    print()
        
    # Player goes forwards
        elif choice == "F":
            print()
            print("You bravely march forward, traversing the mist-shrouded hills with determined steps, until a sudden rustling breaks the serenity of the air. Emerging from the ethereal veil of fog, a bandit approaches, his eyes glint with ill intent. You find yourself confronted by this menacing force, the clash between your unwavering resolve and the imminent threat unfolding before you.")
            print()
            input()
            monster_name = "bandit"
            monster_level = 2
            monster_health = 50
            battle_start()
        
        else:
            print()
            print("That is not a valid option.")
            print()
            adventure()


# Second encounter
    elif area == 2:
        lvl1_choices = ["(L)eft", "(F)orwards", "(R)ight", "(I)nventory"]
        print()
        print("A little ways down the road, you come across another fork.\nTo your left is a statue of a goddess; straight ahead, you see a crude roadblock which definitely was not built by humans; and to your right, an open field with a single old well.")
        print()
        while area == 2:
            print("Would you like to go (L)eft, (F)orwards, or (R)ight?")
            print()
            print(lvl1_choices)
            print()
            choice = input("").upper()
            if choice == "I":
                access_inventory()
            
        # Player goes left
            elif choice == "L":
                print()
                print("With a sense of curiosity and anticipation, you veer left.\nAs you follow the winding course towards the statue, the forest seems to whisper ancient secrets, guiding you to a sacred destination. And there, bathed in a soft, ethereal glow, stands a magnificent statue of a goddess, emanating an aura of enchantment.\nYou approach with reverence, feeling her divine presence envelop you. The goddess, while unmoving, smiles - her voice resonating like a gentle breeze, as she offers you a reward if you can answer her wise and thought-provoking questions.")
                print()
                input()
                
                score = 0
                question_no = 0
                typingPrint('In order to claim your reward, you must answer 3 questions correctly.\n')
                question_no += 1
                ques = typingInput(f'\n{question_no}. Which sea creature has three hearts?\n').lower()
                if ques == 'octopus':
                    score +=1
                    typingPrint('Well done! Here\'s a gold coin.\n')
                    gold = gold + 1
                else:
                    typingPrint('Incorrect!\n')
                    typingPrint(f'The correct answer is --> octopus\n')
                print()
                
                question_no += 1
                ques = typingInput(f'\n{question_no}. Which word can be placed before bottle, bell and bird?\n').lower()
    
                if ques == 'blue':
                    score +=1
                    typingPrint('Well done! Here\'s a gold coin.\n')
                    gold = gold + 1
                else:
                    typingPrint('Incorrect!\n')
                    typingPrint(f'The correct answer is --> blue\n')
                print()
                
                question_no += 1
                ques = typingInput(f'\n{question_no}. I have a cake and a table named after me, and I am used all round the world. What am I?\n').lower()
    
                if ques == 'coffee':
                    score +=1
                    typingPrint('Well done! Here\'s a gold coin.\n')
                    gold = gold + 1
                else:
                    typingPrint('Incorrect!\n')
                    typingPrint(f'The correct answer is --> coffee\n')
                print()
                
                #If all the answers were correct, give xp
                if score == 0:
                    print("\"Unfortunately you did not answer any of my questions correctly.\"\n\"I cannot give you a reward.\"")
                    print()
                    print("Feeling dejected, you pass the statue and carry on your journey.")
                    area = 3
                    input()
                    adventure()
                
                #If some answers were correct, no reward, but keep gold
                elif score > 0 and score < 3:
                    print("\"Unfortunately I cannot give you a reward as you got a question wrong. However, you can keep the gold that you earned. Good luck on your journey, adventurer.\"")
                    print()
                    print("You pass the statue, saddened that you didn't receive the reward, but content now that you have more gold.")
                    area = 3
                    input()
                    adventure()
                
                
                #If all answers were correct, give the player some xp as a reward
                else:
                    print("\"Congratulations on getting all of my questions correct!\"\n\"Here is your reward.\"")
                    print()
                    print("A surge of power begins to build at your feet. It starts as a subtle tremor, an unseen force pulsating through the very core of your being. In an instant, this latent energy erupts, coursing upward through your body like a radiant torrent. Your entire form becomes aglow, a shimmering cascade of light and sparkles that dances in harmony with the newfound strength infusing your every fiber. As the transformation subsides, you stand slightly taller, your spirit emboldened, and your abilities heightened.")
                    print()
                    player_level = player_level + 2
                    max_health = max_health + (player_level * 5)
                    xp_needed = 15 * player_level
                    print(f"You have been given 2 levels! You are now level {player_level}!")
                    print(f"Your damage has increased and your maximum health is now {max_health}.")
                    print()
                    area = 3
                    input()
                    adventure()
            
        # Player goes forwards
            elif choice == "F":
                print()
                print("As you tread forward along the path, your footsteps halt briefly as your eyes land upon a crude roadblock obstructing your way. The haphazard construction betrays its origin — clearly the work of a non-human hand. Before you have a chance to fully assess the situation, a mischievous goblin springs forth, its beady eyes gleaming with malice. With a snarl, it lunges at you, its intention clear: to engage in battle. Adrenaline surges through your veins as you ready yourself, knowing that victory against this formidable foe will require both skill and strategy.")
                print()
                input()
                monster_name = "goblin"
                monster_level = 3
                monster_health = 80
                battle_start()
            
        # Player goes right
            elif choice == "R":
                print()
                print("As you venture down the path to the right, a sense of intrigue fills your heart, for rumors of an old well nestled in a vast field have piqued your curiosity. As you draw nearer, the sight of the well emerges before you, an aging monument amidst the sea of green. Its stone walls, weathered by time's embrace, bear the marks of countless stories etched into its surface. Moss and ivy cling to its edges, lending an air of mystique to its presence. The sweet scent of damp earth and the faint echoes of droplets falling echo from its depths, enticing you to explore the secrets that lie within its ancient confines.")
                print()
                print("Would you like to pull the bucket out of the well? (Y/N)")
                pick = input("").upper()
                if pick == "N":
                    print("You decide not to let curiosity get the best of you and travel onwards, past the well.")
                    area = 3
                    input()
                    adventure()
                    
                elif pick == "Y":
                    well = random.randint(1, 3)
                    if well == 1:
                        print("You grasp the tattered rope and pull firmly, straight up. One hand below the other, you pull and pull. The rope seems endless...")
                        print()
                        input()
                        print("As your arms start to tire, as if it were timed so, an aboleth leaps out of the well at you and attacks!")
                        print()
                        input()
                        monster_name = "aboleth"
                        monster_level = 3
                        monster_health = 60
                        battle_start()
                    else:
                        print("You grasp the tattered rope and pull firmly, straight up. One hand below the other, you pull and pull. The rope seems endless...")
                        print()
                        input()
                        print("After what seems like forever, sunlight finally brings the bucket into view, and what's inside the bucket glimmers proudly...")
                        print("3 gold coins!\nThey have been added to your inventory.")
                        print()
                        gold = gold + 3
                        area = 3
                        input()
                        adventure()
                        
                else:
                    print()
                    print("That is not a valid option.")
                    print()

# Player reaches the town. The town is the hub area.
    elif area == 3:
        print()
        town()
# Area 4 is the town without the intro.
    elif area == 4:
        print()
        town()
    
# Area 5 is the intro to level 2.
# Area 6 is level 2.
    elif area == 5:
        area = 6
        checkpoint = 1
        print()
        print("You decide to leave the town and head up to the mountains for the first time. If you choose to go forwards, you will undoubtedly run into more trials to test your mental and physical strength. However, if you have unfinished business in the town, you can go back.")
        print("This is where your journey truly begins... Prepare yourself...")
        input()
        adventure()
    elif area == 6:
        choice = ""
        print()
        print("You are at the foot of the mountain.")
        print("Where would you like to go?")
        lvl2_choices = ["(F)orwards", "Back to (T)own", "(I)nventory"]
        print(lvl2_choices)
        choice = input("").upper()
        if choice == "I":
            access_inventory()
        elif choice == "T":
            print()
            print("You decide to head back to town.")
            input()
            town()
        elif choice == "F":
            print()
            print("This is where level 2 would really start. There would be more encounters, more puzzles and eventually a boss battle.\nUnfortunately, due to time limitations, missing team members and being too ambitious at the beginning, we did not manage to start developing level 2.")
            input()
            print("We have, however, included a basic fight with the Dragon, if you wish to proceed.")
            print("WARNING: This is a diifficult battle and you CAN NOT run from it.")
            print("(P)roceed, (B)ack to town")
            choice == ""
            choice = input("").upper()
            if choice == "P":
                boss_fight = True
                monster_health = 250
                monster_level = 8
                monster_name = "Dragon"
                area = 5
                battle_start()
            else:
                print("You turn back to town.")
                input()
                town()


#############[Code runs]#############

def print_pause(message):
    # Function to print a message. print_pause will be use instead of 
    # print to give the typewriter effect
    for char in message:
        print(char, end='', flush=True)  # Print each character without a newline
        time.sleep(0.02)  # Pause for a short duration to create the typewriter effect
    print()  # Print a newline at the end


def show_credits(): # Function to show credits
    print_pause('Credits')
    print_pause('The Team')
    print_pause('Lead Developer and Dialogue: Steven White,')
    print_pause('Developer and Dialogue: David Graham,')
    print_pause('Developer: Mohammad Zahir')
    print_pause('Developer: Michael Dickinson,')
    print_pause('Creative Input: Bruno Anyaeriuba,')
    print_pause('Thanks for playing.')


def ask_play_game():
    # Function to ask the player if they want to play Dragon Slayer.
    while True: # while loop to ask for the player's response until a valid choice is made.
        response = input('Would you like to play Dragon Slayer? (\'y\' for yes, \'n\' for no or \'c\' for credits): ')
        if response.lower() == 'y':       # Conditional statements (if, elif,)
            return True                   # used to start the game, see the credits 
        elif response.lower() == 'c':     # or exit the game.
            show_credits()
        elif response.lower() == 'n':
            return False


def explain_game(): #Function that explains the game.
    
    print_pause('                Welcome to Dragon Slayer!')
    print_pause('In a kingdom gripped by the relentless fury of a fearsome dragon,') 
    print_pause('hope has all but withered away. Yet, a solitary hero rises above ') 
    print_pause('the despair, answering the call of the desperate king. Driven by an')  
    print_pause('unwavering spirit, seeking glory, honor, and unimaginable riches.') 
    print_pause('The fate of the realm in your hands.')
    print_pause('Tip: sometimes the game will require you to press \'Enter\' before it can proceed.')


def get_user_name():
    global player_name    

    # Function to get the user's name
    name = input('Enter your name: ')  # use the input function to store in the name variable. 
    print_pause('Hello, ' + name + '! Prepare yourself for the challenge.')  # Print a personalized message.
    player_name = name


def choose_character():
    # Function to choose a character
    character = ''
    while character not in ['knight', 'wizard', 'thief']:# while loop to repeatedly ask for the player's 
        print_pause('Choose your character:')           # choice valid option  is selected.
        print_pause('1. Knight')
        print_pause('2. Wizard')
        print_pause('3. Thief')
        choice = input('Enter the number of your chosen character: ')  
        if choice == '1':
            character = 'knight'             # uses conditional statements (if, elif, else)
        elif choice == '2':                  # to choose which character to play as.
            character = 'wizard' 
        elif choice == '3':
            character = 'thief'  
        else:
            print_pause('Invalid choice! Please try again.')  # Print an error message for invalid choices
    return character  # Return the chosen character


def play_intro(character):
    # Function to play the character-specific intro.
    if character == 'knight':
        # If the chosen character is 'knight'
        print_pause('As a knight, you are known for your bravery and swordsmanship.')   # conditional statements (if, elif, else) to 
        print_pause('You have trained your whole life to face formidable foes.')        # print the introduction based on the character choice.
        print_pause('Now, the kingdom looks up to you to defeat the dragon and restore peace.')  
    elif character == 'wizard':
        # If  the chosen character is 'wizard'
        print_pause('As a wizard, you possess ancient knowledge and powerful spells.')
        print_pause('You have spent years honing your magical abilities.')
        print_pause('Now, it\'s time to put your skills to the test and vanquish the dragon.')
    elif character == 'thief':
        # If the chosen character is 'thief'
        print_pause('As a thief, you excel in stealth and agility.')
        print_pause('You have mastered the art of deception and nimble movements.')
        print_pause('Now, you must outsmart the dragon and claim victory for yourself.')


def show_inventory(character):
    # Function to display the character's inventory
    # onditional statements (if, elif,) to display a  choosen character's inventory.
    print_pause('Inventory:')  
    if character == 'knight':  # If the chosen character is 'knight'
        print_pause('- Sword')  # Print knight's inventory items
        print_pause('- Shield')
        print_pause('- Armour')
    elif character == 'wizard':  # If the chosen character is 'wizard'
        print_pause('- Staff')  # Print wizard's inventory items
        print_pause('- Spellbook')
        print_pause('- Cloak')
    elif character == 'thief':  # If the chosen character is 'thief'
        print_pause('- Dagger')  # Print thief's inventory items
        print_pause('- Bow')
        print_pause('- 3x Lockpicks')


def confirm():
    global area
    
    confirm = input("Would you like to use this character? (Y/N) ").upper()
    if confirm == "Y":
        area = 1
        char_chosen()
        adventure()
    else:
        menu()




#############[Game Start/Reset]#############

# Call this function to either
# start or reset the game.
# All stats will be reset to default.
# All progress will be lost.
# The player will be asked if they
# want to play the game, see the
# credits, or exit.
def menu():
    global area
    global checkpoint
    global upgrades
    global gold
    global player_level
    global player_xp
    global character
    global inventory
    global cloak
    global burn
    global in_battle
    global knights
    global encountered_town
    global encountered_troll
    global encountered_library
    global encountered_tavern
    global encountered_alchemist
    global encountered_blacksmith
    global boss_fight

    # Resets all variables to their default state.
    area = 0
    checkpoint = 0
    upgrades = 0
    gold = 0
    player_level = 1
    player_xp = 0
    character = ""
    inventory = ["(B)ack"]
    cloak = 0
    burn = False
    in_battle = False
    knights = False
    encountered_town = False
    encountered_troll = False
    encountered_library = False
    encountered_tavern = False
    encountered_alchemist = False
    encountered_blacksmith = False
    boss_fight = False
    
    if ask_play_game():
        explain_game()
        get_user_name()
        character = choose_character()
        play_intro(character)
        show_inventory(character)  # Show the character's inventory
        confirm()
    else:
        print_pause('No problem, maybe next time!')
        menu()


print("""

 ▓█████▄  ██▀███   ▄▄▄      ▄████  ▒█████   ███▄    █ 
 ▒██▀ ██▌▓██ ▒ ██▒▒████▄    ██▒ ▀█▒██▒  ██▒ ██ ▀█   █ 
 ░██   █▌▓██ ░▄█ ▒▒██  ▀█▄ ▒██░▄▄▄▒██░  ██▒▓██  ▀█ ██▒
▒░▓█▄   ▌▒██▀▀█▄  ░██▄▄▄▄██░▓█  ██▒██   ██░▓██▒  ▐▌██▒
░░▒████▓ ░██▓ ▒██▒▒▓█   ▓██▒▓███▀▒░ ████▓▒░▒██░   ▓██░
░ ▒▒▓  ▒ ░ ▒▓ ░▒▓░░▒▒   ▓▒█░▒   ▒ ░ ▒░▒░▒░ ░ ▒░   ▒ ▒ 
  ░ ▒  ▒   ░▒ ░ ▒ ░ ░   ▒▒  ░   ░   ░ ▒ ▒░ ░ ░░   ░ ▒░
  ░ ░  ░   ░░   ░   ░   ▒   ░   ░ ░ ░ ░ ▒     ░   ░ ░ 
    ░       ░           ░       ░     ░ ░           ░ 

  ██████   ██▓    ▄▄▄     ▓██   ██▓ ▓█████ ██▀███  
▒██    ▒  ▓██▒   ▒████▄    ▒██  ██▒ ▓█   ▀▓██ ▒ ██▒
░ ▓██▄    ▒██░   ▒██  ▀█▄   ▒██ ██░ ▒███  ▓██ ░▄█ ▒
  ▒   ██▒ ▒██░   ░██▄▄▄▄██  ░ ▐██▓░ ▒▓█  ▄▒██▀▀█▄  
▒██████▒▒▒░██████▒▓█   ▓██  ░ ██▒▓░▒░▒████░██▓ ▒██▒
▒ ▒▓▒ ▒ ░░░ ▒░▓  ░▒▒   ▓▒█   ██▒▒▒ ░░░ ▒░ ░ ▒▓ ░▒▓░
░ ░▒  ░  ░░ ░ ▒  ░ ░   ▒▒  ▓██ ░▒░ ░ ░ ░    ░▒ ░ ▒ 
░  ░  ░     ░ ░    ░   ▒   ▒ ▒ ░░      ░    ░░   ░ 
      ░  ░    ░        ░   ░ ░     ░   ░     ░     

""")

menu()