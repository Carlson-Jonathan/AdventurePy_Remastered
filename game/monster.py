import random

def generate_monster():
    monster_names = ["bug", "slime", "drake", "skeleton", "wasp"]
    name = monster_names[random.randint(0, len(monster_names) - 1)]
    max_health = random.randint(60, 120)
    health = max_health
    min_damage = random.randint(5, 15)
    max_damage = random.randint(20, 30)
    evasion = random.randint(1, 10)
    accuracy = random.randint(1, 10)
    return Monster(name, max_health, min_damage, max_damage, evasion, accuracy)

class Monster:
    def __init__(self, name, max_health, min_damage, max_damage, evasion, accuracy): 
        self.name = name
        self.max_health = max_health
        self.health = max_health
        self.min_damage = min_damage
        self.max_damage = max_damage
        self.evasion = evasion
        self.accuracy = accuracy

    def get_monster_damage(self):
        return random.randint(self.min_damage, self.max_damage)