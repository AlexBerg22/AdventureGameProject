"""A simple game that allows the player to fight monsters.

Allows for saving & loading game data.
Gameplay loops until the player decides to quit.
"""

#game.py
#Xander Bergman
#3/21/206

import gamefunctions #gets the functions from gamefunctions for later use
import json #for save data management
import os #for checking status of save file
import pygame #for drawing the game map
from WanderingMonster import WanderingMonster #get the WanderingMonster class
from playsound3 import playsound #for playing sounds

#tries to force the working directory to be where the game.py file is located
#this is necessary for playing sounds from the sounds foler
try:
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
except Exception as e:
    print(f"Path error: {e}")

main_music = playsound("sounds/main-music.mp3", block=False)
#check for savedata in the current working directory
#if none is found, initializes state dict. with default values
if "adventure_savedata.json" not in os.listdir():
    name = gamefunctions.get_name()
    player_x, player_y = 0, 0
    town_x, town_y = 0, 0
    initial_monster = WanderingMonster.random_spawn([], [(player_x, player_y), (town_x, town_y)], 10, 10)
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
        "trees": [{"x": 5, "y": 5},{"x": 3, "y": 7},{"x": 7, "y": 2}, {"x": 4, "y": 3}, {"x": 2, "y": 2}]
        },
    "monsters": [initial_monster]
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
                state["monsters"] = [WanderingMonster.from_dict(mon) for mon in state["monsters"]]
            break
        #if user chooses new game, initilizes state dict. with default values
        elif user_action == "2":
            name = gamefunctions.get_name()
            player_x, player_y = 0, 0
            town_x, town_y = 0, 0
            initial_monster = WanderingMonster.random_spawn([], [(player_x, player_y), (town_x, town_y)], 10, 10)
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
                "trees": [{"x": 5, "y": 5},{"x": 3, "y": 7},{"x": 7, "y": 2}, {"x": 4, "y": 3}, {"x": 2, "y": 2}]
                },
            "monsters": [initial_monster]
            }
            break
        else:
            print("Unrecognized command.")

gamefunctions.print_welcome(state["player_name"], 20)
#main gameplay loop that runs until the user choses the option to quit
while True:
    if not main_music.is_alive():
        main_music = playsound("sounds/main-music.mp3", block=False)    
    #prints give the player info and shows their options
    print(f"\nYou are currently in town.")
    print(f"Current HP: {state['player_health']}, Current Gold: {state['player_gold']}")
    print("What would you like to do?\n")
    print("1) Explore \n2) Visit shop (purchase items) \n3) Equip Items \n4) Rest at inn \n5) Save & Quit")
    user_action = input()
    if user_action == "1":
        #stop playing menu music
        main_music.stop()
        #moves the player back to town in case they force quits the map
        state["map_state"]["player_pos"] = {"x": 0, "y": 0}
        exploring = True
        while exploring:
            #find what the player colided with
            result = gamefunctions.explore_map(state)
            #quits the map if the player collides with town
            if result == "town":
                exploring = False
            #quits the loop if the player closes the map
            elif result == "quit":
                exploring = False
            #check if player colided with a monster
            elif isinstance(result, WanderingMonster):
                #find what happened during combat
                outcome = gamefunctions.fight_monster_loop(state, result)
                if outcome == "player_fainted":
                    state["map_state"]["player_pos"] = {"x": 0, "y": 0}
                    print("Thankfully, someone found you and brought you back to town.")
                    exploring = False
                elif outcome == "monster_defeated":
                    #if monster is defeated, remove it from monsters list
                    state["monsters"].remove(result)
                    #if there's no monsters left, spawn two new ones
                    if len(state["monsters"]) == 0:
                        player_pos = (state["map_state"]["player_pos"]["x"], state["map_state"]["player_pos"]["y"])
                        forbidden = [(state["map_state"]["town_pos"]["x"], state["map_state"]["town_pos"]["y"])]
                        for tree in state["map_state"]["trees"]:
                            forbidden.append((tree["x"],tree["y"]))
                        mon_1 = WanderingMonster.random_spawn([player_pos], forbidden, 10, 10)
                        mon_2 = WanderingMonster.random_spawn([player_pos, (mon_1.x, mon_1.y)], forbidden, 10, 10)
                        state["monsters"].extend([mon_1, mon_2])
    elif user_action == "2":
        main_music.stop()
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
        save_state = state.copy()
        save_state["monsters"] = [mon.to_dict() for mon in state["monsters"]]
        with open("adventure_savedata.json", "w") as savedata:
            json.dump(save_state, savedata)
        print("Game saved!")
        break
    else:
        #if user command is invalid, sends a message then repeats the loop
        print("Unrecognized command.")
main_music.stop()        
#when main loop is terminated, prints a goodbye message
print("Thanks for playing!")
