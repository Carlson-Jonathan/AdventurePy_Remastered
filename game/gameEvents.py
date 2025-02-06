from .utilities import Utilities
from .player import Player
from . import monster
import random

class Game_Events:
	def __init__(self):
		self.next_event = "hallway"
		self.event_frequencies = {}
		self.main_event_frequencies = {"hallway": 1, "tunnel_fork": 1, "river": 1}
		self.all_event_functions = set()
		self.monster = monster.generate_monster()
		self.player_weapons = "Fists"

		self.game_data = {
			"hallway": {
				"event": self.hallway_event,
				"options": ["Go down the corridor", "Climb down the grate", "Yell for help", "Save Game"],
				"action": self.generic_action_prompt,
				"selection1": [
					self.nothing,
					self.monster_encounter,
					self.hallway_trap_good,
					self.hallway_trap_bad,
					self.hallway_trap_none,
					self.trip_good,
					self.trip_bad,
					self.trip_none,
					self.find_treasure_chest
				],
				"selection2": [
					self.monster_encounter,
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
					self.yell_collapse_none,
				],
				"selection4": [Utilities.save_game]
			},
			"gnome": {
				"event": self.gnome_event,
				"options": ["I had gnome for lunch", "Nummy gnomey!", "Poke it with a stick first", "Save Game"],
				"action": self.gnome_action,
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
				"selection4": [Utilities.save_game]
			},
			"leprechaun": {
				"event": self.leprechaun_event,
				"options": ["Ask what is in the bag", "Walk away", "Reach in and grab something", "Save Game"],
				"action": self.generic_action_prompt,
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
				"selection4": [Utilities.save_game]
			},
			"treasure_room": {
				"event": self.treasure_room_event,
				"options": ["Attempt to open the treasure chest", "Investigate the weapons rack",
					"Leave through the door", "Save Game"],
				"action": self.generic_action_prompt,
				"selection1": [
					self.treasure_room_box_good,
					self.treasure_room_box_bad,
					self.treasure_room_box_none
				],
				"selection2": [
					self.treasure_room_rack_good,
					self.treasure_room_rack_none
				],
				"selection3": [
					self.treasure_room_leave_good,
					self.treasure_room_leave_bad,
					self.treasure_room_leave_none
				],
				"selection4": [Utilities.save_game]
			},
			"tunnel_fork": {
				"event": self.tunnel_fork_event,
				"options": ["Go left", "Go right", "Sing a song", "Save Game"],
				"action": self.generic_action_prompt,
				"selection1": [
					self.tunnel_fork_left_good,
					self.tunnel_fork_left_bad,
					self.tunnel_fork_left_none,
					self.monster_encounter,
					self.nothing,
					self.find_treasure_chest
				],
				"selection2": [
					self.tunnel_fork_right_good,
					self.tunnel_fork_right_bad,
					self.tunnel_fork_right_none,
					self.monster_encounter,
					self.find_treasure_chest
				],
				"selection3": [
					self.tunnel_fork_sing_good,
					self.tunnel_fork_sing_bad,
					self.tunnel_fork_sing_none,
					self.monster_encounter,
					self.nothing					
				],
				"selection4": [Utilities.save_game]
			},
			"river": {
				"event": self.river_event,
				"options": ["Approach river", "Open door", "Look at mirror", "Save Game"],
				"action": self.generic_action_prompt,
				"selection1": [
					self.river_event_monster,
					self.river_event_flotsam,
					self.river_event_drink
				],
				"selection2": [self.river_open_door],
				"selection3": [self.river_approach_mirror],
				"selection4": [Utilities.save_game]
			},
			"door_event": {
				"event": self.door_event,
				"options": ["Knock on door", "Kick in door", "Pick lock", "Save Game"],
				"action": self.generic_action_prompt,
				"selection1": [
					self.door_knock_stinky,
					self.door_knock_gnome,
					self.door_knock_no_answer,
					self.door_knock_door_opens
				],
				"selection2": [
					self.door_kick_monster,
					self.door_kick_treasure_room,
					self.door_kick_empty,
					self.door_kick_bathroom
				],
				"selection3": [
					self.door_lock_pick_good,
					self.door_lock_pick_bad,
					self.door_lock_pick_none
				],
				"selection4": [Utilities.save_game]
			},
			"mirror": {
				"event": self.mirror_event,
				"options": ["Change name", "View stats", "Modify width", "Save Game"],
				"action": self.generic_action_prompt,
				"selection1": [self.mirror_change_name],
				"selection2": [self.mirror_view_stats],
				"selection3": [self.mirror_change_width],
				"selection4": [Utilities.save_game]
			},
			"combat": {
				"event": self.combat_event,
				"options": ["Attack", "Flee", "Change Weapon", "Lay Down and Die"],
				"action": self.generic_action_prompt,
				"selection1": [self.combat_attack],
				"selection2": [self.combat_flee],
				"selection3": [self.combat_change_weapon],
				"selection4": [Utilities.save_game]
			},
			"combat_weapon": {
				"event": self.combat_event,
				"options": [self.player_weapons],
				"action": self.equip_weapon_action,
				"selection1": [self.equip_weapon1],
				"selection2": [self.equip_weapon2],
				"selection3": [self.equip_weapon3],
				"selection4": [self.equip_weapon4]
			}
		}

		self.populate_event_functions(self.game_data)
		self.initialize_event_frequencies()

	##################################### Combat Events ############################################

	def combat_event(self, player: Player):
		return (f"The monster steps forward—a hulking {self.monster.name}, its many eyes glinting in the dim light. "
			f"Its spindly legs shift with unnatural grace, clicking against the stone with each movement. "
			f"A low hiss escapes its fanged maw, the air thick with the scent of damp earth and decay. "
			f"This thing isn’t just lurking—it’s ready to strike.")
	
	# ----------------------------------------------------------------------------------------------

	def equip_weapon_action(self, player: Player):
		if len(player.weapons) == 1:
			return (f"Hmm, it looks like {player.name} doesn't have many options. What would you like "
			f"etched on {player.name}'s tombstone?")
		else:
			return (f"Great! {player.name} has something to fight the {self.monster.name} with!"
				f"What should {player.name} use?")

	# ----------------------------------------------------------------------------------------------
		
	def get_weapon_equip_text(self, player: Player, weapon):
		weapon_text = {
			"Fists": "for a round of fisticuffs!",
			"Sword": "to carve up some meat!",
			"Staff": "to smash some heads!",
			"Magic Book": "to... read a story?"}
		self.next_event = "combat"
		print(f"The selected weapon is {weapon}")
		return weapon_text[weapon]
	
	# ----------------------------------------------------------------------------------------------

	def equip_weapon1(self, player: Player):
		player.equipped_weapon = self.game_data["combat_weapon"]["options"][0]
		return f"{player.name} is ready {self.get_weapon_equip_text(player, player.equipped_weapon)}"

	# ----------------------------------------------------------------------------------------------

	def equip_weapon2(self, player: Player):
		player.equipped_weapon = self.game_data["combat_weapon"]["options"][1]
		return f"{player.name} is ready {self.get_weapon_equip_text(player, player.equipped_weapon)}"

	# ----------------------------------------------------------------------------------------------

	def equip_weapon3(self, player: Player):
		player.equipped_weapon = self.game_data["combat_weapon"]["options"][2]
		return f"{player.name} is ready {self.get_weapon_equip_text(player, player.equipped_weapon)}"

	# ----------------------------------------------------------------------------------------------

	def equip_weapon4(self, player: Player):
		player.equipped_weapon = self.game_data["combat_weapon"]["options"][3]
		return f"{player.name} is ready {self.get_weapon_equip_text(player, player.equipped_weapon)}"

	# ----------------------------------------------------------------------------------------------

	def combat_attack(self, player: Player):
		damage = random.randint(1, 10)
		evaded = random.randint(1, 10)
		monster_evaded = f"The {self.monster.name} evades {player.name}'s attack!"
		landed_damage = f"{player.name} strikes the {self.monster.name} and does {damage} damage!"
		if evaded < 7:
			# reduce monster health
			# check for death
			    # Set next event
			retaliation = self.monster_retaliation(player)
			return (f"{landed_damage} {retaliation}")
		else:
			return monster_evaded
		
	# ----------------------------------------------------------------------------------------------

	def combat_flee(self, player: Player):
		escape = random.randint(1, 10)
		failed = f"{player.name} attempts to flee but is unable to escape!"
		fled = f"{player.name} turns and runs screaming like a coward! (chicken!)"
		if escape < 7:
			retaliation = self.monster_retaliation(player)
			return f"{failed} {retaliation}"
		else:
			self.shuffle_events()
			return fled
		
	# ----------------------------------------------------------------------------------------------

	def combat_change_weapon(self, player: Player):
		self.game_data["combat_weapon"]["options"] = list(player.weapons)
		self.next_event = "combat_weapon"
		return f"{player.name} scrambles to find a better weapon..."
		
	# ----------------------------------------------------------------------------------------------

	def monster_retaliation(self, player: Player):
		damage = random.randint(10, 20)
		evaded = random.randint(1, 12)
		player_evaded = (f"The {self.monster.name} strikes at {player.name}, but {player.name} jumps "
			f"back barely evading the {self.monster.name}'s strike!")
		landed_damage = f"The {self.monster.name} strikes {player.name} causing {damage} points of damage!"
		do_nothing = f"The {self.monster.name} hisses and snarls as it prepares for its next attack."
		if evaded < 7:
			if evaded < 3:
				return do_nothing
			player.modify_health(-damage)
			death_message = player.check_for_death()
			return (f"{landed_damage} {death_message}")
		else:
			return player_evaded
		   

	##################################### Mirror Events ############################################

	def mirror_event(self, player: Player):
		return (f"There is an image that seems to *shift* every time {player.name} tries to focus "
		  	f"on it. It has the eerie feeling of being watched by an unknown presence, but every "
			f"time {player.name} tries to describe it, the details slip through their fingers like "
			f"sand. What was that? Was it a shadow, or just the light? {player.name} can’t say "
			f"for sure, but they feel a strange sense of unease. Suddenly, a voice whispers in "
			f"their head, offering… something. What is it? They can’t quite tell, but it seems "
			f"important. It seems to be speaking- past {player.name}?")

	# ----------------------------------------------------------------------------------------------
	
	def mirror_change_name(self, player: Player):
		self.shuffle_events()
		return (f"{player.name} feels an odd compulsion, as if something is guiding their hands. "
			f"Before they can stop themselves, a dizzying sensation takes over, and the world "
			f"around them warps. {player.name} blinks, suddenly unsure of who they are. Were they "
			f"always this way? Memories oddly begin to slip away, replaced by something fuzzy and "
			f"unfamiliar. The strange sensation lingers, and {player.name} can’t shake the feeling "
			f"that their past has been rewritten, though they can’t recall how or why. Whatever just "
			f"happened, it feels deeply unsettling.")
	
	# ----------------------------------------------------------------------------------------------

	def mirror_view_stats(self, player: Player):
		self.shuffle_events()
		return (f"{player.name} stares at the sudden display of stats and items, unsure how "
			f"they got there. They don’t remember asking for this—what is all this stuff? "
			f"Why are there numbers next to things they don’t even recognize? {player.name} feels "
			f"like they’re being examined by some unseen force, poking around in their most private "
			f"details. They shake their head, trying to shake the weird sensation off. It’s as if "
			f"someone’s looking through their personal diary and critiquing their choices. Oddly, "
			f"{player.name} can't help but wonder if this is how a hamster feels when it’s in a cage.")

	# ----------------------------------------------------------------------------------------------

	def mirror_change_width(self, player: Player):
		self.shuffle_events()
		return (f"{player.name} notices the world suddenly *stretching* and *squishing* as if "
			f"someone's pulling and squeezing it like an old rubber band. Their surroundings "
			f"warp, the walls elongate, and the ground seems to shrink under their feet. It’s like "
			f"the universe itself got a little too excited about adjusting its settings. Just as "
			f"quickly, everything snaps back into place, leaving {player.name} dizzy and wondering "
			f"if they just imagined the whole thing. One thing's for sure: {player.name}'s vision "
			f"has never felt more... wide? Narrow? Neither. Probably neither.")
		

	###################################### Door Events #############################################
		
	def door_event(self, player: Player):
		self.shuffle_events()
		return (f"A rusty keyhole stares back mockingly, as if daring {player.name} to try "
		  	"something clever. Whether this door hides treasure or trouble is unclear, but one "
			"thing is certain—it won't open on its own.") 

	# ----------------------------------------------------------------------------------------------

	def door_kick_monster(self, player: Player):
		self.next_event = "combat"
		return (f"{player.name} rears back and delivers a ferocious kick to the door. With a loud "
			f"*BANG*, it flies open, slamming against the cavern wall. Dust swirls in the dim "
			f"light as {player.name} stands triumphantly, ready to claim victory over—oh. Oh no. "
			f"That is *not* treasure. That is a very large, very angry creature blinking awake "
			f"from its slumber. It stretches, yawns, and fixes its hungry gaze on {player.name}. "
			f"Okay, so maybe kicking wasn't the best idea. In my defense, I thought the door was "
			f"sturdier. Who keeps approving these flimsy doors?!")  
	
	# ----------------------------------------------------------------------------------------------

	def door_kick_treasure_room(self, player: Player):
		self.next_event = "treasure_room"
		return (f"{player.name} takes a deep breath, winds up, and delivers a thunderous kick to "
			f"the center of the door. With a deafening *CRACK*, the old wood gives way, swinging "
			f"open so violently it nearly jumps off its hinges. {player.name} stumbles forward, "
			f"bracing for whatever doom surely awaits… but instead, the flickering torchlight "
			f"reveals heaps of gold, glittering jewels, and priceless artifacts piled high. "
			f"Huh. That actually worked? I mean… of *course* it worked! That was totally meant "
			f"to happen. Yup. Definitely. Excuse me while I go revise *all* my notes.")  

	# ----------------------------------------------------------------------------------------------

	def door_kick_empty(self, player: Player):
		self.shuffle_events()
		return (f"{player.name} takes a step back, squares up, and delivers a mighty kick to the "
			f"center of the door. There’s a loud *thud*... followed by absolutely nothing. "
			f"The door doesn’t budge. Not even a little. Instead, a dull ache creeps up "
			f"{player.name}'s leg as the door stands victorious. Somewhere, in the vast cosmic "
			f"balance of things, the door just earned bragging rights. {player.name} can almost "
			f"hear it whisper, ‘Nice try.’ Feeling dejected, {player.name} wanders away head hanging.")  
	
	# ----------------------------------------------------------------------------------------------

	def door_kick_bathroom(self, player: Player):
		self.shuffle_events()
		rand_num = random.randint(40, 65)
		player.modify_health(rand_num)
		return (f"{player.name} winds up and launches a mighty kick at the door, sending it "
			f"crashing open. Heart pounding, adrenaline surging, {player.name} braces for "
			f"whatever horrors lurk beyond—only to be met with the sight of a humble, well-kept "
			f"restroom. A single torch flickers over a pristine chamber pot, practically inviting. "
			f"After downing all those health potions, nature *has* been calling. Relieved in more "
			f"ways than one, {player.name} feels refreshed and recovers {rand_num} health. "
			f"Honestly, this might be the greatest treasure of all!")  
	
	# ----------------------------------------------------------------------------------------------

	def door_knock_stinky(self, player: Player):
		return (f"{player.name} knocks lightly on the door, and to their surprise, it creaks open. "
			f"Standing there, arms crossed and looking rather unimpressed, is none other than "
			f"Stinky the leprechaun. His tiny, green hat is askew, and his nose twitches as if "
			f"he’s already smelling the trouble in the air. \"Well, well, well, if it isn’t the "
			f"champion of poor decisions,\" he says, his voice dripping with sarcasm. \"What is it, "
			f"then? Come to ask me for more luck, or are you just here to waste my time?\"")

	# ----------------------------------------------------------------------------------------------

	def door_knock_gnome(self, player: Player):
		self.shuffle_events()
		return (f"{player.name} knocks on the door, and it slowly creaks open. On the other side, "
			f"standing with his back against the wall and eyes wide as saucers, is a tiny gnome. "
			f"He stares up at {player.name}, trembling like a leaf in the wind, his hands raised "
			f"defensively. \"P-Please don’t hurt me! I-I’m not the one who—\" he stammers, eyes darting "
			f"around, clearly trying to find an escape route. \"I-I just wanted to... uh... find a nice "
			f"corner to hide in! Please, I promise I’m not important!\"")

	# ----------------------------------------------------------------------------------------------

	def door_knock_no_answer(self, player: Player):
		self.shuffle_events()
		return (f"{player.name} knocks firmly on the door, the sound echoing eerily in the silence. "
			f"Then… nothing. No creak, no footsteps, no mysterious voice from behind the door. Just "
			f"the quiet rustling of the cavern and the faint drip of water from somewhere above. "
			f"{player.name} knocks again, a little louder this time, but still, not a peep. It’s almost "
			f"like the door itself is pretending not to hear. Maybe it’s on a lunch break? In any case, "
			f"{player.name} is left standing there, feeling slightly awkward. This is getting real weird.")

	# ----------------------------------------------------------------------------------------------

	def door_knock_door_opens(self, player: Player):
		self.shuffle_events()
		return (f"{player.name} raps gently on the ancient wooden door, the sound echoing faintly "
			f"through the cavern. For a moment, nothing happens. Then, with a slow, ominous creak, "
			f"the door swings open on its own. Huh. That wasn’t supposed to happen. I distinctly "
			f"remember writing that this door was locked. Hang on—let me check my notes… Yep, "
			f"right here: ‘The door is locked and will not open on its own.’ So either I got the "
			f"wrong script, or {player.name} just has incredibly persuasive knuckles.")  
	
	# ----------------------------------------------------------------------------------------------

	def door_lock_pick_good(self, player: Player):
		self.shuffle_events()
		player.trolls_blood += 1
		return (f"{player.name} carefully works the lock, the pick sliding smoothly into place. With a "
			f"satisfying *click*, the door creaks open. Inside, {player.name} spots a small vial of trolls blood "
			f"on a pedestal. Without hesitation, {player.name} grabs it, uncorks the bottle, and drinks it in one "
			f"gulp. The liquid tastes oddly metallic, but it’s not unpleasant. As the last drop slips down, "
			f"{player.name} wonders out loud, \"Why do I always drink strange potions I find?\" Before they can "
			f"ponder it further, a surge of strength rushes through their veins but no health is restored. "
			f"Must have a delayed effect.")

	# ----------------------------------------------------------------------------------------------

	def door_lock_pick_bad(self, player: Player):
		self.shuffle_events()
		rand_num = random.randint(1, 10)
		player.modify_health(-rand_num)
		if player.invisibility_potions > 0:
			item = "an invisibility potion"
			player.invisibility_potions -= 1
			comment = "Guess it wasn't *that* invisible..."
		else:
			items = ["a sack of marbles", "a tuna sadwich", "a wooden nickle", "a jumping bean",
				"an unread love letter", "a picture of a narwhal"]
			item = random.choice(["a sack of marbles", "a rotten tuna sandwich", "a wooden nickel", 
							"a jumping bean", "an unread love letter", "a picture of a gnarwall"])
			comment = "{player.name was probably better off without that...}"
		death_message = player.check_for_death()
		return (f"{player.name} carefully kneels down and starts fiddling with the lock, the sound of "
			f"the lockpick scraping against the metal filling the air. For a moment, it seems like "
			f"progress is being made—then, with a sharp *snap*, the pick breaks in half! As {player.name} "
			f"fumbles to recover, a hidden mechanism inside the door activates, releasing a cloud of toxic "
			f"fumes. {player.name} stumbles backward, coughing, and feels a sharp pain in their chest. "
			f"That was not the type of treasure {player.name} had in mind. {rand_num} damage is dealt "
			f"and {player.name} loses {item} they were carrying. {comment} {death_message}")
	
	# ----------------------------------------------------------------------------------------------

	def door_lock_pick_none(self, player: Player):
		self.shuffle_events()
		return (f"{player.name} carefully works the lock, concentrating hard, but after what feels like "
			f"an eternity, nothing happens. The lockpick barely moves. {player.name} lets out a frustrated "
			f"sigh and stands up. It's as if the lock is taunting them, saying, 'Nice try, but not today.' "
			f"Maybe next time, {player.name}. Or perhaps just stick to the good ol' fashioned door-kicking method...")


	###################################### River Events ############################################

	def river_event(self, player: Player):
		return (f"{player.name} steps cautiously into a vast cavern, the flickering torchlight barely "
			f"illuminating the eerie surroundings. A slow-moving river glistens in the dim light, "
			f"its dark waters whispering secrets as it winds through the underground expanse. To "
			f"the side, an ancient wooden door stands defiantly, its surface scarred with deep "
			f"gashes—either from age or something with very sharp claws. And against the cavern "
			f"wall, a tall, ornate mirror sits inexplicably, its silver frame untarnished despite "
			f"the damp air. The glass shimmers oddly, reflecting more than just the torchlight… "
			f"or maybe it's just {player.name}'s imagination. Either way, something here demands "
			f"attention.")
	
	# ----------------------------------------------------------------------------------------------
	
	def river_open_door(self, player: Player):
		self.next_event = "door_event"
		return (f"{player.name} steps up to the massive wooden door, its surface worn and riddled "
			f"with deep scratches. A thick iron handle juts out, cold to the touch, but as "
			f"{player.name} gives it a pull, the door refuses to budge. Locked. Of course.")

	# ----------------------------------------------------------------------------------------------

	def river_approach_mirror(self, player: Player):
		self.next_event = "mirror"
		return ("Jonny steps cautiously toward the mirror, its surface rippling slightly "
			f"like water. As Jonny peers into it, something *moves* within the "
			f"reflection—but it’s not Jonny's face staring back. It’s something… else.")

	# ----------------------------------------------------------------------------------------------

	def river_event_monster(self, player: Player):
		self.next_event = "combat"
		return (f"{player.name} kneels down to drink from the river, but just as they do, a "
		  	f"massive creature leaps from the river with a loud splash! {player.name} barely "
			f"manages to dodge as fangs snap at the air. Apparently, this river's not just "
			f"*thirsty*—it’s got some furious company. {player.name} braces for battle as the "
			f"monster snarls and prepares to strike!")
	
	# ----------------------------------------------------------------------------------------------

	def river_event_flotsam(self, player: Player):
		self.shuffle_events()
		rand_num = random.randint(30, 50)
		player.modify_health(rand_num)
		return (f"{player.name} watches the river as they ponder their next move, when suddenly "
			f"a health potion floats down the current, bobbing gently toward them. With a curious "
			f"frown, {player.name} reaches out and grabs it, unsure of how it ended up here. But hey, "
			f"free potion, right? {player.name} drinks it, feeling a rush of rejuvenation. Their health "
			f"recovers {rand_num}, and for once, the river is actually looking out for them!")

	# ----------------------------------------------------------------------------------------------
	
	def river_event_drink(self, player: Player):
		self.shuffle_events()
		rand_num = random.randint(5, 20)
		player.modify_health(-rand_num)
		death_message = player.check_for_death()
		return (f"{player.name} kneels at the river, thirst gnawing at them. After guzzling "
			f"potions, they decide to drink from the river. The water feels cool, but as soon as "
			f"it hits their stomach, they regret it. A burning sensation spreads, making them wish "
			f"they'd stuck with potions. Polluted? Tainted? {player.name} takes {rand_num} damage, "
			f"feeling like the river has a personal vendetta against them. {death_message}")

	################################## Tunnel Fork Events ##########################################

	def tunnel_fork_event(self, player: Player):
		return (f"{player.name} comes to fork in the tunnel. The left path smells musty and "
			f"{player.name} can hear faint sounds of rushing water. To the right a warm "
			"breeze is felt and the path curves up slightly. ")

	# ----------------------------------------------------------------------------------------------

	def tunnel_fork_left_good(self, player: Player):
		self.shuffle_events()
		player.invisibility_potions += 1
		return (f"{player.name} cautiously chooses the left fork of the dimly lit tunnel, their "
			f"footsteps echoing against the damp walls. As they progress, their eyes catch a faint "
			f"glimmer near a pile of rubble. Curiosity outweighs caution, and {player.name} "
			f"brushes aside the debris to reveal a small, intricately carved vial filled with a "
			f"shimmering, translucent liquid. A tattered note tied to its neck reads: \"Drink to "
			f"vanish, but tread wisely. Not for use in locker rooms!\" Realizing it’s an "
			f"invisibility potion, {player.name} tucks it away with a grin, knowing this could be "
			f"the key to slipping past any lurking monsters.")
	
	# ----------------------------------------------------------------------------------------------

	def tunnel_fork_left_bad(self, player: Player):
		self.shuffle_events()
		rand_num = random.randint(10, 30)
		player.modify_health(-rand_num)
		death_message = player.check_for_death()
		return (f"{player.name} ventures down the left fork, hopeful that it leads somewhere useful. "
			f"After a short walk, they stumble upon a strange, sticky substance on the floor. "
			f"Before {player.name} can process what’s happening, their foot gets stuck in the goo, "
			f"and they fall flat on their face. It’s some kind of ancient, gross slime. As they "
			f"struggle to get up, {player.name} realizes the goo is oddly heavy and sticky, "
			f"pulling them down a bit more with every movement. Finally free, {player.name} "
			f"manages to stumble forward, but not without losing {rand_num} health from the "
			f"mishap. It's like the tunnel is trying to prank them… and it’s winning. {death_message}")
	
	# ----------------------------------------------------------------------------------------------

	def tunnel_fork_left_none(self, player: Player):
		return (f"{player.name} walks for quite a while. The tunnel stretches endlessly! "
			f"{player.name} starts jogging, eager to find an end. But the path "
			f"seems endless. Frustrated, {player.name} picks up the pace, running "
			f"faster and faster. Everything looks the same! Finally, {player.name} "
			f"reaches a fork in the tunnel—wait—this looks familiar! {player.name} "
			f"realizes they’ve been running in a massive circle!")
	
	# ----------------------------------------------------------------------------------------------

	def tunnel_fork_right_good(self, player: Player):
		self.shuffle_events()
		player.treasure_keys += 1
		return (f"As {player.name} takes the right fork, a glint catches their eye. "
			f"Could it be... a key? No way! {player.name} picks it up and tries to "
			f"pocket it... but it barely fits in their hand. They giggle to themself, "
			f"hoping they’ll find that treasure chest they *definitely* remember seeing "
			f"somewhere. Or was that just in their dreams? Eh, they’ll figure it out.")
	
	# ----------------------------------------------------------------------------------------------

	def tunnel_fork_right_bad(self, player: Player):
		self.shuffle_events()
		rand_num = random.randint(10, 30)
		player.modify_health(-rand_num)
		death_message = player.check_for_death()
		return (f"{player.name} takes the left fork and walks with newfound confidence. "
			f"As they go, they hear a faint buzzing sound, and before they can react, a swarm of "
			f"annoyed bees flies by, stinging {player.name} on the arms and face! In a flurry of panic, "
			f"{player.name} swats and flails, trying to escape, but only succeeds in making things worse. "
			f"Eventually, the bees disperse, but {player.name} takes {rand_num} damage and is left "
			f"bruised, with a few more scratches than anticipated. Not the best way to spend an "
			f"afternoon! {death_message}")
	
	# ----------------------------------------------------------------------------------------------

	def tunnel_fork_right_none(self, player: Player):
		self.shuffle_events()
		return (f"As {player.name} proceeds down the tunnel, a light can be seen from above—"
				f"daylight! Unfortunately, the light streams from a tall shaft overhead that "
				f"looks completely un-climbable. {player.name} gazes mournfully at the sky and "
				f"the unreachable freedom above.")
	
	# ----------------------------------------------------------------------------------------------

	def tunnel_fork_sing_good(self, player: Player):
		self.shuffle_events()
		player.treasure_keys += 1
		return (f"Feeling a little spontaneous, {player.name} decides to stand around and belt out a "
			f"random song. The tune echoes through the tunnel—surprisingly good acoustics! Just as the last note "
			f"fades, a strange sound interrupts: a metallic clink! {player.name} looks down, and there, glinting "
			f"on the floor, is an old, rusted key. It seems like the tunnel rewards terrible singing. Maybe this key "
			f"will open something… or maybe it’s just a weird coincidence. Either way, {player.name} pockets it, "
			f"feeling oddly accomplished.")
	
	# ----------------------------------------------------------------------------------------------

	def tunnel_fork_sing_bad(self, player: Player):
		self.shuffle_events()
		return (f"{player.name} stands around, confidently singing a song for a few minutes, "
			f"hoping the tunnel might offer some sort of reward. Nothing happens. Not even an echo. "
			f"{player.name} awkwardly clears their throat, looks around, and pretends like they weren't just "
			f"singing to no one. The silence is deafening. It’s a good thing no one else was around to hear that "
			f"performance... or maybe it's a bad thing. Either way, nothing has changed. {player.name} decides "
			f"to move on, slightly embarrassed, but determined.")
	
	# ----------------------------------------------------------------------------------------------

	def tunnel_fork_sing_none(self, player: Player):
		self.shuffle_events()
		if player.treasure_keys > 0:
			lost_item = "a treasure key"
			player.treasure_keys -= 1
		elif player.invisibility_potions > 0:
			lost_item = "an invisibility potion"
			player.invisibility_potions -= 1
		else:
			lost_item = "their smart phone"
		return (f"{player.name} confidently sings a song, expecting something grand to happen. "
			f"Instead, a gust of wind blows through the tunnel and knocks something out of {player.name}'s "
			f"pocket. It tumbles away, disappearing into the darkness. {player.name} scrambles, "
			f"sifting through their pack to find out what had just vanished. {player.name} "
			f"realizes they have just sung {lost_item} out of existence! "
			f"Next time, try humming instead of performing a full concert.")

	#################################### Hallway Events ############################################

	def hallway_event(self, player: Player):
		return (f"{player.name} is in a long, dark cobblestone corridor. Spider webs coat the "
			f"ceiling and lit torches line the walls as if someone were here recently. "
			f"{player.name} sees a sewer grate about 20 feet ahead. There don't seem to be "
			f"many other places that {player.name} can go.")
	
	# ----------------------------------------------------------------------------------------------
	
	def hallway_trap_good(self, player: Player):
		rand_num = random.randint(20, 30)
		player.modify_health(rand_num)
		self.shuffle_events()
		return (f"A loud *click* is heard from a stone under {player.name}'s foot. {player.name} "
		  	f"stepped on a trap! Oh no! "
			f"\nFirey darts shoot out of the walls, but {player.name} quickly evades them. "
			f"The burning darts illuminate a hole in the wall revealing a stashed potion. "
			f"{player.name} grabs the bottle and drinks it to replenish {rand_num} health.")
	
	# ----------------------------------------------------------------------------------------------
	
	def hallway_trap_bad(self, player: Player):
		self.shuffle_events()
		rand_num = random.randint(20, 30)
		player.modify_health(-rand_num)
		death_message = player.check_for_death()
		return (f"A loud *click* is heard from a stone under {player.name}'s foot. {player.name} "
		  	f"stepped on a trap! Oh no! "
			f"\nFirey darts shoot out of the walls wounding {player.name} and causing {rand_num} reduction in health!"
			f"\n{death_message}")
	
	# ----------------------------------------------------------------------------------------------
	
	def hallway_trap_none(self, player: Player):
		self.shuffle_events()
		return (f"A loud *click* is heard from a stone under {player.name}'s foot. {player.name} "
		  	f"stepped on a trap! Oh no! "
			f"\n{player.name} braces for sudden pain but the trap appears to have been a dud. Phew!")
	
	# ----------------------------------------------------------------------------------------------
	
	def trip_good(self, player: Player):
		self.shuffle_events()
		rand_num = random.randint(10, 30)
		player.modify_health(rand_num)
		return (f"While prancing down the corridor, {player.name} suddenly trips over a rock! "
			f"\nAfter getting up and dusting off, {player.name} sees that the rock was actually a health potion!"
			f"\n{player.name} quickly grabs and gulps it down regaining {rand_num} health.")
	
	# ----------------------------------------------------------------------------------------------
	
	def trip_bad(self, player: Player):
		self.shuffle_events()
		rand_num = random.randint(1, 20)
		player.modify_health(-rand_num)
		death_message = player.check_for_death()
		return (f"While prancing down the corridor, {player.name} suddenly trips over a rock! "
			f"\n{player.name} face plants into the hard floor and takes {rand_num} damage! Ouch! "
			f"Maybe next time {player.name} will stick the landing."
			f"\n{death_message}")
	
	# ----------------------------------------------------------------------------------------------
	
	def trip_none(self, player: Player):
		self.shuffle_events()
		return (f"While prancing down the corridor, {player.name} suddenly trips over a rock! "
			f"\nFortunately {player.name} landed in some nice soft mud. Every thing is fine, "
			f"though a little more squishy.")
	
	################################## Sewer Grate Events ##########################################

	def grate_good(self, player: Player):
		rand_num = random.randint(15, 35)
		player.modify_health(rand_num)
		self.shuffle_events()
		return (f"{player.name} removes the bars and finds a ladder leading down into darkness. "
			f"On the way down the ladder {player.name} finds a potion dangling by a string on one "
			f"of the ladder rungs. {player.name} pops the cork and gussles it regaining {rand_num} "
			f"health! Mmmmm! Cherry flavored!")
	
	# ----------------------------------------------------------------------------------------------

	def grate_bad(self, player: Player):
		rand_num = random.randint(25, 40)
		player.modify_health(-rand_num)
		death_message = player.check_for_death()
		self.shuffle_events()
		return (f"{player.name} removes the bars and finds a ladder leading down into darkness. "
			f"While climbing down a rung on the ladder breaks loose! {player.name} falls and "
			f"lands hard taking {rand_num} damage! Owiee! {death_message}")
	
	# ----------------------------------------------------------------------------------------------

	def grate_none(self, player: Player):
		self.shuffle_events()
		return (f"{player.name} removes the bars and finds a ladder leading down into darkness. "
			f"{player.name} slides down the greasy ladder and springs into a fighting stance "
		 	f"at the bottom. No attack comes.")
	
	# ----------------------------------------------------------------------------------------------

	def grate_leprechaun(self, player: Player):
		self.next_event = "leprechaun"
		return (f"{player.name} removes the bars and finds a ladder leading down into darkness. "
			f"After methodically stepping down the ladder, {player.name} splashes into a puddle "
			f"and turns to find a leprechaun sitting in a nook with a burlap sack.")
	
	# ----------------------------------------------------------------------------------------------

	def grate_treasure_room(self, player: Player):
		self.next_event = "treasure_room"
		return (f"{player.name} removes the bars and finds a ladder leading down into darkness. "
			f"{player.name} drops down the hole and lands with a \"clink-clink-clatter\". What's "
			f"this on the floor? {player.name} discovers a room full of treasure!")
	
	################################## Treasure Room Events ########################################

	def treasure_room_event(self, player: Player):
		return (f"In the center of this small chamber is a pile of gold dabloons, on top "
			f"of which sits an ornate treasure chest. There is a rack of old, rusty weapons "
			f"hanging on the wall and an open door leading to another corridor. ")
	
	# ----------------------------------------------------------------------------------------------

	def treasure_room_box_good(self, player: Player):
		rand_num = random.randint(0, 2)
		self.shuffle_events()
		items = ["compass", "vial of troll's blood", "magic ring"]
		if rand_num == 0:
			player.has_compass = True
		if rand_num == 1:
			player.trolls_blood += 1
		if rand_num == 2:
			player.has_magic_ring = True
		item_description = [
			"This looks like it would go well with a map. Hmmm. ",
			f"{player.name} swallows the contents of the vial. Tastes like- green. ",
			(f"As {player.name} slips the ring on, {player.name} is surrounded in a dim light. "
			f"\"My precious!\" All damage {player.name} takes will now be reduced by one third! "
			f"Because I said so! Shut up and keep playing! ")
		]
		return (f"{player.name} climbs the golden pile and grabs the lid of the chest. "
			f"The chest creeks open. {player.name} finds a {items[rand_num]}! "
			f"{item_description[rand_num]}{player.name} is pleased with the loot and stares at it "
			f"wandering out the door forgetting that there was ever anything else in the room.")
	
	# ----------------------------------------------------------------------------------------------

	def treasure_room_box_bad(self, player: Player):
		self.shuffle_events()
		rand_num = random.randint(10, 15)
		player.modify_health(-rand_num)
		death_message = player.check_for_death()
		return (f"{player.name} climbs the golden pile and grabs the lid of the chest. As the lid "
			f"opens, {player.name} is sprayed in the face with posionous gas taking {rand_num} "
			f"damage! Gas continues to fill the room and {player.name} is forced to flee. "
			f"{death_message}")
	
	# ----------------------------------------------------------------------------------------------

	def treasure_room_box_none(self, player: Player):
		self.shuffle_events()
		return (f"{player.name} climbs the golden pile and grabs the lid of the chest. It's "
		  	f"locked and too heavy to move! As {player.name} attempts to pry the chest open "
			f"the stone door to the room starts to slide closed. {player.name} dashes to the door "
			f"to avoid being trapped and barely escapes! The door is now sealed tight.")
	
	# ----------------------------------------------------------------------------------------------

	def treasure_room_rack_good(self, player: Player):
		self.shuffle_events()
		player.weapons.add("Sword")
		self.game_data["combat_weapon"]["options"] = list(player.weapons)
		return (f"{player.name} inspects the weapons on the rack. All are rusty or rotted away "
		  	f"except for a shiny sword that appears to be in pristine condition. This might be "
			f"useful to fight off monsters! {player.name} takes the sword from the rack and jams "
			f"it in a pocket. Ouch! Just then, swarms of venomous spiders begin emerging from "
			f"cracks in the walls. {player.name} must have disturbed a nest and runs out of the room.")
	
	# ----------------------------------------------------------------------------------------------

	def treasure_room_rack_none(self, player: Player):
		self.shuffle_events()
		return (f"Everything on the rack is rusted or rotted away. There is nothing useful here. "
			f"Just then, swarms of venomous spiders begin emerging from cracks in the walls. "
			f"{player.name} must have disturbed a nest and runs out of the room.")
	
	# ----------------------------------------------------------------------------------------------

	def treasure_room_leave_good(self, player: Player):
		player.weapons.add("Magic Book")
		self.game_data["combat_weapon"]["options"] = list(player.weapons)
		self.shuffle_events()
		return (f"{player.name} has seen Indiana Jones more than once and knows what will happen if "
		  	f"any of this cursed treasure is disturbed. {player.name} respecftully bows and starts "
			f"toward the exit. On a bookshelf by the door sits a lone tome. Maybe there is something "
			f"in it that will help {player.name} escape this place. {player.name} grabs the book "
			f"and walks out of the room. On closer inspection, {player.name} sees that the book is "
			f"actually a book of combat magic! Maybe this will help fight away the monsters!")
	
	# ----------------------------------------------------------------------------------------------

	def treasure_room_leave_bad(self, player: Player):
		self.shuffle_events()
		rand_num = random.randint(10, 15)
		player.modify_health(-rand_num)
		death_message = player.check_for_death()
		return (f"{player.name} has seen Indiana Jones more than once and knows what will happen if "
		  	f"any of this cursed treasure is disturbed. {player.name} respecftully bows and starts "
			f"toward the exit. Ironically, {player.name} slips on a pile of gold coins near the "
			f"door and falls taking {rand_num} damage! {death_message}")
	
	# ----------------------------------------------------------------------------------------------

	def treasure_room_leave_none(self, player: Player):
		self.shuffle_events()
		return (f"{player.name} has seen Indiana Jones more than once and knows what will happen if "
		  	f"any of this cursed treasure is disturbed. {player.name} respecftully bows and starts "
			f"toward the exit. {player.name} briefly looks back at the glittering prizes and "
			f"wonders if any of this stuff could have assisted in escaping. Maybe next time.")

	##################################### Yelling Events ###########################################

	def yell_monster(self, player: Player):
		self.next_event = "combat"
		return (f"{player.name} hollers into the darkness and hears an echoing voice followed "
		  	f"by a deep growl. {player.name}'s yells are responded to by a monster!")
	
	# ----------------------------------------------------------------------------------------------

	def yell_throat_hurts(self, player: Player):
		rand_num = random.randint(1, 10)
		player.modify_health(-rand_num)
		death_message = player.check_for_death()
		return (f"{player.name} hollers as loud as possible for several minutes. {player.name}'s "
		  	f"throat now hurts from yelling and takes {rand_num} damage. (Way to go.) "
			f"{death_message}")
	
	# ----------------------------------------------------------------------------------------------
	
	def yell_gnome(self, player: Player):
		self.next_event = "gnome"
		return (f"{player.name} shouts for help. Moments later, a curious looking gnome appears "
		  	f"from around the corner.")
	
	# ----------------------------------------------------------------------------------------------

	def yell_none(self, player: Player):
		return (f"{player.name}'s voice echos down the tunnel, \"can anyone hear me?\". Just then "
		  	f"a reply is heard, \n\"Yes I hear you! Stop playing video games and get back to your "
			f"school work!\". Hmm, I wonder who that was?")
	
	# ----------------------------------------------------------------------------------------------
	
	def yell_collapse_good(self, player: Player):
		rand_num = random.randint(15, 35)
		player.modify_health(rand_num)
		return (f"{player.name} screams and stomps. The tunnel walls begin to quiver. A potion "
		  	f"bottle randomly rolls out of a pipe in the wall! {player.name} slurps it up and "
			f"regains {rand_num} health!")
	
	# ----------------------------------------------------------------------------------------------

	def yell_collapse_bad(self, player: Player):
		rand_num = random.randint(10, 15)
		player.modify_health(-rand_num)
		death_message = player.check_for_death()
		return (f"{player.name} screams and stomps. The tunnel walls begin to quiver. "
			f"Rocks begin to fall from above and and strike {player.name} on the head! "
			f"{player.name} takes {rand_num} damage! {death_message}")
	
	# ----------------------------------------------------------------------------------------------

	def yell_collapse_none(self, player: Player):
		return (f"{player.name} screams and stomps. The tunnel walls begin to quiver. "
		  	f"The roar of large falling rocks can be heard ahead. I hope that didn't block any "
			f"important passages. Oops!")

	##################################### Gnome Events #############################################

	def gnome_event(self, player: Player):
		return "The gnome looks delicious!"
	
	# ----------------------------------------------------------------------------------------------

	def gnome_action(self, player: Player):
		return f"Should {player.name} eat it?"
	
	# ----------------------------------------------------------------------------------------------

	def nummy_gnomey_good(self, player: Player):
		self.shuffle_events()
		player.maximum_health += 30
		return (f"The todler-sized gnome beings to squeak out in its happy little voice, \"I "
			f"know a way out...\" when {player.name} suddenly pounces on it and begins feasting "
			f"on its chocolaty innards. What was that it was about to say? Oh who cares. As "
			f"{player.name} munches on the remainder of the gnomes head, {player.name} feels "
			f"an increase in vitality. {player.name}'s maximum health increases!")
	
	# ----------------------------------------------------------------------------------------------

	def nummy_gnomey_bad(self, player: Player):
		self.shuffle_events()
		rand_num = random.randint(10, 15)
		player.modify_health(-rand_num)
		death_message = player.check_for_death()
		return (f"Gnomercy! The cuddly little gnome squeaks in terror as {player.name} lunges "
		  	f"toward it drooling. Its retreat is in vain as {player.name} scoops the squirmy "
			f"doll creature up and gobbles it down. Moments later {player.name} begins to have "
			f"bad indegestion and takes {rand_num} damage. Gnomaalox! {death_message}")
	
	# ----------------------------------------------------------------------------------------------
	
	def nummy_gnomey_none(self, player: Player):
		self.shuffle_events()
		return (f"{player.name} picks the startled gnome up by the head, and bites off one of "
			f"its legs. The last gnome {player.name} ate tasted much better. {player.name} drops "
			f"the gnome on the floor in disgust and lets it hop away.")
	
	# ----------------------------------------------------------------------------------------------

	def pokey_gnomey_good(self, player: Player):
		self.shuffle_events()
		rand_num = random.randint(15, 35)
		player.modify_health(rand_num)
		return (f"{player.name} breaks a stick off of a sewer tree and suspiciously prods the "
		  	f" gnoblin. The gnome suddenly pops into a shower of confetti leaving only its pointed "
			f"hat behind. Picking it up {player.name} finds a potion inside and chugs it. "
			f"{player.name} regains {rand_num} health!")
	
	# ----------------------------------------------------------------------------------------------
	
	def pokey_gnomey_bad(self, player: Player):
		self.shuffle_events()
		return (f"{player.name} pulls a walking stick from their pocket and jabs the gnome in the "
		  	f"eye. The gnome becomes enraged, growls, and viciously attacks {player.name}!")
	
	# ----------------------------------------------------------------------------------------------
	
	def pokey_gnomey_none(self, player: Player):
		self.shuffle_events()
		return (f"{player.name} pulls out the breadstick left over from lunch and extends it "
		  	f"toward the gnome. In a flash, the gnome snatches it away and gobbles it up. "
			f"\"Thanks!\" it says as it dissapears into the darkness. {player.name} was going to "
			f"eat that. How rude!")
	
	# ----------------------------------------------------------------------------------------------
			  
	def dirpy_gnomey_good(self, player: Player):
		self.shuffle_events()
		player.trolls_blood += 1
		return (f"\"What are you doing here cute little guy?\" {player.name} asks. The gnome "
		  	f"sniffles, and begins to tear up. \"Did you say 'cute'?\" After about five minutes "
			f"of sobbing, the gnome pull a vial of green liquid from its beard and offers it to "
			f"{player.name}. \"This is troll's blood.\" he begins to explain. \"You can use it "
			f"to...\" *gulp* {player.name} swallows the last drop while inattentively staring off "
			f"in another direction. \"Oh dear!\" exclaims the gnome. Was {player.name} supposed "
			f"to do that?")
	
	# ----------------------------------------------------------------------------------------------
	
	def dirpy_gnomey_bad(self, player: Player):
		self.next_event = "combat"
		return (f"{player.name} stares silently at the gnome. It sniffs and begins making an odd "
			f"growling sound. The gnome begins increasing in size and transforms into a monster!")
	
	# ----------------------------------------------------------------------------------------------
		  	
	def dirpy_gnomey_none(self, player: Player):
		self.shuffle_events()
		return (f"{player.name} decides there is no time to entertain a short-stack and punts it "
		  	f"down the nearest open grate. \"I can't reach the ground fast enough!\" it yells as "
			f"as it decends into the dark abyss. Time to focus on more important things.")

	################################### Leprechaun Events ##########################################
	
	def leprechaun_event(self, player: Player):
		return (f"The little green-dressed leprechaun, who looks like he came straight "
			f"off a cereal box, dives right into pleasantries and introduces himself as "
			f"'Stinky'. \"It's dangerous to go alone! Take this.\" he says as he holds his "
			f"bag open in front of {player.name}. Where has {player.name} heard that line "
			f"before? It looks like there are several things in that bag but for some "
			f"reason, {player.name} knows only to take one item. Can this leprechaun be "
			f"trusted? ")
	
	# ----------------------------------------------------------------------------------------------
	
	def leprechaun_bag_good(self, player: Player):
		self.shuffle_events()
		item_list = ["potion", "vial to troll's blood", "quarter staff", "treasure_key"]
		rand_item_num = random.randint(0, 3)
		rand_health_num = random.randint(15, 25)
		player.modify_health(rand_health_num if rand_item_num == 0 else 0)
		if rand_item_num == 2:
			player.trolls_blood += 1
		if rand_item_num == 2:
			player.weapons.add("Staff")
			self.game_data["combat_weapon"]["options"] = list(player.weapons)
		if rand_item_num == 3:
			player.treasure_keys += 1
		item_description = [
			f"Just what {player.name} needed! {player.name} pops the lid and gulps it down "
				f"regaining {rand_health_num} health! {player.name} then bids farewell to "
				f"Stinky. Maybe {player.name} will encounter him again?",
			f"Well that sure looks tasty! {player.name} tips the contents of the vial and "
				f"gulps it down. \"No! You are supposed to... oh nevermind.\" Stinky says as "
				f"{player.name} licks the remaining fluid from the opening of the vial. Feeling "
				f"a bit loopy, {player.name} wanders away toward visions of sugar plumbs.",
			f"How did Stinky fit a 6' pole in that little sack? What does it matter? {player.name} "
				f"should be able to use this to fight back the monsters. "
				f"\n\tNew weapon: Staff - Occasionally lands multiple blows to monsters.",
			f"Hmm, this could be used to pick {player.name}'s nose. Also, it could open something. "
			f"Stinky scurries away into the darkness."
		]
		return (f"{player.name} reaches blindly into the bag and grabs ahold of something. "
			f"{player.name} pulls out a {item_list[rand_item_num]}! {item_description[rand_item_num]}")
	
	# ----------------------------------------------------------------------------------------------
				  
	def leprechaun_bag_bad(self, player: Player):
		self.shuffle_events()
		damage_type = random.randint(0, 4)
		damage_amount = random.randint(5, 10)
		player.modify_health(-damage_amount)
		death_message = player.check_for_death()
		damage_event = ["bit by a venomous spider ", "stung by a scorpion ", "bit by a snake ",
			"stung by a large wasp ", "pricked by a rusty nail "]
		return (f"{player.name} reaches blindly into the bag and grabs ahold of something. "
			f"Oww! {player.name} was {damage_event[damage_type]} inside the bag and takes "
			f"{damage_amount} health damage! \"Sorry fer that,\" Stinky says unapologetically, "
			f"\"but ye are only allowed to reach into this here bag once per visit.\" Stinky "
			f"ties his bag shut and scurries off. How unfortunate. Maybe you will see him again? "
			f"{death_message}")
	
	# ----------------------------------------------------------------------------------------------

	def leprechaun_bag_none(self, player: Player):
		self.shuffle_events()
		rand_num = random.randint(0,5)
		rand_item = ["a pink stuffed bunny", "a solar-powered flashlight", "a stack of coupons ",
			"a broken umbrella", "a soggy newspaper", "an AOL CD"]
		return (f"{player.name} reaches blindly into the bag and grabs ahold of something. "
		  	f"{player.name} pulls {rand_item[rand_num]} out of the bag. Great. This will be "
			f"so useful as {player.name} struggles for life in a hostile underworld. \"Thank you "
			f"fer yer business. See ya next time!\" says Stinky as he dissapears in a cloud of "
			f"smoke. 'Next time?'")
	
	# ----------------------------------------------------------------------------------------------
	
	def leprechaun_walk_good(self, player: Player):
		self.shuffle_events()
		return (f"{player.name} looks the little green half-pint up and down. Wheel and deal with this "
			f"sketchy character? Ain't nobody got time for that! As {player.name} starts to walk "
			f"away, Stinky shouts, \"Wait! Perhaps ye be interested in finding a way out of this "
			f"here dark maze. I have a map, see, that will show ya how to escape, but I'll only "
			f"give it to ya if you rid this dungeon of at least 5 monsters. Also, you will be "
			f"need'n a compass to use it, but I don't have one. What do ya say?\" It sounds "
			f"like {player.name} doesn't have much of a choice and agrees to do the leprechaun's "
			f"dirty work of monster slaying. {player.name} reluctantly agrees and wanders off.")
	
	# ----------------------------------------------------------------------------------------------

	def leprechaun_walk_bad(self, player: Player):
		self.shuffle_events()
		rand_num = random.randint(30, 50)
		player.modify_health(-rand_num)
		death_message = player.check_for_death()
		return (f"{player.name} looks the little green half-pint up and down. Wheel and deal with this "
			f"sketchy character? Ain't nobody got time for that! As {player.name} turns around to walk "
			f"away, Stinky pulls a knife from his bag and stabs {player.name} in the back! Oh no! It "
			f"was the leprechaun from THAT movie! {player.name} takes {rand_num} damage! {death_message}")
	
	# ----------------------------------------------------------------------------------------------
	
	def leprechaun_ask_good(self, player: Player):
		self.shuffle_events()
		player.modify_health(9999999)
		return (f"{player.name} suspiciously asks the leprechaun what is in the bag. \"Perhaps it "
		  	f"be best if I show ya! Try a sample of this here potions. Satisfaction guarenteed!\" "
			f"{player.name} takes the bottle of purple liquid from Stinky and gulps it down. "
			f"{player.name}'s health fully recovers! Wow! What else does Stinky... where'd he go?")
	
	# ----------------------------------------------------------------------------------------------
		  
	def leprechaun_ask_bad(self, player: Player):
		self.shuffle_events()
		rand_num = random.randint(1, 30)
		player.modify_health(-rand_num)
		death_message = player.check_for_death()
		return (f"{player.name} suspiciously asks the leprechaun what is in the bag. \"Perhaps it "
		  	f"be best if I show ya! Try a sample of this here potions. Satisfaction guarenteed!\" "
			f"{player.name} takes the bottle of inky liquid from Stinky and gulps it down. "
			f"{player.name} becomes momentarily blind and walks into the wall taking {rand_num} "
			f"damage! When {player.name}'s vision returns, Stinky is gone. That little troll! "
			f"{death_message}")
	
	# ----------------------------------------------------------------------------------------------
	
	def leprechaun_ask_none(self, player: Player):
		self.shuffle_events()
		return (f"{player.name} suspiciously asks the leprechaun what is in the bag. Stinky "
			f"says excitedly, \"I'm glad ye asked! From the far reaches of Centrailia I have "
			f"baubles, doodads, and gizmos. I have acquired 80 nickknacks from Grumblethorp! Ye "
			f"want thingamajigs? I've got 20! But who cares? No big deal. I've got more!\" Stinky "
			f"continues on and on listing non-sensical items he has proudly acquired from places "
			f"that sound entirely made up. {player.name}'s eyes begin to glaze over. "
			f"After 10 minutes of this {player.name} decides to wander off.")
	
	################################# Miscellaneous Events #########################################

	def monster_encounter(self, player: Player):
		self.next_event = "combat"
		return (f"As {player.name} takes a step forward, a loud rustling comes from the shadows. "
			f"Before they can react, a giant, furry monster leaps out with a terrifying roar! "
			f"Well, that was unexpected. {player.name} stumbles back, face pale, as the creature "
			f"snarls and shows way too many teeth for comfort. There’s no time to panic – it’s "
			f"fight-or-flight time!")
	
	# ----------------------------------------------------------------------------------------------

	def nothing(self, player: Player):
		return (f"{player.name} moves a bit, then stands there for a moment, pondering the vast unknown. "
			f"They scratch their head, glance around, and take a deep breath, only to realize "
			f"they haven't actually done anything at all. Well, sometimes it’s nice to just... exist. "
			f"After a few seconds of deep, philosophical reflection, they decide to keep moving. "
			f"Maybe next time something will happen...")
	
	# ----------------------------------------------------------------------------------------------
	
	def death(self, width):
		border = Utilities.create_ruler(width, 'X')
		death_message = "You have failed your quest!"
		game_over = "G A M E   O V E R !"
		print(f"{border}\n{death_message.center(width)}\n{game_over.center(width)}\n{border}")
		input()

	# ----------------------------------------------------------------------------------------------

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

	# ----------------------------------------------------------------------------------------------

	def find_treasure_chest(self, player):
		if player.treasure_keys == 0: 
			outcome = (
				f"After a while of wandering, {player.name} spots a nook in the wall. "
				f"Inside, they see a locked treasure chest, just waiting to be opened. "
				f"They bend down to check it out, only to realize—uh-oh! They don’t have a key! "
				f"{player.name} tries shaking it, hoping for the best, but the chest isn’t budging. "
				f"Guess it’ll just have to stay a mystery for now. Maybe next time {player.name} "
				f"will come across a key—or a crowbar. Who knows?")
		else:
			rand_num = random.randint(0, 4)
			rand_health = random.randint(10, 30)
			player.treasure_keys -= 1
			if rand_num == 0:
				player.modify_health(rand_health)
			if rand_num == 1:
				player.trolls_blood += 1
			if rand_num == 2:
				player.invisibility_potions += 1
			if rand_num == 3:
				player.maximum_health += 30
				player.modify_health(-20)
			if rand_num == 4:
				player.treasure_keys += 1
			items = [" potion", " vial of troll's blood", "n invisibility potion", " mega health pack", " treasure key"]
			item_description = [
				(f"{player.name} hopes this one will taste different than the other and slams it down. "
					f"Nope. At least {player.name} regained {rand_health} heath!"),
				(f"Having no idea what this is actually does to the human body, {player.name} "
	 				f"guzzles it and hopes for the best. Mmmmm! Thick and gooey!"),
				(f"It's one of those sneaky sneaky things to escape from monsters! Yay!"),
				(f"Inside is {player.name} discovers a stash of food! A fresh sandwich, some "
					f"fruit, and even a mysterious drink that looks like it’s from the future! "
					f"{player.name} devours it all with reckless abandon, thinking, 'This’ll fix "
					f"Sure enough, {player.name} feels tougher, but also maybe a little "
					f"sicker? Oh well, worth it! {player.name} looses 20 health, but gains 30 to "
					f"maximum health."),
				(f"...a treasure key just like the one {player.name} used to open this chest. Yay.")
			]
			outcome = (
				f"After a while of wandering, {player.name} spots a nook in the wall. "
				f"Inside, they see a locked treasure chest. {player.name} grins, realizing "
				f"they actually have a key! They eagerly shove the key into the lock, "
				f"turn it, and—voila! The chest creaks open with a satisfying sound. "
				f"Inside, {player.name} finds a{items[rand_num]}! {item_description[rand_num]} "
				f"{player.name} attempts to remove the key from the chest, but as expected, "
				f"it is stuck tight. I guess these keys are a one-time use."
			)
		return outcome

	#################################### Event Helpers #############################################

	def populate_event_functions(self, data):
		for key, value in data.items():
			if isinstance(value, dict):
				self.populate_event_functions(value)
			elif isinstance(value, list):
				for item in value:
					if callable(item):
						self.all_event_functions.add(item)
			elif callable(value):
				self.all_event_functions.add(value)

	# ----------------------------------------------------------------------------------------------
				
	def initialize_event_frequencies(self):
		for event in list(self.all_event_functions):
			self.event_frequencies[event] = 1
				
	# ----------------------------------------------------------------------------------------------				

	def shuffle_events(self):
		main_events = ["hallway", "tunnel_fork", "river"]
		self.next_event = self.get_event_using_frequency(main_events, self.main_event_frequencies)

	# ----------------------------------------------------------------------------------------------
		
	def generic_action_prompt(self, player: Player):
		return f"What should {player.name} do?"
	
	# ----------------------------------------------------------------------------------------------		

	# Returns an event based on how frequently it has been used so far. Less frequent = higher chance.
	def get_event_using_frequency(self, event_possibilites, event_frequencies):
		inverse_occurences = []	
		for i in range(len(event_possibilites)):
			inverse_occurences.append(1 / (event_frequencies[event_possibilites[i]]))
		result = random.choices(event_possibilites, weights=inverse_occurences, k=1)
		event_frequencies[result[0]] += 1
		return result[0]