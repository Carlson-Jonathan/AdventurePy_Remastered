class Player:
	def __init__(self):
		self.name = "Anonymous"
		self.weapons = {"Fists"}
		self.equipped_weapon = "Fists"
		self.maximum_health = 100
		self.health = 100
		self.is_dead = False
		self.trolls_blood = 0
		self.invisibility_potions = 0
		self.monsters_killed = 0
		self.has_compass = False
		self.has_map = False
		self.has_magic_ring = False
		self.treasure_keys = 0

	def modify_health(self, adjustment):
		adjustment = int(adjustment / 3 * 2) if self.has_magic_ring else adjustment
		self.health += adjustment
		self.health = min(self.health, self.maximum_health)
		self.health = max(self.health, 0)

	def check_for_death(self):
		self.is_dead = bool(self.health <= 0)
		return f"Having lost all health, {self.name} falls lifeless to the ground." if self.is_dead else ""
	
	# For serializing the object for json (saving games)
	def to_dict(self):
		return {
			"name": self.name,
			"weapons": list(self.weapons),
			"equipped_weapon": self.equipped_weapon,
			"health": self.health,
			"maximum_health": self.maximum_health,
			"trolls_blood": self.trolls_blood,
			"is_dead": self.is_dead,
			"invisibility_potions": self.invisibility_potions,
			"monsters_killed": self.monsters_killed,
			"has_compass": self.has_compass,
			"has_map": self.has_map,
			"has_magic_ring": self.has_magic_ring,
			"treasure_keys": self.treasure_keys
		}