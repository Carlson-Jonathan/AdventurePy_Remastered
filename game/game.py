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
		self.mains = {"hallway": 0, "tunnel_fork": 0, "river": 0}
		self.debug_mode = False
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
			self.events_data["combat_weapon"]["options"] = list(self.player.weapons)
		
	# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	def perform_event(self, header, full_event):
		event_name = self.game_events.next_event
		num_options = len(full_event["options"])

		options = Utilities.format_options(full_event["options"])
		Utilities.draw_game_frame(header, full_event["event"](self.player), options,
			full_event["action"](self.player), self.display_width)

		# Choose a random event based on the player selection
		player_input = Utilities.get_player_input("Action: ", num_options)
		event_possibilites = (self.events_data[event_name][f"selection{player_input}"])
		num_possibilites = len(event_possibilites)
		chosen_event = self.game_events.get_event_using_frequency(event_possibilites,
			self.game_events.event_frequencies)
		
		Utilities.draw_game_frame(header, full_event["event"](self.player), options,
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

			if self.game_events.next_event in self.mains:
				self.mains[self.game_events.next_event] += 1
			if self.debug_mode:
				print(self.mains)
			input()

			# Process 'game over' if player dies
			if(self.player.is_dead):
				self.game_events.death(self.display_width)


'''
Ideas:
Go to an area where there is an underground river, a mirror on the wall, and a door
	River:
		Something is floating down the river
		A monster jumps out of the water
		Take a drink and take damage
	Mirror
		Options:
			Change Name
			View Stats
			Get hint
			Modify width
	Door
		Options
			Kick it in
				Monster
				Treasure Room
				Empty
				Bathroom
			Knock
				Stinky
					Did you eat the gnome?
						Bring the gnome hat and learn to read the spell book
				Gnome
					Are you conspiring with the leprechaun?
						Bring the staff and learn multi-strikes
				No answer
				Opens 

'''				