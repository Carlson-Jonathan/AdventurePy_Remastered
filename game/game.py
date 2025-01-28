import random
from .player import Player
from .utilities import Utilities
from .gameEvents import Game_Events

class Game:
	def __init__(self):
		self.player = Player()
		self.game_events = Game_Events()
		self.events_data = self.game_events.game_data
		self.display_width = 75
		self.start_game()

	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	# The introduction and setup sequence when the game begins		
	def run_start_sequence(self):
		player_input = Utilities.show_save_load_prompt(self.display_width)
		
		if player_input == 1:
			self.player.name = input("Enter your character's name: ")
			Utilities.clear_screen()
			Utilities.print_title(self.display_width)
			self.game_events.print_introduction(self.player, self.display_width)
		else:
			Utilities.load_game(self.player, self.display_width)
		
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	def perform_event(self, header, event):
		num_options = len(event["options"])
		options = Utilities.format_options(event["options"])

		Utilities.draw_game_frame(header, event["event"](self.player), options,
			event["action"](self.player), self.display_width)
		
		# Choose a random event based on the player selection
		player_input = Utilities.get_player_input("Action: ", num_options)
		selection_size = len(self.events_data[self.game_events.next_event][f"selection{player_input}"])
		chosen_event = self.game_events.get_event_using_frequency(
			self.events_data[self.game_events.next_event][f"selection{player_input}"])
		
		Utilities.draw_game_frame(header, event["event"](self.player), options,
			chosen_event(self.player), self.display_width)

		return player_input
	
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	
	def start_game(self):
		self.run_start_sequence()
		while not self.player.is_dead:
			# Display the header stats
			stats = [str(self.player.name), str(f"{self.player.health}/{self.player.maximum_health}"),
				str(self.player.equipped_weapon)]
			header = Utilities.create_table_header("Name, Health, Weapon", self.display_width, stats)

			# Run an event and pause so the player can read it
			player_input = self.perform_event(header, self.events_data[self.game_events.next_event])
			input()

			# Process 'game over' if player dies
			if(self.player.is_dead):
				self.game_events.death(self.display_width)