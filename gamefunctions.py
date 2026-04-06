"""Defines 4 different game functions for a several purposes.

purchase_item allows the user to buy items.
new_random_monster randomly generates a monster with unique stats.
print_welcome prints a centered welcome message for the user.
print_shop_menu prints a sign displaying two items and their prices.
get_total_stats updates the player's current power when needed.
fight_input gets the players action for fight_monster_loop.
"""

#gamefunctions.py
#Xander Bergman
#2/28/2026

#random numbers are required for monster generation so random is imported
import random

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
        monster (dict): Generated from gamefunctions.new_random_monster

    Returns:
        action (str): The player's selected action.
    """
    #prints display information and options to the player
    print(f"\nYour HP: {state["player_health"]}, {monster["name"]} HP: {monster["health"]}")
    print("What would you like to do?\n")
    print("1) Fight \n2) Use Bomb \n3) Run away")
    #gets and returns the player's action
    return input()

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
