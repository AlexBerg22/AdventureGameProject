"""Defines 4 different game functions for a several purposes.

purchase_item allows the user to buy items.
new_random_monster randomly generates a monster with unique stats.
print_welcome prints a centered welcome message for the user.
print_shop_menu prints a sign displaying two items and their prices.
get_total_stats updates the player's current power when needed.
fight_input gets the players action for fight_monster_loop.
get_name gets the player's name it is under a certain length.
fight_monster_loop creats a loop that lets the player fight a monster.
buy_stuff uses the print_shop_menu and purchase_item functions
from gamefunctions.py to allow the player to see and purchase 2
different items.
rest_at_inn allows the player to spend gold to refill their HP.
move_player updates the player's position in map_state in place.
respawn_monster moves the monster to a new random location on the map.
explore_map continually draws a map using the game state as reference.
"""

#gamefunctions.py
#Xander Bergman
#2/28/2026

#random numbers are required for monster generation so random is imported
import random, pygame, time
from playsound3 import playsound
from WanderingMonster import WanderingMonster

def purchase_item(itemPrice,startingMoney,quantityToPurchase=1):
    """
    Allows the user to buy items and automatically subtracts their cost.

    Parameters: 
        itemPrice (int): Cost of the item to be purchased.
        startingMoney (int): Amount of money the user has.
        quantityToPurchase (int): Number of item to purchase (default 1).

    Returns: 
        num_purchased (int): The number of items successfully purchased.
        leftover_money (int): The amout of money the user has leftover.
    """
    #if-else function ensures you cannot buy more items than you can afford
    if (quantityToPurchase) > (startingMoney // itemPrice):
        num_purchased = startingMoney // itemPrice
    else:
        num_purchased = quantityToPurchase
    #once number of purchased items is determined, subtracts the total cost from starting money
    leftover_money = startingMoney - (itemPrice * num_purchased)  
    return (num_purchased, leftover_money)

def new_random_monster():
    """
    Creates a random monster with unique stats from one of four types.

    Parameters: 
        None

    Returns: 
        A dictionary with the following elements:
            name (str)
            health (int)
            description (str)
            power (int)
            money (int)
    """
    #randomly chooses an int 1 - 4, each int corresponds to a monster type 
    rand_monster_type = random.randint(1,4)
    if rand_monster_type == 1:
     #unique 'random.randint's are used after monster type is chosen
     #to generate its stats within a given range
     return {
        "name": "Goblin",
        "description": ("A common neusance. It seems to have ammased some wealth from stealing. "
        "Perhaps you could \"liberate\" this wealth?"),
        "health": random.randint(5,15),
        "power": random.randint(2,5),
        "money": random.randint(25, 100),
        }
    elif rand_monster_type == 2:
      return {
        "name": "Beholder",
        "description": ("They say that beauty is in its eye, but you really don\'t see any. "
        "Behold it while you still can or draw your weapon and fight!"),
        "health": random.randint(75,125),
        "power": random.randint(20,30),
        "money": random.randint(500, 750),
        }
    elif rand_monster_type == 3:
      return {
        "name": "Ancient Dragon",
        "description": ("The better half of D&D approaches! "
        "Ready your weapon and claim the dragon\'s hoard!"),
        "health": random.randint(100,150),
        "power": random.randint(25,30),
        "money": random.randint(800,1200),
        }
    elif rand_monster_type == 4:
       return {
        "name": "Troll",
        "description": "Someone's trying to stir up trouble online! Get them!",
        "health": random.randint(10,20),
        "power": random.randint(5,10),
        "money": random.randint(0,50),
        }

def print_welcome(name, width):
    """
    Prints a centered welcome message with the user\'s name.

    Parameters: 
        name (str): The user\'s name.
        width (int): The width the message should be.

    Returns:
        Prints \'name\' centered at \'width\' between two \' characters.
    """ 
    welcome_message = f"Hello, {name}!"
    print(f"'{welcome_message:^{width}}'")


def print_shop_menu(item1Name, item1Price, item2Name, item2Price):
    """
    Prints a sign displaying 2 purchasable items and their prices.
    
    Parameters: 
        item1Name (str): The name of the first desplayed item.
        item1Price (float): The price of the first desplayed item.
        item2Name (str): The name of the second desplayed item.
        item2Price (float): The price of the second desplayed item.

    Returns: 
        A four line sign with the items aligned on the left and
        the prices aligned on the right.
        Items are framed using -, \\, and / characters.
    """
    #converts the item prices into easier to align strings and rounds them to two decimal places
    item1cost = f"${item1Price:.2f}"
    item2cost = f"${item2Price:.2f}"
    print("/" + "-" * 20 + "\\")
    print(f"|{item1Name:12}{item1cost:>8}|")
    print(f"|{item2Name:12}{item2cost:>8}|")
    print("\\" + "-" * 20 + "/")

def get_total_stats(state):
    """Calculates power based on equipped items.
    Parameters:
        state (dict): The gamestate dictionary

    Returns:
        None
    """
    #power_bonus defaults to 0, then checks for equiped weapon
    power_bonus = 0
    for item in state["inventory"]:
        #if there is an equipped weapon, add its power to base power
        if item.get("equipped"):
            power_bonus += item.get("power_bonus", 0)
    #update state dict with new calculated power
    state["current_power"] = state["base_power"] + power_bonus

def fight_input(state, monster):
    """
    Provides the player with information during fights and gets their action.

    Parameters:
        state (dict): The gamestate dictionary
        monster (obj): A WanderingMonster Object

    Returns:
        action (str): The player's selected action.
    """
    #prints display information and options to the player
    print(f"\nYour HP: {state["player_health"]}, {monster.mon_type} HP: {monster.health}")
    print("What would you like to do?\n")
    print("1) Fight \n2) Use Bomb \n3) Run away")
    #gets and returns the player's action
    return input()

def get_name():
    """
    Gets the player's name and ensures that it is under a certain length.

    Parameters:
        None

    Returns:
        name (str): The player's name (<20 characters)
    """
    name = input("Please enter your name:\n")
    while len(name) > 20:
        name = input("Name is too long, please enter a name less than 20 characters: ")
    return name

def fight_monster_loop(state, monster):
    """Creats a loop where the player fights a monster.

    Parameters:
        state (dict): The gamestate dictionary
        monster (obj): A WanderingMonster Object

    Retruns:
        A string describing what happened
    """
    print(f"\nYou encounter a wild {monster.mon_type}!")
    #while loops ends when either the player or monster dies
    battle_music = playsound("sounds/battle-music.mp3", block=False)
    while state["player_health"] > 0 and monster.health > 0:
        if not battle_music.is_alive():
            battle_music = playsound("sounds/battle-music.mp3", block=False)
        get_total_stats(state)
        fight_action = fight_input(state, monster)
        if fight_action == "1":
            #check for an equipped weapon
            for item in state["inventory"]:
                #if found, reduce its durability
                if item.get("equipped") and item.get("type") == "weapon":
                    item["durability"] -= 1
                    #if it breaks, remove it and reset player power
                    if item["durability"] <= 0:
                        print(f"Your {item["name"]} broke!")
                        playsound("sounds/break.mp3")
                        state["inventory"].remove(item)
                        state["current_power"] = state["base_power"]
                    else:
                        print(f"Weapon durability: {item["durability"]}")
                    break
            playsound("sounds/battle-hit.mp3", block=False)
            monster.health -= state["current_power"]
            #if monster dies, it doesn't hurt the player
            if monster.health > 0:
                state["player_health"] -= monster.power
        elif fight_action == "2":
            #bomb_found defaults to false, then check to see if player has one
            bomb_found = False
            for item in state["inventory"]:
                #if they do, immediately defeat the monster and remove bomb from inventory
                if item["name"] == "bomb":
                    print("\nYou threw a bomb!")
                    playsound("sounds/explosion.mp3")
                    monster.health = 0
                    state["inventory"].remove(item)
                    bomb_found = True
                    break
            if not bomb_found:
                    print("\nYou don't have a bomb to throw!")
                    playsound("sounds/battle-bomb-fail.mp3", block=False)
        elif fight_action == "3":
            battle_music.stop()
            print("\nYou ran away!")
            playsound("sounds/battle-flee.mp3")
            break
        else:
            #if user command is invalid, sends a message then repeats the loop
            print("Unrecognized command.\n")
    #if-else statements check the two cases that cause the loop to end
    if state["player_health"] <= 0:
        state["player_health"]= 0 #prevents player_health from appearing as negative
        battle_music.stop()
        print("You passed out...")
        playsound("sounds/player-dies.mp3")
        return "player_fainted"
    elif monster.health <= 0:
        battle_music.stop()
        print("You defeated the monster!")
        playsound("sounds/battle-win.mp3")
        state["player_gold"] += monster.gold
        return "monster_defeated"

def buy_stuff(state):
    """
    Uses functions in gamefunctions to display and allow the player to purchase items.

    Parameters:
        state (dict): The gamestate dictionary
        
    Returns:
        state (dict): Updates the gamestate dictionary
    """
    shop_action = "0"
    shop_music = playsound("sounds/shop-music.mp3", block=False)
    while shop_action != "3": #keeps the player in the store until they choose to leave
        if not shop_music.is_alive():
            shop_music = playsound("sounds/shop-music.mp3", block=False)
        #prints a sign displaying item options to the player
        print()
        print_shop_menu("Sword", 100, "Bomb", 50)
        print(f"\nYou currently have {state["player_gold"]} gold.")
        print("What would you like to buy?\n")
        print("1) Sword \n2) Bomb \n3) Nothing (Leave) ")
        shop_action = input()
        #if-else statments check which item the player purchased, then subtract its cost from their gold
        if shop_action == "1":
            num, state["player_gold"] = purchase_item(100, state["player_gold"])
            if num > 0:
                #add a sword dictionary to inventory
                playsound("sounds/purchase.mp3", block=False)
                state["inventory"].append({
                    "name": "sword", 
                    "type": "weapon", 
                    "power_bonus": 5,
                    "durability": 10,
                    "equipped": False
                })
                print(f"\nYou purchased a sword! You have {state["player_gold"]} gold left.")
            else:
                print("\nNot enough gold!")
        elif shop_action == "2":
            num, state["player_gold"] = purchase_item(50, state["player_gold"])
            if num > 0:
                #add a bomb dictionary to inventory
                playsound("sounds/purchase.mp3", block=False)
                state["inventory"].append({"name": "bomb", "type": "consumable"})
                print(f"\nYou purchased a bomb! You have {state["player_gold"]} gold left.")
            else:
                print("\nNot enough gold!")
        elif shop_action == "3":
            shop_music.stop()
            print("\nYou left the store.")
            return state
            #exits the store loop and returns the player to the main loop
        else:
            print("\nUnrecognised command.")

def equip_items(state):
    """
    Runs a loop that allows the player to equip/unequip items.
    Filters by type so the user only sees relevant items at one time.

    Parameters:
        state (dict): The gamestate dictionary
        
    Returns:
        state (dict): Updates the gamestate dictionary
    """
    #outer 'main' equip loop
    #runs indefinately until player choses '3' to leave
    while True:
        print("\nWhat type of item would you like to equip?")
        print("1) Weapons \n2) Armor \n3) Nothing") 
        category = input()
        target_type = ""
        if category == "1":
            target_type = "weapon"
        elif category == "2":
            target_type = "armor"
        elif category == "3":
            return state
            break
        else:
            print("\nInvalid category.")
            continue
        #inner loop for the specific category
        while True:
            #create a list of only items that match the chosen type
            relevant_items = [item for item in state["inventory"] if item.get("type") == target_type]
            print(f"\nYour {target_type.capitalize()}s:")
            if not relevant_items:
                print(f"\nYou don't have any {target_type}s!")
                break #go back to the category selection
            #display only the relevant items
            for i, item in enumerate(relevant_items):
                status = "[Equipped]" if item.get("equipped") else "[ ]"
                print(f"{i+1}) {status} {item['name']}")
            print(f"{len(relevant_items) + 1}) Back to Categories")
            choice = input(f"Select a {target_type} to equip, or go back:")
            #requires conversion of input into int for list indexing
            if choice.isdigit():
                idx = int(choice) - 1
                #if they chose an item from the list
                if 0 <= idx < len(relevant_items):
                    selected_item = relevant_items[idx]
                    #can only equip one weapon
                    if not selected_item["equipped"]:
                        #unequip all other items of this type first
                        for item in relevant_items:
                            item["equipped"] = False
                        selected_item["equipped"] = True
                        playsound("sounds/equip-item.mp3", block=False)
                        print(f"You equipped the {selected_item['name']}!")
                    else:
                        selected_item["equipped"] = False
                        playsound("sounds/equip-item.mp3", block=False)
                        print(f"You unequipped the {selected_item['name']}.")
                #if they chose the "Back" option
                elif idx == len(relevant_items):
                    break 
                else:
                    print("Unrecognized command.")
            else:
                print("Please enter a number.")

def rest_at_inn(state):
    """
    Allows the player to pay gold to reset their health to their max HP.
    
    Parameters:
        state (dict): The gamestate dictionary
        
    Returns:
        state (dict): Updates the gamestate dictionary
    """
    #same logic as other loops
    print("It cost 10 gold to rest and refill your HP.")
    print(f"You currently have {state["player_health"]}/{state["player_max_health"]} HP and {state["player_gold"]} gold.")
    print("Would you like to rest?")
    print("1) Yes \n2) No")
    #defines inn_action so it can be used as loop variable
    inn_action = "0"
    while inn_action != "2":
        inn_action = input()
        if inn_action == "1":
                #checks to see if player can afford to stay
                if state["player_gold"] < 10:
                    print("\nYou don't have enough money to stay here. The innkeeper kicks you out.")
                    return state #return to main loop since player won't have any other actions here
                else:
                    state["player_gold"] -= 10
                    state["player_health"] = state["player_max_health"]
                    playsound("sounds/hp-refill.mp3", block=False)
                    print("\nYou awake feeling refreshed!")
                    return state
        elif inn_action != "2":
            print("\nUnrecognized command")
    print("\nYou leave the inn.")
    return state

def move_player(state, direction):
    """
    Updates the player's position in map_state in place.
    
    Parameters:
        direction (str): Either "up", "down", "left", or "right"
    Retruns:
        A string saying what happened
    """
    map_state = state["map_state"]
    pos = map_state["player_pos"]

    #create variables for the potential movement location
    new_x, new_y = pos["x"], pos["y"]
    #try to move the player a direction based on parameters
    if direction == "up":    new_y -= 1
    elif direction == "down":  new_y += 1
    elif direction == "left":  new_x -= 1
    elif direction == "right": new_x += 1
    #checks that the new position wouldn't be outside the boundry
    #skips updating the position if it would
    if (0 <= new_x < 10) and (0 <= new_y < 10):
        for tree in map_state["trees"]:
            if new_x == tree["x"] and new_y == tree["y"]:
                playsound("sounds/walk-sound-quiet.mp3", block=False)
                return "moved"
        pos["x"] = new_x
        pos["y"] = new_y
    playsound("sounds/walk-sound-quiet.mp3", block=False)
    return "moved"

def respawn_monster(state):
    """
    Moves the monster to a new random location on the map.

    Parameters:
        state (dict): The gamestate dictionary
    Returns:
        None
    """
    map_data = state["map_state"]
    while True:
        #randomly generates a position
        new_pos = {"x": random.randint(0, 9), "y": random.randint(0,9)}
        #makes sure that the new monster position isn't the same as the town or player
        #if it is, it rolls a new random location until it is in a different spot
        if new_pos != map_data["town_pos"] and new_pos != map_data["player_pos"]:
            map_data["monster_pos"] = new_pos
            break

def explore_map(state):
    """
    Continually draws a map using the game state as reference.
    Runs until the player encounters something (monster/town).

    Parameters:
        state (dict): The gamestate dictionary
    Returns:
        A string containing what the player encountered
        or the WanderingMonster object the player encountered.
    """
    #variables for setup that make the code easier to read
    colors = {"black": (0, 0, 0), "green": (0,200,0), "white": (250,250,250), "red": (200,0,0)}
    grid_size = 32 #Set the size of the grid block
    pygame.init()
    SCREEN = pygame.display.set_mode((320, 320))
    pygame.display.set_caption("World Map")
    map_state = state["map_state"]
    world_music = playsound("sounds/overworld-music.mp3", block=False)
    while True:
        if not world_music.is_alive():
            world_music = playsound("sounds/overworld-music.mp3", block=False)
        #makes sure that the player doesn't encounter something if they didn't move
        direction = None
        #get any user inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                world_music.stop()
                return "quit"
            #look for keypresses
            if event.type == pygame.KEYDOWN:
                #if key is an arrow key, set direction with which arrow key was pressed
                if event.key == pygame.K_UP: direction = "up"
                elif event.key == pygame.K_DOWN:  direction = "down"
                elif event.key == pygame.K_LEFT:  direction = "left"
                elif event.key == pygame.K_RIGHT: direction = "right"
            if direction:
                #use move_player to update player_pos
                move_player(state, direction)
                player_x, player_y = map_state["player_pos"]["x"], map_state["player_pos"]["y"]
                town_x, town_y = map_state["town_pos"]["x"], map_state["town_pos"]["y"]
                #check if player collided with something
                if (player_x, player_y) == (town_x, town_y):
                    pygame.display.quit()
                    world_music.stop()
                    return "town"
                for monster in state["monsters"]:
                    if (player_x, player_y) == (monster.x, monster.y):
                        pygame.display.quit()
                        world_music.stop()
                        return monster
                #attempt to move each monster to unoccupied square
                forbidden = [(town_x, town_y)]
                for tree in map_state["trees"]:
                    forbidden.append((tree["x"],tree["y"]))
                for monster in state["monsters"]:
                    other_monsters = [(mon.x, mon.y) for mon in state["monsters"] if mon != monster]
                    occupied = [(player_x, player_y)] + other_monsters
                    monster.move(occupied, forbidden, 10, 10)
                    
        #fill screen with black
        SCREEN.fill(colors["black"])
        #draw grid outline
        for x in range(10):
            for y in range(10):
                rect = pygame.Rect(x* grid_size , y * grid_size, grid_size, grid_size)
                pygame.draw.rect(SCREEN, colors["green"], rect, 1)
        #draw the town based on its position in the game state
        town_x, town_y = map_state["town_pos"]["x"], map_state["town_pos"]["y"]
        pygame.draw.circle(SCREEN, colors["green"], (town_x *32 + 16, town_y * 32 + 16), 15)
        #draw obsticles
        for tree in map_state["trees"]:
            x, y = tree["x"], tree["y"]
            pygame.draw.polygon(SCREEN, colors["green"], ((x*32+6,y*32+10),(x*32+16,y*32+1),(x*32+26,y*32+10)))
            pygame.draw.polygon(SCREEN, colors["green"], ((x*32+6,y*32+18),(x*32+16,y*32+6),(x*32+26,y*32+18))) 
            pygame.draw.rect(SCREEN, colors["green"], (x*32 + 11, y * 32 + 20, 10, 10))
        #draw all monsters based on their positions in the game state
        for monster in state["monsters"]:
            pygame.draw.circle(SCREEN, monster.color, (monster.x * 32 + 16, monster.y * 32 +16), 15)
        #draw the player based on their position in the game state
        player_x, player_y = map_state["player_pos"]["x"], map_state["player_pos"]["y"]
        pygame.draw.rect(SCREEN, colors["white"], (player_x*32+11, player_y*32+9, 10, 14))
        #update the screen
        pygame.display.flip()

def test_function():
    """
    Runs a test of each function in gamefunctions.py 3 times.

    Parameters: 
        None

    Returns: 
        Each function three seperate times.
        Functions are separated by a newline.
    """
    
    num_purchased, leftover_money = purchase_item(123, 1000, 3)
    print(num_purchased)
    print(leftover_money)
    print()
    num_purchased, leftover_money = purchase_item(341, 2112)
    print(num_purchased)
    print(leftover_money)
    print()
    num_purchased, leftover_money = purchase_item(3141, 2112)
    print(num_purchased)
    print(leftover_money)
    print()
    
    monster = new_random_monster()
    print(monster["name"])
    print(monster["description"])
    print(monster["health"])
    print(monster["power"])
    print(monster["money"])
    print()
    monster = new_random_monster()
    print(monster["name"])
    print(monster["description"])
    print(monster["health"])
    print(monster["power"])
    print(monster["money"])
    print()
    monster = new_random_monster()
    print(monster["name"])
    print(monster["description"])
    print(monster["health"])
    print(monster["power"])
    print(monster["money"])
    print()

    print_welcome("Xander", 20)
    print()
    print_welcome("Ember", 40)
    print()
    print_welcome("Ranger", 15)
    print()

    print_shop_menu("Apple", 31, "Pear", 1.234)
    print()
    print_shop_menu("Egg", .23, "Bag of Oats", 12.34)
    print()
    print_shop_menu("Big Sword", 99.99, "Biger Sword", 100)

if __name__ == "__main__":
    test_function()
