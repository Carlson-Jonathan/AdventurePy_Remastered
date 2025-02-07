import random

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
		self.base_combat_damage = 5
		self.save_scum = 0
		self.battles_fled = 0
		self.health_potions_drank = 0

	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~		

	def modify_health(self, adjustment):
		if adjustment < 0:
			adjustment = int(adjustment / 3 * 2) if self.has_magic_ring else adjustment
		self.health += adjustment
		self.health = min(self.health, self.maximum_health)
		self.health = max(self.health, 0)

	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~		

	def check_for_death(self):
		self.is_dead = bool(self.health <= 0)
		return f"Having lost all health, {self.name} falls lifeless to the ground." if self.is_dead else ""
	
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	
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
			"treasure_keys": self.treasure_keys,
			"base_combat_damage": self.base_combat_damage,
			"save_scum": self.save_scum,
			"battles_fled": self.battles_fled,
			"health_potions_drank": self.health_potions_drank
		}

	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	def get_base_damage(self):
		return random.randint(int(self.base_combat_damage * 0.5), self.base_combat_damage * 2)
	
	def get_sword_damage(self):
		return random.randint(15, 25)
	
	def get_staff_damage(self):
		return random.randint(1, 35)
	
	def get_fist_damage(self):
		return random.randint(3, 7)

	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	def get_combat_damage(self):
		damages = {"Fists": self.get_fist_damage, "Sword": self.get_sword_damage, "Staff": self.get_staff_damage}
		return self.get_base_damage() + damages[self.equipped_weapon]()

	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	def apply_regeneration(self):
		message = ""
		if self.trolls_blood > 0:
			regen = self.trolls_blood * random.randint(2, 5)
			self.modify_health(regen)
			message = f"{self.name} regenerates {regen} health!"
		return message

	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
