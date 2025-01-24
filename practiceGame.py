import subprocess
import random
import os

class Player:
	def __init__(self):
		self.name = "Joe"
		self.health = 100
		self.weapon = "Broad Sword"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		
class Utilities:
	def clear_screen():
		# Windows
		if os.name == 'nt':
			subprocess.call('cls', shell=True)
		# Linux
		else:
			subprocess.call('clear', shell=True)

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
		words = text.split()  # Split the text into words
		lines = []
		current_line = ""

		for word in words:
			# Check if adding the word would exceed the width
			if len(current_line) + len(word) + 1 > width:
				lines.append(current_line.strip())  # Add the current line to the list
				current_line = word  # Start a new line with the current word
			else:
				current_line += " " + word  # Add the word to the current line

		# Add the last line if there's anything left
		if current_line:
			lines.append(current_line.strip())

		return "\n".join(lines)
	
	# ------------------------------------------------------------------------------------

	def format_options(items):
		result = []
		for i, item in enumerate(items, start=1):  # Start indexing at 1
			result.append(f"\t{i}: {item}")
		return "\n".join(result)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Game:
	def __init__(self, player: Player, events: 'Game_Events' = None):
		self.player = player
		self.events = events.game_data
		self.gameover = False
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
		while not self.gameover:
			stats = [str(self.player.name), str(self.player.health), str(self.player.weapon)]
			header = Utilities.create_table_header("Name, Health, Weapon", self.display_width, stats)

			player_input = self.perform_event(header, self.events["hallway"])
			input()

			if player_input == 0:
				self.gameover = True

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~				
lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
options = ["Sing a song", "Do a dance", "Pick your nose"]

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

	def monster(self, player: Player):
		return f"A monster jumps out of the darkness!"
	
	def hallway_trap_good(self, player: Player):
		player.health += 40
		return f"{player.name} gets 40 health!"
	
	def hallway_trap_bad(self, player: Player):
		player.health -= 40
		return f"{player.name} loses 40 health!"
	
	def hallway_trap_none(self, player: Player):
		return f"{player.name} contemplates their health."
	
	def trip_good(self, player: Player):
		rand_num = random.randint(10, 30)
		player.health += rand_num
		return (f"{player.name} trips over a rock!"
			f"\nAfter getting up and dusting off, {player.name} sees that the rock was actually a health potion!"
			f"\n{player.name} quickly grabs and gulps it down regaining {rand_num} health.")
	
	def trip_bad(self, player: Player):
		rand_num = random.randint(1, 20)
		player.health -= rand_num
		return (f"{player.name} trips over a rock!"
			f"\n{player.name} face plants into the hard floor and takes {rand_num} damage! Ouch!")
	
	def trip_none(self, player: Player):
		return (f"{player.name} trips over a rock!"
			f"\nFortunately {player.name} landed in some nice soft mud. Every thing is fine.")
	
	def weapon_treasure(self, player: Player):
		return f"{player.name} finds a weapon!"
	
	def nothing(self, player: Player):
		return (f"Well that didn't seem to go anywhere."
		   f"\n{player.name} is in a similar place as before.")
	
	# -------------------------------- Sewer Grate Events --------------------------------

	# ----------------------------------- Yelling Events ---------------------------------

	# ------------------------------- Miscellaneous Events -------------------------------


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

player = Player()
events = Game_Events()
newGame = Game(player, events)
newGame.start_game()