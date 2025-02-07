import random

def generate_monster():
    monster_names = ["bug", "slime", "drake", "skeleton", "wasp"]
    name = monster_names[random.randint(0, len(monster_names) - 1)]
    health = random.randint(60, 120)
    min_damage = random.randint(5, 15)
    max_damage = random.randint(20, 30)
    evasion = random.randint(1, 10)
    accuracy = random.randint(1, 10)
    return Monster(name, health, min_damage, max_damage, evasion, accuracy)

class Monster:
    def __init__(self, name, health, min_damage, max_damage, evasion, accuracy): 
        self.name = name
        self.health = health
        self.min_damage = min_damage
        self.max_damage = max_damage
        self.evasion = evasion
        self.accuracy = accuracy