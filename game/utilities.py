import subprocess
import json
import os
from pathlib import Path
from .player import Player

class Utilities:
	def clear_screen():
		command = 'cls' if os.name == 'nt' else 'clear'
		subprocess.call(command, shell=True)

	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	def get_player_input(prompt, num_options):
		while True:
			player_input = input(prompt)
			if player_input.isdigit() and 0 < int(player_input) <= num_options:
				return int(player_input)
			else:
				print("Invalid input. Try again.")

	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~				

	def create_ruler(length = 50, character = '~'):
		return character * length
	
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	
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
		
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	def create_table_header(headers, table_width, stats):
		header_list = [header.strip() for header in headers.split(",")]
		num_columns = len(header_list)
		column_width = table_width // num_columns
		header_row = "".join(header.center(column_width) for header in header_list)
		stats_row = "".join(stat.center(column_width) for stat in stats)
		separator_length = max(len(header_row), len(stats_row))
		separator = Utilities.create_ruler(int(table_width * 0.75), '-').center(table_width)
		return f"{header_row}\n{separator}\n{stats_row}"
	
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	
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
	
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	def format_options(items):
		result = []
		for i, item in enumerate(items, start = 1):
			result.append(f"\t{i}: {item}")
		return "\n".join(result)
	
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	def print_title():
		print('''
	 _           _                _       _   _     _       
	| |         | |              (_)     | | | |   (_)      
	| |     __ _| |__  _   _ _ __ _ _ __ | |_| |__  _  __ _ 
	| |    / _` | '_ \\| | | | '__| | '_ \\| __| '_ \\| |/ _` |
	| |___| (_| | |_) | |_| | |  | | | | | |_| | | | | (_| |
   	\\_____/\\__,_|_.__/ \\__, |_|  |_|_| |_|\\__|_| |_|_|\\__,_|
		   	   __/  |                               
			  |____/  
''')
		
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	def format_opening_menus(options, num_options, prompt, prompt_type, width):
		border = Utilities.create_ruler(width, '~')
		Utilities.clear_screen()
		Utilities.print_title()
		print(border + "\n")
		print(options)
		print("\n" + border)
		if prompt_type == "num":
			return Utilities.get_player_input(prompt, num_options)
		else:
			return input(prompt)
		
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~		
		
	def show_save_load_prompt(width):
		options = Utilities.format_options(["New Game", "Load Saved Game"])
		return Utilities.format_opening_menus(options, len(options),
			"Make your selection: ", "num", width)
	
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	def save_game(player: Player):
		player_string = json.dumps(player.to_dict(), indent=4)
		current_dir = Path(__file__).parent
		saves_dir = current_dir / "saves"  # Pointing to the "saves" directory
		saves_dir.mkdir(parents=True, exist_ok=True)
		save_file = saves_dir / f"{player.name}.sav"
		with save_file.open(mode="w") as file:
			file.write(player_string)
		
		return (f"{player.name} pauses for a moment of meditation. {player.name} feels a strange "
				f"bond with the surrounding area. (Game saved as \"{player.name}.sav\")")
	
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	# Verifies .sav files exist in the saves directory and returns a list of them
	def get_save_files():
		current_dir = Path(__file__).parent
		saves_dir = current_dir / "saves"
		if not saves_dir.exists() or not any(saves_dir.glob("*.sav")):
			print("Error: No saved games were found in the 'saves' directory.")
			exit()
		file_paths = saves_dir.glob("*.sav")
		return [file.name for file in file_paths]

	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	def prompt_for_game_to_load(save_files, width):
		file_options = Utilities.format_options(save_files)
		player_input = int(Utilities.format_opening_menus(file_options, len(file_options),
			"Select a save to load: ", "str", width))
		return save_files[player_input - 1]

	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		
	def extract_json_data(game_to_load):
		try:
			saves_dir = Path(__file__).parent / "saves"  # Update to point to the 'saves' directory
			file_path = saves_dir / game_to_load
			file_path = file_path.resolve()

			with file_path.open("r") as file:
				data = json.load(file)
			return data
		except json.JSONDecodeError:
			print("Error: The file does not contain valid JSON.")
		except FileNotFoundError:
			print(f"Error: The file '{game_to_load}' was not found.")
		
		exit()

	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	def load_game(player: Player, width):
		save_files = Utilities.get_save_files()
		game_to_load = Utilities.prompt_for_game_to_load(save_files, width)
		save_data = Utilities.extract_json_data(game_to_load)
		if save_data:
			player.__dict__.update(save_data)

			# player.weapons should be a set to prevent duplicate items. However, JSON cannot handle
			# sets so this must be converted to a list prior to saving. On load, this converts the saved
			# list back to a set.
			if isinstance(player.weapons, list):
				player.weapons = set(player.weapons)
		else:
			print("Error: No data was loaded.")