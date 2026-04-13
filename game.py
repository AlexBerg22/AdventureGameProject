"""A simple game that allows the player to fight monsters.

fight_monster_loop creats a loop that lets the player fight a monster.
buy_stuff uses the print_shop_menu and purchase_item functions
from gamefunctions.py to allow the player to see and purchase 2
different items.
rest_at_inn allows the player to spend gold to refill their HP.
"""

#game.py
#Xander Bergman
#3/21/206

import gamefunctions #gets the functions from gamefunctions for later use
import json #for save data management
import os #for checking status of save file

#check for savedata in the current working directory
#if none is found, initializes state dict. with default values
if "savedata.json" not in os.listdir():
    name = gamefunctions.get_name()
    state = {
    "player_name": name,
    "player_max_health": 100,
    "player_health": 100,
    "player_gold": 1000,
    "base_power": 10,
    "current_power": 10,
    "inventory": []
    }

#if savedata is found, asks user if they want to load save or start a new game
else:
    print("Would you like to continue from previous save?")
    print("1) Continue \n2) New Game")
    while True:
        user_action = input()
        #if user chooses to continue, loads state dict. from save file
        if user_action == "1":
            with open("savedata.json", "r") as savedata:
                state = json.load(savedata)
            break
        #if user chooses new game, initilizes state dict. with default values
        elif user_action == "2":
            name = gamefunctions.get_name()
            state = {
            "player_name": name,
            "player_max_health": 100,
            "player_health": 100,
            "player_gold": 1000,
            "base_power": 10,
            "current_power": 10,
            "inventory": []
            }
            break
        else:
            print("Unrecognized command.")

user_action = "0"

#loop functions are defined here to keep the main gameplay loop readable
def fight_monster_loop(monster):
    """Creats a loop where the player fights a monster.

    Parameters:
        monster (dict): Generated from gamefunctions.new_random_monster

    Retruns:
        None
    """
    print(f"\nYou encounter a wild {monster["name"]}!")
    #while loops ends when either the player or monster dies
    while state["player_health"] > 0 and monster["health"] > 0:
        gamefunctions.get_total_stats(state)
        fight_action = gamefunctions.fight_input(state, monster)
        if fight_action == "1":
            #check for an equipped weapon
            for item in state["inventory"]:
                #if found, reduce its durability
                if item.get("equipped") and item.get("type") == "weapon":
                    item["durability"] -= 1
                    #if it breaks, remove it and reset player power
                    if item["durability"] <= 0:
                        print(f"Your {item["name"]} broke!")
                        state["inventory"].remove(item)
                        state["current_power"] = state["base_power"]
                    else:
                        print(f"Weapon durability: {item["durability"]}")
                    break
            monster["health"] -= state["current_power"]
            #if monster dies, it doesn't hurt the player
            if monster["health"] > 0:
                state["player_health"] -= monster["power"]
        elif fight_action == "2":
            #bomb_found defaults to false, then check to see if player has one
            bomb_found = False
            for item in state["inventory"]:
                #if they do, immediately defeat the monster and remove bomb from inventory
                if item["name"] == "bomb":
                    print("\nYou threw a bomb!")
                    monster["health"] = 0
                    state["inventory"].remove(item)
                    bomb_found = True
                    break
            if not bomb_found:
                    print("\nYou don't have a bomb to throw!")
        elif fight_action == "3":
            print("\nYou ran away!")
            break #exits the fight loop and returns the player to the main loop
        else:
            #if user command is invalid, sends a message then repeats the loop
            print("Unrecognized command.\n")
    #if-else statements check the two cases that cause the loop to end
    if state["player_health"] <= 0:
        state["player_health"]= 0 #prevents player_health from appearing as negative
        print("You passed out.")
    elif monster["health"] <= 0:
        print("You defeated the monster!")
        state["player_gold"] += monster["money"]

def buy_stuff():
    """
    Uses functions in gamefunctions to display and allow the player to purchase items.
    """
    shop_action = "0"
    while shop_action != "3": #keeps the player in the store until they choose to leave
        #prints a sign displaying item options to the player
        print()
        gamefunctions.print_shop_menu("Sword", 100, "Bomb", 50)
        print(f"\nYou currently have {state["player_gold"]} gold.")
        print("What would you like to buy?\n")
        print("1) Sword \n2) Bomb \n3) Nothing (Leave) ")
        shop_action = input()
        #if-else statments check which item the player purchased, then subtract its cost from their gold
        if shop_action == "1":
            num, state["player_gold"] = gamefunctions.purchase_item(100, state["player_gold"])
            if num > 0:
                #add a sword dictionary to inventory
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
            num, state["player_gold"] = gamefunctions.purchase_item(50, state["player_gold"])
            if num > 0:
                #add a bomb dictionary to inventory
                state["inventory"].append({"name": "bomb", "type": "consumable"})
                print(f"\nYou purchased a bomb! You have {state["player_gold"]} gold left.")
            else:
                print("\nNot enough gold!")
        elif shop_action == "3":
            print("\nYou left the store.")
            break #exits the store loop and returns the player to the main loop
        else:
            print("\nUnrecognised command.")

def equip_items():
    """
    Runs a loop that allows the player to equip/unequip items.
    Filters by type so the user only sees relevant items at one time.
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
                        print(f"You equipped the {selected_item['name']}!")
                    else:
                        selected_item["equipped"] = False
                        print(f"You unequipped the {selected_item['name']}.")
                #if they chose the "Back" option
                elif idx == len(relevant_items):
                    break 
                else:
                    print("Unrecognized command.")
            else:
                print("Please enter a number.")

def rest_at_inn():
    """
    Allows the player to pay gold to reset their health to their max HP.
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
                    break #return to main loop since player won't have any other actions here
                else:
                    state["player_gold"] -= 10
                    state["player_health"] = state["player_max_health"]
                    print("\nYou awake feeling refreshed!")
                    break
        elif inn_action != "2":
            print("\nUnrecognized command")
    print("\nYou leave the inn.")

gamefunctions.print_welcome(state["player_name"], 20)
#main gameplay loop that runs until the user choses the option to quit
while True: 
    #prints give the player info and shows their options
    print(f"\nYou are currently in town.")
    print(f"Current HP: {state['player_health']}, Current Gold: {state['player_gold']}")
    print("What would you like to do?\n")
    print("1) Leave town (fight monster) \n2) Visit shop (purchase items) \n3) Equip Items \n4) Rest at inn \n5) Save & Quit")
    user_action = input()
    if user_action == "1":
        monster = gamefunctions.new_random_monster()
        fight_monster_loop(monster)
    elif user_action == "2":
        #runs the store loop
        buy_stuff()
    elif user_action == "3":
        equip_items()
    elif user_action == "4":
        rest_at_inn()
    elif user_action == "5":
        #on exit, export the current state dictionary to save file
        with open("savedata.json", "w") as savedata:
            json.dump(state, savedata)
        print("Game saved!")
        break
    else:
        #if user command is invalid, sends a message then repeats the loop
        print("Unrecognized command.")
        
#when main loop is terminated, prints a goodbye message
print("Thanks for playing!")
