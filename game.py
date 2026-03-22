#game.py
#Xander Bergman
#3/21/206

import gamefunctions

num_purchased, leftover_money = gamefunctions.purchase_item(123, 1000, 3)
print(num_purchased)
print(leftover_money)
print()

monster = gamefunctions.new_random_monster()
print(monster["name"])
print(monster["description"])
print(monster["health"])
print(monster["power"])
print(monster["money"])
print()

gamefunctions.print_welcome(input("Enter your name: "), 20)
print()

item1 = input("Enter an item that costs around $1: ")
item2 = input("Enter an item that costs around $20: ")
gamefunctions.print_shop_menu(item1, 1, item2, 20)
