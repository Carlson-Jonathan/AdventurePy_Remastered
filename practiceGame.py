import subprocess
import random
import os

class Player:
	def __init__(self):
		self.name = "Joe"
		self.weapon = "Broad Sword"
		self.__health = 100
		self.is_dead = False

	def set_health(self, adjustment):
		self.__health += adjustment
		self.__health = min(self.__health, 100)
		self.__health = max(self.__health, 0)

	def get_health(self):
		return self.__health
	
	def check_for_death(self):
		self.is_dead = bool(self.__health <= 0)
		return f"Having lost all health, {player.name} falls lifeless to the ground." if self.is_dead else ""


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		
class Utilities:
	def clear_screen():
		command = 'cls' if os.name == 'nt' else 'clear'
		subprocess.call(command, shell=True)

	# ------------------------------------------------------------------------------------

	def get_player_input(prompt, num_options):
		while True:
			player_input = input(prompt)
			if player_input.isdigit() and 0 < int(player_input) <= num_options:
				return int(player_input)
			else:
				print("Invalid input. Try again.")

	# ------------------------------------------------------------------------------------				

	def create_ruler(length = 50, character = '~'):
		return character * length
	
	# ------------------------------------------------------------------------------------
	
	def draw_game_frame(header, scenario, options, outcome, width):
		Utilities.clear_screen()
		Utilities.print_title()
		border = Utilities.create_ruler(width)
		print(
			f"{border}\n"
			f"{header}\n"
			f"{border}\n"
			f"{Utilities.wrap_text(scenario, width)}\n"
			f"{border}\n"
			f"{options}\n"
			f"{border}\n"
			f"{Utilities.wrap_text(outcome, width)}\n"
			f"{border}")
		
	# ------------------------------------------------------------------------------------

	def create_table_header(headers, table_width, stats):
		header_list = [header.strip() for header in headers.split(",")]
		num_columns = len(header_list)
		column_width = table_width // num_columns
		header_row = "".join(header.center(column_width) for header in header_list)
		stats_row = "".join(stat.center(column_width) for stat in stats)
		separator_length = max(len(header_row), len(stats_row))
		separator = Utilities.create_ruler(int(table_width * 0.75), '-').center(table_width)

		return f"{header_row}\n{separator}\n{stats_row}"
	
	# ------------------------------------------------------------------------------------
	
	def wrap_text(text, width):
		words = text.split()
		lines = []
		current_line = ""

		for word in words:
			if len(current_line) + len(word) + 1 > width:
				lines.append(current_line.strip())
				current_line = word
			else:
				current_line += " " + word

		if current_line:
			lines.append(current_line.strip())

		return "\n".join(lines)
	
	# ------------------------------------------------------------------------------------

	def format_options(items):
		result = []
		for i, item in enumerate(items, start = 1):
			result.append(f"\t{i}: {item}")
		return "\n".join(result)
	
	def print_title():
		print('''
	 _           _                _       _   _     _       
	| |         | |              (_)     | | | |   (_)      
	| |     __ _| |__  _   _ _ __ _ _ __ | |_| |__  _  __ _ 
	| |    / _` | '_ \| | | | '__| | '_ \| __| '_ \| |/ _` |
	| |___| (_| | |_) | |_| | |  | | | | | |_| | | | | (_| |
	\_____/\__,_|_.__/ \__, |_|  |_|_| |_|\__|_| |_|_|\__,_|
		   	   __/ |                               
			  |___/  
''')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Game:
	def __init__(self, player: Player, events: 'Game_Events' = None):
		self.player = player
		self.events = events.game_data
		self.display_width = 75

	# ------------------------------------------------------------------------------------

	def perform_event(self, header, event):
		num_options = len(event["options"])
		options = Utilities.format_options(event["options"])

		Utilities.draw_game_frame(header, event["event"], options, event["action"], self.display_width)
		player_input = Utilities.get_player_input("Action: ", num_options)
		random_num = random.randint(0, 8)
		outcome = event[f"selection{player_input}"][random_num](self.player)
		Utilities.draw_game_frame(header, event["event"], options, outcome, self.display_width)

		return player_input
	
	# ------------------------------------------------------------------------------------
	
	def start_game(self):
		while not self.player.is_dead:
			stats = [str(self.player.name), str(self.player.get_health()), str(self.player.weapon)]
			header = Utilities.create_table_header("Name, Health, Weapon", self.display_width, stats)

			player_input = self.perform_event(header, self.events["hallway"])
			input()

			#if(self.player.is_dead):
			events.death(self.display_width)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~				
class Game_Events:
	def __init__(self):
		self.game_data = {
			"hallway": {
				"event": f"{player.name} sees a long corridor. There is a sewer grate about 20 feet ahead.",
				"options": ["Go down the corridor", "Climb down the grate", "Yell for help", "Save Game"],
				"action": f"What will {player.name} do?",
				"selection1": [
					self.monster,
					self.weapon_treasure,
					self.hallway_trap_good,
					self.hallway_trap_bad,
					self.hallway_trap_none,
					self.trip_good,
					self.trip_bad,
					self.trip_none,
					self.nothing
				],
				"selection2": [
					#self.hallway_S2_good,
					#self.hallway_S2_bad,
					#self.hallway_S2_none
				],
				"selection3": [
					#self.hallway_S3_good,
					#self.hallway_S3_bad,
					#self.hallway_S3_none
				]
			}
		}

	# ---------------------------------- Hallway Events ----------------------------------
	def hallway_trap_good(self, player: Player):
		rand_num = random.randint(20, 30)
		player.set_health(rand_num)
		return (f"{player.name} steps on a trap! Oh no!"
			f"\nFirey darts shoot out of the walls, but {player.name} quickly evades them. "
			f"The burning darts illuminate a hole in the wall revealing a stashed potion. "
			f"{player.name} grabs the bottle and drinks it to replenish {rand_num} health.")
	
	def hallway_trap_bad(self, player: Player):
		rand_num = random.randint(20, 30)
		player.set_health(-rand_num)
		death_message = player.check_for_death()
		return (f"{player.name} steps on a trap! Oh no!"
			f"\nFirey darts shoot out of the walls wounding {player.name} and causing {rand_num} reduction in health!"
			f"\n{death_message}")
	
	def hallway_trap_none(self, player: Player):
		return (f"{player.name} steps on a trap! Oh no!"
			f"\n{player.name} braces for sudden pain but the trap appears to have been a dud. Phew!")
	
	def trip_good(self, player: Player):
		rand_num = random.randint(10, 30)
		player.set_health(rand_num)
		return (f"{player.name} trips over a rock!"
			f"\nAfter getting up and dusting off, {player.name} sees that the rock was actually a health potion!"
			f"\n{player.name} quickly grabs and gulps it down regaining {rand_num} health.")
	
	def trip_bad(self, player: Player):
		rand_num = random.randint(1, 20)
		player.set_health(-rand_num)
		death_message = player.check_for_death()
		return (f"{player.name} trips over a rock!"
			f"\n{player.name} face plants into the hard floor and takes {rand_num} damage! Ouch!"
			f"\n{death_message}")
	
	def trip_none(self, player: Player):
		return (f"{player.name} trips over a rock!"
			f"\nFortunately {player.name} landed in some nice soft mud. Every thing is fine.")
	
	# -------------------------------- Sewer Grate Events --------------------------------


	# ----------------------------------- Yelling Events ---------------------------------

	# ------------------------------- Miscellaneous Events -------------------------------
	def monster(self, player: Player):
		return f"A monster jumps out of the darkness!"

	def weapon_treasure(self, player: Player):
		return f"{player.name} finds a weapon!"

	def nothing(self, player: Player):
		return (f"Well that didn't seem to go anywhere."
		   f"\n{player.name} is in a similar place as before.")
	
	def death(self, width):
		border = Utilities.create_ruler(width, 'X')
		death_message = "You have failed your quest!"
		game_over = "G A M E   O V E R !"
		print(f"{border}\n{death_message.center(width)}\n{game_over.center(width)}\n{border}")
		input()
	
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

player = Player()
events = Game_Events()
newGame = Game(player, events)
newGame.start_game()