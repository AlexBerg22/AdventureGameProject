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
import pygame #for drawing the game map
    
#check for savedata in the current working directory
#if none is found, initializes state dict. with default values
if "adventure_savedata.json" not in os.listdir():
    name = gamefunctions.get_name()
    state = {
    "player_name": name,
    "player_max_health": 100,
    "player_health": 100,
    "player_gold": 1000,
    "base_power": 10,
    "current_power": 10,
    "inventory": [],
    "map_state": {
        "player_pos": {"x": 0, "y": 0},
        "town_pos": {"x": 0, "y": 0},
        "monster_pos": {"x": 8, "y": 8}
        }
    }

#if savedata is found, asks user if they want to load save or start a new game
else:
    print("Would you like to continue from previous save?")
    print("1) Continue \n2) New Game")
    while True:
        user_action = input()
        #if user chooses to continue, loads state dict. from save file
        if user_action == "1":
            with open("adventure_savedata.json", "r") as savedata:
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
            "inventory": [],
            "map_state": {
                "player_pos": {"x": 0, "y": 0},
                "town_pos": {"x": 0, "y": 0},
                "monster_pos": {"x": 8, "y": 8}
                }
            }
            break
        else:
            print("Unrecognized command.")

user_action = "0"

gamefunctions.print_welcome(state["player_name"], 20)
#main gameplay loop that runs until the user choses the option to quit
while True: 
    #prints give the player info and shows their options
    print(f"\nYou are currently in town.")
    print(f"Current HP: {state['player_health']}, Current Gold: {state['player_gold']}")
    print("What would you like to do?\n")
    print("1) Explore \n2) Visit shop (purchase items) \n3) Equip Items \n4) Rest at inn \n5) Save & Quit")
    user_action = input()
    if user_action == "1":
        exploring = True
        while exploring:
            result = gamefunctions.explore_map(state)
            if result == "monster":
                monster = gamefunctions.new_random_monster()
                gamefunctions.fight_monster_loop(state, monster)
                gamefunctions.respawn_monster(state)
                if state["player_health"] <= 0:
                    state["map_state"]["player_pos"] = {"x": 0, "y": 0}
                    print("Thankfully, someone found you and brought you back to town.")
                    result = "town"
            if result == "town":
                exploring = False
            elif result == "quit":
                exploring = False
    elif user_action == "2":
        #runs the store loop
        state = gamefunctions.buy_stuff(state)
    elif user_action == "3":
        #runs the equip items loop
        state = gamefunctions.equip_items(state)
    elif user_action == "4":
        #runs the inn loop
        state = gamefunctions.rest_at_inn(state)
    elif user_action == "5":
        #on exit, export the current state dictionary to save file
        with open("adventure_savedata.json", "w") as savedata:
            json.dump(state, savedata)
        print("Game saved!")
        break
    else:
        #if user command is invalid, sends a message then repeats the loop
        print("Unrecognized command.")
        
#when main loop is terminated, prints a goodbye message
print("Thanks for playing!")
