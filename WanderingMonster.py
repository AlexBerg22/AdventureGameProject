"""Defines the class WanderingMonster with several functions.

random_spawn creates a new monster at a random location.
from_dict imports monster data from state dict.
to_dict returns monster data in JSON format.
move moves the monster in a random direction, with restrictions.
"""

#WanderingMonster.py
#Xander Bergman
#4/24/2026
import random, gamefunctions

class WanderingMonster:
    def __init__(self, x, y, mon_type, color, hp, power, gold):
        """Initializes a class object with a number of variables.
        Parameters:
            x (int): The x position of the monster
            y (int): The y position of the monster
            mon_type (str): The type of monster
            hp (int): The current health of the monster
            power (int): The power of the monster
            gold (int): The amount of gold on the monster
        Returns:
            None
        """
        self.x = x
        self.y = y
        self.mon_type = mon_type
        self.color = color
        self.health = hp
        self.power = power
        self.gold = gold
    @classmethod
    def random_spawn(cls, occupied, forbidden, grid_w, grid_h):
        """Creates a new WanderingMonster object at a random location.
        Parameters:
            occupied (list): All spaces occupied by moving objects
            forbidden (list): All spaces occupied by non-moving objects
            grid_w (int): The width of the map grid
            grid_h (int): The height of the map grid
        Returns:
            None
        """
        while True:
            rand_x = random.randint(0, grid_w - 1)
            rand_y = random.randint(0, grid_h - 1)
            if (rand_x, rand_y) not in occupied and (rand_x, rand_y) not in forbidden:
                monster = gamefunctions.new_random_monster()
                monster_color = (200, 0, 0)
                return cls(
                    rand_x,
                    rand_y,
                    monster["name"],
                    monster_color,
                    monster["health"],
                    monster["power"],
                    monster["money"]
                    )
    @classmethod        
    def from_dict(cls, data):
        """Converts a monster stored in a dict. to a class object.
        Parameters:
            data (dict): The data for a saved monster
        Returns:
            A wandering monster object with the attributes from data.
        """
        return cls(
            data["x"],
            data["y"],
            data["mon_type"],
            data["color"],
            data["health"],
            data["power"],
            data["gold"]
            )
    
    def to_dict(self):
        """Converts a monster object into a saveable dictionary.
        Parameters
            self (obj): The object being converted
        Returns:
            A dictionary containing the attributes from self.
        """
        return {
            "x": self.x,
            "y": self.y,
            "mon_type": self.mon_type,
            "color": self.color,
            "health": self.health,
            "power": self.power,
            "gold": self.gold
            }
    
    def move(self, occupied, forbidden, grid_w, grid_h):
        """Attempts to move the monster to a new nearby position.
        Parameters:
            occupied (list): All spaces occupied by moving objects
            forbidden (list): All spaces occupied by non-moving objects
            grid_w (int): The width of the map grid
            grid_h (int): The height of the map grid
        Returns:
            None
        """
        directions = [(0,1), (0,-1), (1,0), (-1,0)]
        x, y = random.choice(directions)
        new_x = self.x + x
        new_y = self.y + y
        if (0 <= new_x < grid_w) and (0 <= new_y < grid_h):
            if (new_x, new_y) not in occupied and (new_x, new_y) not in forbidden:
                self.x = new_x
                self.y = new_y
                return
        return
