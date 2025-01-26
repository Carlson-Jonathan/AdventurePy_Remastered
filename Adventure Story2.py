import Save1
import random
import time
inventory=["1.Bare fists"]
health=100
M=0
monsters = ["slime","goblin","vampire bat","skeleton","giant rat","cobra","troll","troglodyte","golem","giant spider"]
quest=[]

def death():
	raw_input( "%s is fatally wounded and dies squirming and gasping!"%name)
	x=["\n\n    Y O U","    H A V E","    F A I L E D","    Y O U R","    Q U E S T !"]
	for i in x:
		time.sleep(.4)
		print i
		print '\a'
	time.sleep(1)
	print "\nG  A  M  E     O  V  E  R  !\n\n"
	raw_input()
	exit()

def travel():
	try:
		x=int(raw_input("The corridor continues. There is also a great about 20 feet ahead. Where should %s go?\n1.Continue down the corridor\n2.Climb down the grate\n3.Yell for help\n4.Save Game\n\n>>"%name))
	except ValueError:
		print "That is not a valid input. Try again."
		travel()
	if x==1:
		HallWay()
	if x==2:
		Grate()
	if x==3:
		Yell()
	if x==4:
		print "\tGame saved.\n"
		with open('Save1.py','w') as open_file:
			open_file.write("health=%d\ninventory=%s\nquest=%s\nM=%d\nname='%s'"%(health,inventory,quest,M,name))
		travel()
	else:
		print "That is not an option. Try again."
		travel()
		
def travel2():
	try:
		x=int(raw_input("There is another dark hallway. To the right %s sees a ladder leading up to somehwere else. \nWhere should %s go?\n1.Down the dark hallway\n2.Climb up the ladder\n3.Yell for help\n\n>>"%(name,name)))
	except ValueError:
		print "That is not a valid input. Try again."
		travel()
	if x==1:
		HallWay()
	if x==2:
		Grate()
	if x==3:
		Yell()
	else:
		print "That is not an option. Try again."
		travel()
		
def fists():
	d=random.randint(1,15)
	return d

def sword():
	d=random.randint(12,25)
	return d
	
def fire():
	d=random.randint(1,40)
	return d
	
def knuckles():
	d=random.randint(5,15)
	return d
	
def staff():
	d=random.randint(8,20)
	return d
	
def double():
	d=random.randint(1,22)
	return d
	
def weps():
	print'''
		%s walks down the corridor and finds a sword, a spell 
		book (fireball), and some brass knuckles. 
		For some random reason, %s decides only to take one.
		What will %s take?
		
			1. sword
			2. spell book
			3. brass knuckles
			''' %(name,name,name)
	try:
		x=int(raw_input(">>"))
	except ValueError:
		print "That is not a valid input. Try again."
		weps()
	if x==1:
		if "2.Sword" in inventory:
			raw_input("%s takes the sword and walks away only to realize there is already a sword in the inventory.\n%s dosent need two so decides to drop it and continues down the corridor.\n"%(name,name))
			HallWay()
		else:
			raw_input("%s now has a shiney pointy thing to stab monsters with! Boo-yaa! %s feels safe!\n"%(name,name))
			inventory.insert(1,"2.Sword")
	elif x==2:
		if "3.Fire" in inventory:
			raw_input("%s takes the fire spell and walks away only to realize there is already a fire spell in the inventory.\n%s dosent need two so decides to drop it and continues down the corridor.\n"%(name,name))
			HallWay()
		else:
			raw_input("%s can now shoot fire from the hands, eyes and butt! Monsters beware!\n"%name)
			inventory.insert(2,"3.Fire")
	elif x==3:
		if "4.Brass Knuckles" in inventory:
			raw_input("%s takes the knuckles and walks away only to realize there is already knuckles in the inventory.\n%s dosent need two so decides to drop it and continues down the corridor.\n"%(name,name))
			HallWay()
		else:
			raw_input("%s now can hit harder with fists! Lets get ready to rumbllllleeeeeeee!\n"%name)
			inventory.insert(3,"4.Brass Knuckles")
	else:
		print "Try selecting something from the list instead of just mashing keys!"
		weps()
	travel()
	#x=(int(raw_input("The corridor continues. There is also a grate in the floor.\n%s will: \n1.Continue down the hall\n2.Climb down the grate\n>"%name)))
	#if x==1:
	#	HallWay()
	#else:
	#	Grate()
def weapons(w):
	if w==1 or w==6:
		return fists()
	elif w==2:
		return sword()
	elif w==3:
		return fire()
	elif w==4:
		return knuckles()
	elif w==5:
		return staff()
	
def Battle():
	print "%s's health is currently %d.\n"%(name,health)
	try:
		x=int(raw_input("What action will %s take?\n\n1.Attack\n2.Run Away\n>"%name))
	except ValueError:
		print("Invalid input. Try again.")
		Battle()
	if x==1:
		attack(1)
	elif x==2:
		x=random.randint(1,2)
		if x==1:
			raw_input("%s sucessfully escaped! Yay! (chicken!)"%name)
			raw_input("%s flees down the corridor.\n"%name)
			HallWay()
		elif x==2:
			print "%s is cornered and cant escape! %s has not choice but to fight.\n"%(name,name)
			attack(1)
	else:
		print "Invalid input. Try again.\n"
		Battle()
def attack(weapon):
	global M
	global health
	global name
	global quest 
	global inventory
	print "\nChoose %s's weapon: \n"%name
	for i in inventory:
		print i
	try:
		x=int(raw_input("\n>"))
		monster=random.randint(60,130)
		if x==1:
			raw_input("No weapon. This will be a tough fight! Good luck! \n(1-15 damage)")
		elif x==2 and "2.Sword" in inventory:
			raw_input("Ahh, a trusty sword! Reliable damage and can be used to parry and ripost. \n(12-25 damage)")
		elif x==3 and "3.Fire" in inventory:
			raw_input("The unstable but devestating power of fire! Mwwaaahahaahhaahaa! \n(1-50 damage + burn effect!)")
		elif x==4 and "4.Brass Knuckles" in inventory:
			print "Not extreemly powerful but carefully aimed blows will give %s the advantage!\n(5-15 damage)"%name
		elif x==6 and "6.Invisibility Potion" in inventory:
			print "%s drinks the invisibility potion and fades away. %s is able to slip past the monster and escape\ndown the corridor! Only moments later, the potion suddenly wears off.\n"%(name,name)
			inventory.remove("6.Invisibility Potion")
			travel()
			#try:
			#	x=int(raw_input("Where should %s go next?\n1.Corridor\n2.Grate"))
			#except ValueError:
			#	
			#if x==1:
			#	HallWay()
		elif x==5 and "5.Staff" in inventory:
			print "The quarter staff. Light and swift! (8-20 damage) Occasionally lands multiple hits."
		else:
			print "%s doesn't have that weapon. Pick again."%name
			attack(1)
	except ValueError:
		print("Invalid input. Try again.")
		attack(1)
	raw_input(  "\n\n      		  T I M E   T O   F I G H T ! ! !\n")
	w=1
	while monster>0:
		w+=1
		c=0
		if w%5==0:
			try:
				f=int(raw_input("How do you feel like this fight is going?\n\n1.Change weapons\n2.Run Away\n3.Keep Fighting!\n\n>"))
			except ValueError:
				print "Invalid input. Try Again."
				w-=1
				continue
			if f==1:
				print "\nChoose %s's new weapon:"%name
				for i in inventory:
					print i
				try:
					x=int(raw_input(">"))
				except ValueError:
					print "Input invalid. Try again."
					continue
			elif f==2:
				f=random.randint(1,2)
				if f==1:
					raw_input("%s sees a grate and dives down it.\n"%name)
					raw_input("%s sucessfully escaped! Yay! (chicken!)"%name)
					Grate()
				else:
					print "%s is cornered and cant escape! %s has not choice but to fight.\n"%(name,name)
					raw_input("   The monster attacks %s durring the escape attempt doing 8 damage!"%name)
					health-=8
					print "   %s's health is reduced to %d!\n"%(name,health)
			elif f==3:
				pass
			else:
				print "Invalid input. Try again."
				w-=1
				continue
		if x==2 and "2.Sword" in inventory or x==3 and "3.Fire" in inventory or x==4 and "4.Brass Knuckles" in inventory or x==5 and "5.Staff" in inventory:
			d=weapons(x)
		else:
			d=weapons(1)
		if x==5 and "5.Staff" in inventory:
			if (double())in range(14,19):
				print "            D O U B L E   S T R I K E !"
				print "   %s strikes the monster twice with the staff!"%name
				print "   %s attacks the monster and does %d damage!"%(name,d)
				monster-=d
				d=weapons(5)
			elif double()>18:
				print "            T R I P L E   S T R I K E !"
				print "   %s strikes the monster three times with the staff!"%name
				print "   %s attacks the monster and does %d damage!"%(name,d)
				monster-=d
				d=weapons(5)
				print "   %s attacks the monster and does %d damage!"%(name,d)
				monster-=d
				d=weapons(5)
				monster-=d
			elif double()==1:
				raw_input("   %s beging showing off his ninja skills and twirls the staff...\n   %s then unleashes a devastating flurry of blows!"%(name,name))
				print "\n             S U P E R   C O M B O ! ! !"
				print "   %s strikes the monster repeatedly!"%name
				print "   %s attacks the monster and does %d damage!"%(name,d)
				monster-=d
				d=weapons(5)
				print "   %s attacks the monster and does %d damage!"%(name,d)
				monster-=d
				d=weapons(5)
				print "   %s attacks the monster and does %d damage!"%(name,d)
				monster-=d
				d=weapons(5)
				print "   %s attacks the monster and does %d damage!"%(name,d)
				monster-=d
				d=weapons(5)
		raw_input("   %s attacks the monster and does %d damage!"%(name,d))
		monster-=d
		if x==3:
			u=random.randint(4,10)
			print "   The monster is on fire and takes an additional %d damage!"%u
			monster-=u
		c=random.randint(1,21)
		z=0
		z=random.randint(1,11)
		if monster<=0:
			break
		if (z<=6 and x==2) or (z<=5 and x==4) or (x!=2 and x!=4):
			raw_input("\n      The monster counter attacks and %s takes %d damage!"%(name,c))
			health-=c
			print "      %s's health is reduced to %d!\n"%(name,health)
			if health<=0:
				death()
		elif z in range(7,11) and x==2:
			d=random.randint(12,25)
			raw_input("\n      The monster retaliates but %s parrys the attack with the sword\n      and counters doing %d more damage to the monster!\n"%(name,d))
			monster-=d
		elif z in range(5,11) and x==4:
			raw_input("\n      A well-placed blow with the brass knuckles knocks the monster to the ground\n      and the monster is unable to attack!\n")
		if "Troll's Blood" in quest:
			p=random.randint(3,7)
			raw_input("   %s feels the revitalizing effects of the trolls blood and regenerates %d health!"%(name,p))
			health +=p
			if health >100:
				health=100
			print "   %s's health inceases to %d!\n"%(name,health)
	raw_input("\nThe foul beast begins squirting blood and \nwrithes under %s's last strike before dying!"%name)
	raw_input("%s gains 200 experience points which will never be used for anything!"%name)
	M+=1
	raw_input("%s has killed %d monsters today."%(name,M))
	raw_input("After cutting some body parts off the foe to keep as a trophies %s continues on the journey."%name)
	travel()
	#if x==1:
	#	HallWay()
	#elif x==2:
	#	Grate()
	#else:
	#	Yell()
		
def HallWay():
	global quest 
	global health
	global inventory
	global name
	global M
	if "map" in quest and "compass" in quest:
		print '''
	%s realizes that with a compass and a map in the inventory, a 
	way can be found out of the labrynth! After carefully examining
	them %s decides to turn left and go through the door with 
	the giant 'EXIT' sign that was there the while time. Eureka!
	%s feels the warm sun, a calm breeze and a rushing releif. %s 
	has finally escaped the labrynth thanks to you! :D :D :D
	'''%(name,name,name,name)
		raw_input()
		print""
		raw_input("	C O N G R A T U L A T I O N S ! ! ! !   Y O U   W I N ! ! !\n\n")
		print '''
				Credits:
						
		Story writer 		Jonathan Carlson
		Graphic artist		Jonathan Carlson
		Graphic assistant	Jonathan Carlson
		Developer		Jonathan Carlson
		Producer		Jonathan Carlson
		Game Architect		Jonathan Carlson
		Accountant		Jonathan Carlson
		Director		Jonathan Carlson
		Music Scores by		Jonathan Carlson
		Debugger		Jonathan Carlson
		Purchasing		Jonathan Carlson
		Lunch Guy		Jonathan Carlson
		Assistant lunch guy	Jonathan Carlson
		'''
		raw_input()
		print 		'''
						
			Special Thanks To:
						
		My Honey for helping me test this thing
		"Lets Learn Python from YouTube"
		Elinor for bringing me a sandwich
		Wesley for distracting Jamey
		Jamey for not screaming too loud
		Whoever else plays this and doesnt think it sucks.
		'''
		raw_input("Thanks for paying! Press any key to quit.")
		exit()
				
	x=random.randint(1,3)
	if x==1:
		raw_input("After a few steps, %s steps on a trap! Oh no!\n"%name)
		x=random.randint(1,3)
		if x==1:
			c=0
			c=random.randint(1,11)
			print "%s is now injured and takes %d points of damage! Ouch!\n"%(name,c)
			health-=c
			print "%s's health is reduced to %d"%(name,health)
			if health<=0:
				death()
		elif x==2:
			print "The trap was a dud and %s is safe! Phew!\n"%name
		else:
			raw_input("Arrows shoot out of the wall but %s jumps out of the way just in time!\n"%name)
			raw_input("%s notices a potion in one of the holes where arrow shot from and drinks it."%name)
			raw_input("%s gains 30 health!\n"%name)
			health+=30
			if health >100:
				health=100
			print "%s's health is now %d.\n"%(name,health)
		travel()
		#x=int(raw_input("The corridor continues. \n1.Keep going \n2.Turn around and go down the grate\n>"))
		#if x==1:
		#	HallWay()
		#else:
		#	Grate()
	elif x==2:
		if ("2.Sword" or "3.Fire" or "4.Brass Knuckles") in inventory:
			x=random.randint(1,4)
			if x==1:
				weps()
			else:
				try:
					raw_input("%s comes to a fork. Should %s go left or right?\n1.Left\n2.Right\n>."%(name,name))
				except ValueError:
					print "Invalid input. Kicking you down hallway."
					HallWay()
		else:
			weps()
	else: 
		raw_input("A monster suddenly jumps out of the darkness!")
		raw_input("%s encounters a %s!!\n" %(name,random.choice(monsters)))
		Battle()	
def Grate():
	x=random.randint(1,4)
	if x==1:
		grate1()
	elif x==2:
		grate2()
	elif x==3:
		grate3()
	elif x==4:
		grate4()

#	global health
#	global quest
#	global inventory
#	global name
#	global M
#	x=random.selectGrate
#	if x==1:
def grate1():
	global health
	c=0
	c=random.randint(1,11)
	print"A rung on the ladder is loose and %s falls taking %d points of damage! OUCH!" %(name,c)
	health-=c
	print "%s's health is reduced to %d"%(name,health)
	if health<=0:
		death()
	print '''
	%s gets up and stand in another corridor.
	In one direction can be seen a pair of sinister 
	glowing yellow eyes in the darkness. What should %s do?

	1.Go down the corridor toward the eyes
	2.Turn and run the other way
	3.Stand around and sing a little song
	'''%(name,name)
	grate12()
def grate12():
    try:
    	x=int(raw_input("%s will: "%name))
    except ValueError:
    	print "Invalid input. Try again.\n>>"
    	grate12()
    if x==1:
    	raw_input("%s courageously approaches the glowing eyes.\n"%name)
    	x=random.randint(1,3)
        if x==1:
			raw_input("It turns out the eyes were actually gemstones glittering in the darkness!\n")
			raw_input("Aww, they are lodged in the wall and %s can't get them out.\nThey do however, make %s feel better for some unknown reason.\n%s's health increases 40 points!"%(name,name,name))
			health+=40
			if health >100:
				health=100
			travel2()				
        elif x==2:
            raw_input("The eyes belong to a giant ravenous monster! There is no espcape! Time to fight!")
            raw_input("%s encounters a %s!!\n" %(name,random.choice(monsters)))
            Battle()
	elif x==3:
		raw_input("False alarm! The eyes in the dark were just a trick of the light. %s is safe."%name)
		travel2()
		#x=int(raw_input("Should %s\n1.Walk some more\n2.Go down another grate\n> "%name))
		#if x==1:
		#	HallWay()
		#else:
		#	Grate()
	elif x==2:
		print "%s bolts down the corridor like a screaming like a coward!\n"%name
		HallWay()
	elif x==3:
		grate13()
def grate13():
	print '''
	What song should %s sing?
	1. Mary had a little lamb
	2. The Star Spangled Banner
	3. "I like big butts and I cannot lie...!"
		''' %name
	try:
		x=(int(raw_input(">")))
	except ValueError:
		print "Invalid input. Try again."
		grate13()
	if x==1:
		raw_input("A mysterious porthole opens and %s is sucked into a different part of the story...\n"%name)
		Yell()
	elif x==2:
		raw_input("The big yellow eyes become angry big yellow eyes and attack!")
		raw_input("%s encounters a %s!!\n" %(name,random.choice(monsters)))
		Battle()
	else:
		print "Invalid input. Try again."
		grate13()
def grate2():
	global health
	#elif x==2:
	raw_input("%s discovers a leprecaun sitting at the bottom." %name)
	print '''
The leprechaun introduces himself as Stinky. Seeing that %s is
in distress, Stinky offers something from his bag of
goodies sitting in the corner. 
It could be a trick. Should %s take a look?
1. Yes   2. No'''%(name,name)
	try:
		x=int(raw_input(">"))
	except ValueError:
		print "Invalid input. Try again."
		grate2()
	if x==1:
		x=random.randint(1,11)
		if x<9:
			print '''
Stinky spreads a few items in front of %s. 
Most are usless trinkets but %s notices some useful items 
that could help escape the labrynth. Which will %s take?

	1. Potion
	2. Staff
	3. Map	
	4. Vial of Troll's Blood		
	''' %(name,name,name)
			x=(int(raw_input(">")))
			if x==1:
				raw_input("%s takes the potion and drinks it. %s gains 30 health!\n"%(name,name))
				health+=30
				if health >100:
					health=100
				print "%s's health is now %s."%(name,health)
			elif x==2:
				print "A long, sturdy looking peice of wood. This should help you fight off monsters."
				inventory.insert(4,"5.Staff")
				HallWay()
			elif x==3:
				raw_input("Stinkey says that is his special map that shows how to get out of the labrynth.\nHe is only willing to part with it if %s kills 5 monsters for him."%name)
				if M>=5:
					raw_input("Seeing the amount of monster blood dripping from %s's clothing,\nStinky is convinced that %s has completed his task.\n"%(name,name))
					quest.append("map")
					HallWay()
			elif x==4:
				raw_input("%s takes the vial of troll's blood and gulps it down. \nWas that what %s was supposed to do with it?"%(name,name))
				quest.append("Troll's Blood")
			raw_input("After taking what %s needs the adventure continues down the corridor."%name)
			HallWay()
		else:
			raw_input("It WAS a trick! While %s is discracted\nStinkey pulls a knife out from under his coat and stabs %s!\n%s takes 50 damage and Stinky dissapears into the darkness."%(name,name,name))
			health-=50
			print "%s's health is now %d"%(name,health)
			if health<=0:
				death()
			raw_input("%s limps down another corridor"%name)
			HallWay()
	elif x==2:
		raw_input("%s decides Stinky's odor is too potent and moves on down the corridor."%name)
		HallWay()
	else:
		print "Invalid input. Try again."
		grate13()
def grate3():
	global health	
	#elif x==3:
	raw_input("%s find a potion of invisibility! This should help %s sneak past monsters!"%(name,name))
	#if "6.Invisibility Potion" in inventory:
	#	raw_input("%s takes the potion and walks away only to realize there is already a potion in the inventory.\n%s dosent need two so decides to drop it.\n"%(name,name))
	#else:
	inventory.insert(5,"6.Invisibility Potion")
	travel2()
	#if x==1:
	#	HallWay()
	#else:
	#	Yell()
#else:
def grate4():	
	global health
	raw_input( "%s climbs the ladder and discovers a secret room filled with treasure!\n" % name)
	print "Unfortunately, treasure wont do %s much good while trying to stay alive in a labrynth.\nThere is a compass and a potion on the top of the treasure hoard. %s can take only 1...\n...because I said so. Which should %s grab before going back up the ladder?\n"%(name, name,name)
	try:
		x=int(raw_input("1.Potion\n2.Compass\n>"))
	except ValueError:
		print "Invalid input. Try again."
		grate4()	
	if x==1:
		raw_input("%s decides to drink the potion and regains 30 health.\n%s continues down the corridor.\n"%(name,name))
		health+=30
		if health >100:
			health=100
		print "%s's health is now %d"%(name,health)
	elif x==2:
		print "%s takes the compass and heads out down the corridor. Hmm, this might be an important item..." %name
		quest.append("compass")
		HallWay()
	else:
		print "Invalid input. Try again."
		grate4()
		
def Yell():
	global quest
	global health
	global inventory
	global name
	global M
	x=random.randint(1,3)
	if x==1:
		print "%s's screams are heard by a giant monster that looks hungry!" %name
		raw_input("%s encounters a %s!!\n" %(name,random.choice(monsters)))
		Battle()
	elif x==2:
		print "A curious looking gnome appears from around the corner and offers %s assistence." %name
		try:
			x=int(raw_input("The gnome looks delicious! Should %s eat it?\n\n1.I had gnome for lunch\n2.Nummy nummy!\n>"%name))
		except ValueError:
			print "Invalid input. Try again."
			Yell()
		if x==1:
			raw_input("%s decides to have a gnome allergy and punts the little runt down the grate.>"%name)
			travel2()
			#if x==1:
			#	HallWay()
			#else:
			#	Grate()
		elif x==2:
			x=random.randint(1,11)
			if x<6:
				x=int(raw_input("Gnomercy! %s pounces on the gnome and fests on its chocolatey innerds.\nWell that was a filling meal! %s feels full now and replenished some health!\n%s goes back up the ladder."%(name,name,name)))
				health+=25
				if health >100:
					health=100
				print "%s's health is now %d."%(name,health)
				travel()
				#if x==1:
				#	HallWay()
				#else:
				#	Grate()
			else:
				raw_input("As it turns out, %s is allergic to gnomes! Oops!\n%s takes 30 points of damage!"%(name,name))
				health-=30
				print "%s's health is reduced to %d!\n\n%s walks down the corridor.\n"%(name,health,name)
				if health<=0:
					death()
				HallWay()
	else:
		c=random.randint(1,11)
		raw_input("%s's throat now hurts from screaming and %s takes %d damage.\n(Way to go!)\n" %(name,name,c))
		health-=c
		print "%s's health is reduced to %d"%(name,health)
		if health<=0:
			death()
		raw_input("Care to do something more productive?")
		travel()
		#if x==1:
		#	HallWay()
		#else:
		#	Grate()

#def start():

#name=raw_input("Please enter your name: ")
#	if name=="":
#		print "Seriously, ENTER YOUR NAME!"
#		start()
#start()
def Startup():
	global health,inventory,quest,M,name
	try:
		x=int(raw_input("1.Start New Game\n2.Load Saved Game\n\n>>"))
	except ValueError:
		print "Invalid input. Try again."
		Startup()
	if x==1:
		pass
	elif x==2:
		health,inventory,quest,M,name=Save1.health,Save1.inventory,Save1.quest,Save1.M,Save1.name
		print "Game Loaded"
		travel()
	else:
		print "Invalid input. Try again."
		Startup()
Startup()
name=raw_input("Please enter your name: ")
raw_input("Please enter your age: ")
SSN=raw_input("Please enter your Social Security Number: ")
if SSN>=0:
	raw_input("\nJust kidding! Don't be so gullible!")
print "\n--------------------------------------------------------------------------------------"
print "\n\n\t\t\tO U R   S T O R Y   B E G I N S !"
print '''
	My name is %s. I fell down a hole while doing something stupid but can't
	remember what. When I woke up, I was in a strange smelly labrynth. I need 
	you to help me get out! Guide me through the random events using the prompts 
	and help me stay alive long enough to escape!
 ''' %name
raw_input()
print '''
%s comes to a long corridor and notices a grate in the floor. What should %s do?
(Make your selection by entering the number)
'''% (name,name)
travel()
choice=int(raw_input("\n%s should: "%name))
if choice==1:
	HallWay()
elif choice==2:
	Grate()
else:
	Yell()

raw_input()

	


