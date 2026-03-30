"""A simple game that allows the player to fight monsters.


fight_input displays the options for the user while fighting
and shows their current health.
fight_monster_loop creats a loop that lets the player fight a monster.
buy_stuff uses the print_shop_menu and purchase_item functions
from gamefunctions.py to allow the player to see and purchase 2
different items."""

#game.py
#Xander Bergman
#3/21/206

#gets the functions from gamefunctions for later use
import gamefunctions

#defines a number of variables for later use
player_health = 100
player_gold = 10
player_power = 10
user_action = 0

#three functions that update or reference game.py variables are created here
#this keeps the code in the main game loop organized while avoiding variable errors
def fight_input():
    """
    Provides the player with information during fights and gets their action.

    Parameters:
        None

    Returns:
        action (str): The player's selected action.

    """
    #global variables are used to update the players stats outside of the function
    global player_health, player_gold, player_power, monster
    #prints display information and options to the player
    print(f"Your HP: {player_health}, Monster HP: {monster["health"]}")
    print("What would you like to do?\n")
    print("1) Fight \n2) Run away")
    #gets the player's action
    action = input()
    return action

def fight_monster_loop():
    """Creats a loop where the player fights a monster.

    Parameters:
        None
        
    Returns:
        None
    """
    #global variables are used to update the players stats outside of the function
    global player_health, player_gold, player_power, monster
    print(f"You encounter a wild {monster["name"]}!")
    #while loops ends when either the player or monster dies
    while player_health > 0 and monster["health"] > 0:
        user_action = fight_input()
        if user_action == "1":
            monster["health"] -= player_power
            player_health -= monster["power"]
        elif user_action == "2":
            user_action = "0"
            print("You ran away!\n")
            break #exits the fight loop and returns the player to the main loop
        else:
            #if user command is invalid, sends a message then repeats the loop
            print("Unrecognized command.\n")
    #if-else statements check the two cases that cause the loop to end
    if player_health <= 0:
        player_health = 0 #prevents player_health from appearing as negative
        print("You passed out.\n")
    elif monster["health"] <= 0:
        print("You defeated the monster!\n")
        player_gold += monster["money"]

def buy_stuff():
    """
    Uses functions in gamefunctions to display and allow the player to purchase items.

    Parameters:
        None

    Returns:
        None
    """
    #global variables are used to edit the players stats outside of the function
    global user_action
    global player_gold
    #num_purchased is defined so it can be set later
    num_purchased = 0
    while user_action != "3": #keeps the player in the store until they choose to leave
        #prints a sign displaying item options to the player
        gamefunctions.print_shop_menu("Apple", 10, "Healing Pot.", 25)
        print("What would you like to buy?\n")
        print("1) Apple \n2) Healing Potion \n3) Nothing (Leave) ")
        user_action = input()
        #if-else statments check which item the player purchased, then subtract its cost from their gold
        if user_action == "1":
            num_purchased, player_gold = gamefunctions.purchase_item(10, player_gold)
            print(f"You purchased {num_purchased} apple(s). You have {player_gold} gold left.")
        elif user_action == "2":
            num_purchased, player_gold = gamefunctions.purchase_item(25, player_gold)
            print(f"You purchased {num_purchased} healing potion(s). You have {player_gold} gold left.")
        elif user_action == "3":
            user_action = "0"
            print("You left the store.")
            break #exits the store loop and returns the player to the main loop
        else:
            print("Unrecognised command.")

#main gameplay loop that runs until the user choses the option to quit
while user_action != "3": 
    #prints give the player info and shows their options
    print(f"You are currently in town.")
    print(f"Current HP: {player_health}, Current Gold: {player_gold}")
    print("What would you like to do?\n")
    print("1) Leave town (fight monster) \n2) Visit shop (purchase items) \n3) Quit")
    user_action = input()
    if user_action == "1":
        monster = gamefunctions.new_random_monster()
        fight_monster_loop()
        user_action = 0 #makes sure the main while loop runs regardless of the player's last input
    elif user_action == "2":
        #runs the store loop
        buy_stuff()
        user_action = 0
    elif user_action != "3":
        #if user command is invalid, sends a message then repeats the loop
        print("Unrecognized command.\n")
        
#when main loop is terminated, prints a goodbye message
print("Thanks for playing!")



            
