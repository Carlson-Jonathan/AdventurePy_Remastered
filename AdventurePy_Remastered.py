from pathlib import Path
import subprocess
import random
import json
import os

class Player:
	def __init__(self):
		self.name = input("Enter your character's name: ")
		self.weapons = {"Fists"}
		self.equipped_weapon = "Fists"
		self.maximum_health = 100
		self.__health = 100
		self.is_dead = False
		self.trolls_blood = 0
		self.invisibility_potions = 0
		self.monsters_killed = 0

	def set_health(self, adjustment):
		self.__health += adjustment
		self.__health = min(self.__health, self.maximum_health)
		self.__health = max(self.__health, 0)

	def get_health(self):
		return self.__health
	
	def check_for_death(self):
		self.is_dead = bool(self.__health <= 0)
		return f"Having lost all health, {player.name} falls lifeless to the ground." if self.is_dead else ""
	
	# For serializing the object for json (saving games)
	def to_dict(self):
		return {
			"name": self.name,
			"weapons": list(self.weapons),
			"equipped_weapon": self.equipped_weapon,
			"health": self.__health,
			"maximum_health": self.maximum_health,
			"trolls_blood": self.trolls_blood,
			"is_dead": self.is_dead,
			"invisibility_potions": self.invisibility_potions,
			"monsters_killed": self.monsters_killed
		}


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
	
	# ------------------------------------------------------------------------------------

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
		
	# ------------------------------------------------------------------------------------

	def save_game(player: Player):
		player_string = json.dumps(player.to_dict(), indent = 4)
		current_dir = Path(__file__).parent
		save_file = current_dir / f"{player.name}.sav"
		with save_file.open(mode="w") as file:
			file.write(player_string)
		return (f"{player.name} pauses for a moment of meditation. {player.name} feels a strange "
			f"bond with the surrounding area. (Game saved as \"{player.name}.sav\")")


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
		selection_size = len(self.events[events.next_event][f"selection{player_input}"])
		random_num = random.randint(0, selection_size - 1) if player_input < 4 else 0
		outcome = event[f"selection{player_input}"][random_num](self.player)
		Utilities.draw_game_frame(header, event["event"], options, outcome, self.display_width)

		return player_input
	
	# ------------------------------------------------------------------------------------
	
	def start_game(self):
		events.print_introduction(player, self.display_width)
		while not self.player.is_dead:
			stats = [str(self.player.name), str(f"{self.player.get_health()}/{self.player.maximum_health}"),
				str(self.player.equipped_weapon)]
			header = Utilities.create_table_header("Name, Health, Weapon", self.display_width, stats)

			player_input = self.perform_event(header, self.events[events.next_event])
			input()

			if(self.player.is_dead):
				events.death(self.display_width)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~				
class Game_Events:
	def __init__(self):
		self.next_event = "hallway"

		self.game_data = {
			"hallway": {
				"event": f"{player.name} sees a long corridor. There is a sewer grate about 20 feet ahead.",
				"options": ["Go down the corridor", "Climb down the grate", "Yell for help", "Save Game"],
				"action": f"What will {player.name} do?",
				"selection1": [
					self.monster,
					self.hallway_trap_good,
					self.hallway_trap_bad,
					self.hallway_trap_none,
					self.trip_good,
					self.trip_bad,
					self.trip_none
				],
				"selection2": [
					self.monster,
					self.nothing,
					self.grate_good,
					self.grate_bad,
					self.grate_none,
					self.grate_treasure_room,
					self.grate_leprechaun
				],
				"selection3": [
					self.yell_monster,
					self.yell_gnome,
					self.yell_throat_hurts,
					self.yell_none,
					self.yell_collapse_good,
					self.yell_collapse_bad,
					self.yell_collapse_none
				],
				"selection4": [
					Utilities.save_game
				]
			},
			"gnome": {
				"event": "The gnome looks delicious!",
				"options": ["I had gnome for lunch.", "Nummy gnomey!", "Poke it with a stick first.", "Save Game"],
				"action": f"Should {player.name} eat it?",
				"selection1": [
					self.dirpy_gnomey_good,
					self.dirpy_gnomey_bad,
					self.dirpy_gnomey_none
				],
				"selection2": [
					self.nummy_gnomey_good,
					self.nummy_gnomey_bad,
					self.nummy_gnomey_none
				],
				"selection3": [
					self.pokey_gnomey_good,
					self.pokey_gnomey_bad,
					self.pokey_gnomey_none
				],
				"selection4": [
					Utilities.save_game
				]
			},
			"leprechaun": {
				f"event": "The little green-dressed leprechaun, who looks like he came straight "
					f"off a cereal box, dives right into pleasantries and introduces himself as "
					f"'Stinky'. \"It's dangerous to go alone! Take this.\" he says as he holds his "
					f"bag open in front of {player.name}. Where has {player.name} heard that line "
					f"before? It looks like there are several things in that bag but for some "
					f"reason, {player.name} knows only to take one item. Can this leprechaun be "
					f"trusted?",
				"options": ["Ask what is in the bag.", "Walk away.", "Reach in and grab something.", "Save Game"],
				"action": f"What should {player.name} do?",
				"selection1": [
					self.leprechaun_ask_good,
					self.leprechaun_ask_bad,
					self.leprechaun_ask_none
				],
				"selection2": [
					self.leprechaun_walk_good,
					self.leprechaun_walk_bad
				],
				"selection3": [
					self.leprechaun_bag_good,
					self.leprechaun_bag_bad,
					self.leprechaun_bag_none
				],
				"selection4": [
					Utilities.save_game
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
	def grate_good(self, player: Player):
		rand_num = random.randint(15, 35)
		player.set_health(rand_num)
		return (f"{player.name} removes the bars and finds a ladder leading down into darkness. "
			f"On the way down the ladder {player.name} finds a potion dangling by a string on one "
			f"of the ladder rungs. {player.name} pops the cork and gussles it regaining {rand_num} "
			f"health! Mmmmm! Cherry flavored!")

	def grate_bad(self, player: Player):
		rand_num = random.randint(25, 40)
		player.set_health(-rand_num)
		death_message = player.check_for_death()
		return (f"{player.name} removes the bars and finds a ladder leading down into darkness. "
			f"While climbing down a rung on the ladder breaks loose! {player.name} falls and "
			f"lands hard taking {rand_num} damage! Owiee! {death_message}")

	def grate_none(self, player: Player):
		return (f"{player.name} removes the bars and finds a ladder leading down into darkness. "
			f"{player.name} slides down the greasy ladder and springs into a fighting stance "
		 	f"at the bottom. No attack comes.") 

	def grate_leprechaun(self, player: Player):
		self.next_event = "leprechaun"
		return (f"{player.name} removes the bars and finds a ladder leading down into darkness. "
			f"After methodically stepping down the ladder, {player.name} splashes into a puddle "
			f"and turns to find a leprechaun sitting in a nook with a burlap sack.")

	def grate_treasure_room(self, player: Player):
		return (f"{player.name} removes the bars and finds a ladder leading down into darkness. "
			f"{player.name} drops down the hole and lands with a \"clink-clink-clatter\". What's "
			f"this on the floor? {player.name} discovers a room full of treasure!")

	# ----------------------------------- Yelling Events ---------------------------------
	def yell_monster(self, player: Player):
		return (f"{player.name} hollers into the darkness and hears an echoing voice followed "
		  	f"by a deep growl. {player.name}'s yells are responded to by a monster!")

	def yell_throat_hurts(self, player: Player):
		rand_num = random.randint(1, 10)
		player.set_health(-rand_num)
		death_message = player.check_for_death()
		return (f"{player.name} hollers as loud as possible for several minutes. {player.name}'s "
		  	f"throat now hurts from yelling and takes {rand_num} damage. (Way to go.) "
			f"{death_message}")
	
	def yell_gnome(self, player: Player):
		self.next_event = "gnome"
		return (f"{player.name} shouts for help. Moments later, a curious looking gnome appears "
		  	f"from around the corner.")

	def yell_none(self, player: Player):
		return (f"{player.name}'s voice echos down the tunnel, \"can anyone hear me?\". Just then "
		  	f"a reply is heard, \n\"Yes I hear you! Stop playing video games and get back to your "
			f"school work!\". Hmm, I wonder who that was?")
	
	def yell_collapse_good(self, player: Player):
		rand_num = random.randint(15, 35)
		player.set_health(rand_num)
		return (f"{player.name} screams and stomps. The tunnel walls begin to quiver. A potion "
		  	f"bottle randomly rolls out of a pipe in the wall! {player.name} slurps it up and "
			f"regains {rand_num} health!")

	def yell_collapse_bad(self, player: Player):
		rand_num = random.randint(10, 15)
		player.set_health(-rand_num)
		death_message = player.check_for_death()
		return (f"{player.name} screams and stomps. The tunnel walls begin to quiver. "
			f"Rocks begin to fall from above and and strike {player.name} on the head! "
			f"{player.name} takes {rand_num} damage! {death_message}")

	def yell_collapse_none(self, player: Player):
		return (f"{player.name} screams and stomps. The tunnel walls begin to quiver. "
		  	f"The roar of large falling rocks can be heard ahead. I hope that didn't block any "
			f"important passages. Oops!")

	# ----------------------------------- Gnome Events ---------------------------------
	def nummy_gnomey_good(self, player: Player):
		player.maximum_health += 30
		return (f"The todler-sized gnome beings to squeak out in its happy little voice, \"I "
			f"know a way out...\" when {player.name} suddenly pounces on it and begins feasting "
			f"on its chocolaty innards. What was that it was about to say? Oh who cares. As "
			f"{player.name} munches on the remainder of the gnomes head, {player.name} feels "
			f"an increase in vitality. {player.name}'s maximum health increases!")
	
	def nummy_gnomey_bad(self, player: Player):
		rand_num = random.randint(10, 15)
		player.set_health(-rand_num)
		death_message = player.check_for_death()
		return (f"Gnomercy! The cuddly little gnome squeaks in terror as {player.name} lunges "
		  	f"toward it drooling. Its retreat is in vain as {player.name} scoops the squirmy "
			f"doll creature up and gobbles it down. Moments later {player.name} begins to have "
			f"bad indegestion and takes {rand_num} damage. Gnomaalox! {death_message}")
	
	def nummy_gnomey_none(self, player: Player):
		return (f"{player.name} picks the startled gnome up by the head, and bites off one of "
			f"its legs. The last gnome {player.name} ate tasted much better. {player.name} drops "
			f"the gnome on the floor in disgust and lets it hop away.")	

	def pokey_gnomey_good(self, player: Player):
		rand_num = random.randint(15, 35)
		player.set_health(rand_num)
		return (f"{player.name} breaks a stick off of a sewer tree and suspiciously prods the "
		  	f" gnoblin. The gnome suddenly pops into a shower of confetti leaving only its pointed "
			f"hat behind. Picking it up {player.name} finds a potion inside and chugs it. "
			f"{player.name} regains {rand_num} health!")
	
	def pokey_gnomey_bad(self, player: Player):
		return (f"{player.name} pulls a walking stick from their pocket and jabs the gnome in the "
		  	f"eye. The gnome becomes enraged, growls, and viciously attacks {player.name}!")
	
	def pokey_gnomey_none(self, player: Player):
		return (f"{player.name} pulls out the breadstick left over from lunch and extends it "
		  	f"toward the gnome. In a flash, the gnome snatches it away and gobbles it up. "
			f"\"Thanks!\" it says as it dissapears into the darkness. {player.name} was going to "
			f"eat that. How rude!")
			  
	def dirpy_gnomey_good(self, player: Player):
		player.trolls_blood += 1
		return (f"\"What are you doing here cute little guy?\" {player.name} asks. The gnome "
		  	f"sniffles, and begins to tear up. \"Did you say 'cute'?\" After about five minutes "
			f"of sobbing, the gnome pull a vial of green liquid from its beard and offers it to "
			f"{player.name}. \"This is troll's blood.\" he begins to explain. \"You can use it "
			f"to...\" *gulp* {player.name} swallows the last drop while inattentively staring off "
			f"in another direction. \"Oh dear!\" exclaims the gnome. Was {player.name} supposed "
			f"to do that?")
	
	def dirpy_gnomey_bad(self, player: Player):
		return (f"{player.name} stares silently at the gnome. It sniffs and begins making an odd "
			f"growling sound. The gnome begins increasing in size and transforms into a monster!")  
		  	
	def dirpy_gnomey_none(self, player: Player):
		return (f"{player.name} decides there is no time to entertain a short-stack and punts it "
		  	f"down the nearest open grate. \"I can't reach the ground fast enough!\" it yells as "
			f"as it decends into the dark abyss. Time to focus on more important things.")

	# --------------------------------- Leprechaun Events --------------------------------

	def leprechaun_bag_good(self, player: Player):
		item_list = ["potion", "vial to troll's blood", "quarter staff"]
		rand_item_num = random.randint(0, 2)
		rand_health_num = random.randint(15, 25)
		
		player.set_health(rand_health_num if rand_item_num == 0 else 0)
		if(rand_item_num == 2):
			player.trolls_blood += 1
		if(rand_item_num == 2):
			player.weapons.add("Staff")

		item_description = [
			f"Just what {player.name} needed! {player.name} pops the lid and gulps it down "
				f"regaining {rand_health_num} health! {player.name} then bids farewell to "
				f"Stinky. Maybe {player.name} will encounter him again?",
			f"Well that sure looks tasty! {player.name} tips the contents of the vile and "
				f"gulps it down. \"No! You are supposed to... oh nevermind.\" Stinky says as "
				f"{player.name} licks the remaining fluid from the opening of the vile. Feeling "
				f"a bit loopy, {player.name} wanders away toward visions of sugar plumbs.",
			f"How did Stinky fit a 6' pole in that little sack? What does it matter? {player.name} "
				f"should be able to use this to fight back the monsters. "
				f"\n\tNew weapon: Staff - Occasionally lands multiple blows to monsters."
		]

		return (f"{player.name} reaches blindly into the bag and grabs ahold of something. "
			f"{player.name} pulls out a {item_list[rand_item_num]}! {item_description[rand_item_num]}")
				  
	def leprechaun_bag_bad(self, player: Player):
		damage_type = random.randint(0, 4)
		damage_amount = random.randint(5, 10)
		player.set_health(-damage_amount)
		death_message = player.check_for_death()
		damage_event = ["bit by a venomous spider ", "stung by a scorpion ", "bit by a snake ",
			"stung by a large wasp ", "pricked by a rusty nail "]
		return (f"{player.name} reaches blindly into the bag and grabs ahold of something. "
			f"Oww! {player.name} was {damage_event[damage_type]} inside the bag and takes "
			f"{damage_amount} health damage! \"Sorry fer that,\" Stinky says unapologetically, "
			f"\"but ye are only allowed to reach into this here bag once per visit.\" Stinky "
			f"ties his bag shut and scurries off. How unfortunate. Maybe you will see him again? "
			f"{death_message}")

	def leprechaun_bag_none(self, player: Player):
		rand_num = random.randint(0,5)
		rand_item = ["a pink stuffed bunny", "a solar-powered flashlight", "a stack of coupons ",
			"a broken umbrella", "a soggy newspaper", "an AOL CD"]
		return (f"{player.name} reaches blindly into the bag and grabs ahold of something. "
		  	f"{player.name} pulls {rand_item[rand_num]} out of the bag. Great. This will be "
			f"so useful as {player.name} struggles for life in a hostile underworld. \"Thank you "
			f"fer yer business. See ya next time!\" says Stinky as he dissapears in a cloud of "
			f"smoke. 'Next time?'")
	
	def leprechaun_walk_good(self, player: Player):
		return (f"{player.name} looks the little green half-pint up and down. Wheel and deal with this "
			f"sketchy character? Ain't nobody got time for that! As {player.name} starts to walk "
			f"away, Stinky shouts, \"Wait! Perhaps ye be interested in finding a way out of this "
			f"here dark maze. I have a map, see, that will show ya how to escape, but I'll only "
			f"give it to ya if you rid this dungeon of at least 5 monsters. Also, you will be "
			f"need'n a compass to use it, but I don't have one. What do ya say?\" It sounds "
			f"like {player.name} doesn't have much of a choice and agrees to do the leprechaun's "
			f"dirty work of monster slaying. {player.name} reluctantly agrees and wanders off.")

	def leprechaun_walk_bad(self, player: Player):
		rand_num = random.randint(30, 50)
		player.set_health(-rand_num)
		death_message = player.check_for_death()
		return (f"{player.name} looks the little green half-pint up and down. Wheel and deal with this "
			f"sketchy character? Ain't nobody got time for that! As {player.name} turns around to walk "
			f"away, Stinky pulls a knife from his bag and stabs {player.name} in the back! Oh no! It "
			f"was the leprechaun from THAT movie! {player.name} takes {rand_num} damage! {death_message}")
	
	def leprechaun_ask_good(self, player: Player):
		player.set_health(player.maximum_health)
		return (f"{player.name} suspiciously asks the leprechaun what is in the bag. \"Perhaps it "
		  	f"be best if I show ya! Try a sample of this here potions. Satisfaction guarenteed!\" "
			f"{player.name} takes the bottle of purple liquid from Stinky and gulps it down. "
			f"{player.name}'s health fully recovers! Wow! What else does Stinky... where'd he go?")
		  
	def leprechaun_ask_bad(self, player: Player):
		rand_num = random.randint(1, 30)
		player.set_health(-rand_num)
		death_message = player.check_for_death()
		return (f"{player.name} suspiciously asks the leprechaun what is in the bag. \"Perhaps it "
		  	f"be best if I show ya! Try a sample of this here potions. Satisfaction guarenteed!\" "
			f"{player.name} takes the bottle of inky liquid from Stinky and gulps it down. "
			f"{player.name} becomes momentarily blind and walks into the wall taking {rand_num} "
			f"damage! When {player.name}'s vision returns, Stinky is gone. That little troll! "
			f"{death_message}")
	
	def leprechaun_ask_none(self, player: Player):
		return (f"{player.name} suspiciously asks the leprechaun what is in the bag. Stinky "
			f"says excitedly, \"I'm glad ye asked! From the far reaches of Centrailia I have "
			f"baubles, doodads, and gizmos. I have acquired 80 nickknacks from Grumblethorp! Ye "
			f"want thingamajigs? I've got 20! But who cares? No big deal. I've got more!\" Stinky "
			f"continues on and on listing non-sensical items he has proudly acquired from places "
			f"that sound entirely made up. {player.name}'s eyes begin to glaze over. "
			f"After 10 minutes of this {player.name} decides to wander off.")
	
	# ------------------------------- Miscellaneous Events -------------------------------
	def monster(self, player: Player):
		return f"Before {player.name} can act, a monster jumps out of the darkness!"

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

	def print_introduction(self, player: Player, width):
		print(Utilities.create_ruler(width, '~'))
		header = "O U R   S T O R Y   B E G I N S".center(width)
		opening_text = f'''My name is {player.name}. I fell down a hole while doing something stupid
			but can't remember what. When I woke up, I was in a strange smelly labyrinth full of
			tricks, treasures, traps, and other things that begin with 't'. It is spooky down here
			and I need you to help me get out! Guide me through the events using the prompts and
			help me stay alive and escape! Good luck!'''
		print(f"{header}\n{Utilities.wrap_text(opening_text, width)}\n")
		print(f"Are you ready to begin your adventure?".center(width))
		print("[Enter] Labyrinthia".center(width))
		print(Utilities.create_ruler(width, '~'))
		input()
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == "__main__":
	player = Player()
	events = Game_Events()
	newGame = Game(player, events)
	newGame.start_game()