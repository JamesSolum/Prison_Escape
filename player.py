#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Player Class
-------------

Author: James Solum

This class will be the foundation for creating
our different players in the Prison Escape Simulation.

The player class will be the blueprints for:
		Billy
		-----
			* Billy

			Abilities
			* Weapon
			* Sprint
			* Smart
			* Line of Sight
		Guard
		-----
			* squareGuard
			* genericGuard
			* Bishop
			* Rook
			* Knight
			* Teleporter

			Abilities
			* Alarm, at (0,0)
			* Weapon
			* Line of Sight
			* Quartile Alarm
"""

import random as rand # For random movements
import numpy # For weighting choices with probabilities
import itertools
import math # for square root in distance function

#### Helper Functions ####
def addTuple(t1, t2):
		x = t1[0] + t2[0]
		y = t1[1] + t2[1]
		return (x,y)

def distance(t1, t2):
	x1 = t1[0]
	y1 = t1[1]
	x2 = t2[0]
	y2 = t2[1]

	return math.sqrt( (x2 - x1)**2 + (y2 - y1)**2)

#### Class ####

class player(object):
	"""
	Generic Player Super Class

	Initializes location on the game board and 
	provides helpful location update methods
	"""
	def __init__(self, border, location):
		"""
		Initialized player with:
			Location   tuple
		"""
		self.border = border
		self.OutOfBounds = False
		self.location = location
		if self.location == float("inf"):
			self.setRandomLocation(self.border)

	def locX(self):
		# returns x value of location
		return self.location[0]

	def locY(self):
		# returns y value of a location
		return self.location[1]

	def setLocation(self, loc):
		"""
		resets location to loc:
			loc   tuple
		"""
		self.location = loc

	def move(self, loc):
		"""
		Updates location relative to current location
			loc  tuple
		Moves locX 
		"""
		point = addTuple(loc, self.location)
		border = self.border

		if abs(point[0]) > border or abs(point[1]) > border:
			self.OutOfBounds = True

		self.location = point

	def moveX(self, x):
		"""
		Moves player left or right
			x   int
		"""
		self.move((x,0))

	def moveY(self, y):
		"""
		Moves player up or down
			y  int
		"""
		self.move((0,y))

	def setRandomLocation(self, border):
		"""
		Random Location

		Give our player a random location other than (0,0)
		"""
		loc = (rand.randint(-border, border), rand.randint(-border, border))
		while(loc == (0,0)):
			loc = (rand.randint(-border, border), rand.randint(-border, border))
		self.location = loc

	def generatePerimeter(self, perim=1):
		"""
		Generate Perimeter

		Generate a list of points that is around the location of one of our players
		"""
		location = self.location
		x = location[0]
		y = location[1]
		Xlist = [x+perim, x, x-perim]
		Ylist = [y+perim, y, y-perim]

		perimeter = [(a,b) for a in Xlist for b in Ylist]
		perimeter.remove(location)
		return perimeter
	
class billy(player):

	def __init__(self, border, location=(0,0), weapon=False, probability=[1/3, 1/3, 1/3], caught=False):
		"""
		Billy Class

		Implements random walk algorithms, smart Billy, and Line of Sight

		"""

		super().__init__(border, location)
		self.CAUGHT = caught
		self.weapon = weapon
		self.probX = probability
		self.probY = probability

	def caughtCheck(self, options):
		"""
		Caught Check

		Utilized in Line of Sight, and line of Sight Sprint

		If not Caught, location is updated randomly.  If Caught, CAUGHT boolean is updated to True
		"""
		if not options:
			self.CAUGHT = True
			return self.CAUGHT
		else:
			loc = rand.choice(options)
			self.setLocation(loc)# Used in Line of Sight # Having an issue with this function
			return self.CAUGHT

	def randomMove(self, maxStep):
		"""
		Random Step

		Randomly move Billy by maximum step at a time.  
			maxStep   int
		Cannot move (0,0)
		"""
		x = rand.choice((-maxStep,0,maxStep))
		if x == 0:
			y = rand.choice((-maxStep,maxStep))
		else:
			y = rand.randint(-maxStep, maxStep)
		self.move((x,y))

	def randomStep(self):
		"""
		Random Step

		Randomly move Billy one step at a time.  
		Cannot move (0,0)
		"""
		self.randomMove(1)

	def randomSprint(self):
		"""
		Random Spring

		Randomly move Billy two steps at a time
		Cannot move (0,0)
		"""
		self.randomStep()
		self.randomStep()

	def smartUpdate(self, increment=0.1, subtract=0.05):
		"""
		Smart Update

		Every step from the center he is 10% more likely to move towards the closest border
		"""
		x = self.locX()
		y = self.locY()

		if not((x,y) == (0,0)):
			if not(x == 0):
				xSign = int(x/abs(x))
			else:
				xSign = 0
			if not(y==0):
				ySign = int(y/abs(y))
			else:
				ySign = 0

			self.probX[xSign] += abs(x)*(increment+subtract)
			self.probY[ySign] += abs(y)*(increment+subtract)

			self.probX = list(map(lambda x: x -subtract, self.probX))
			self.probY = list(map(lambda x: x-subtract, self.probY))

			x = int(numpy.random.choice(3, 1, self.probX)) -1
			y = int(numpy.random.choice(3, 1, self.probY)) -1

			self.move((x,y))
		else:
			self.randomStep()

	# Need to check all code below this :)

	# Need to write this
	def superBilly(self):
		"""
		Super Billy

		Combines all of Billy's abilities to update his position
		"""

		return 1 

	def abstractLineOfSight(self, walk, guard, rook, bishop, knight, teleporter): # This is more complicated than I want it to be.  Maybe use the new Generate Perimeter Function.
		"""
		Abstract Line of Sight

		Abstraction for line of Sight
			paramters: all players
			returns: list of possible movements

		"""
		loc = self.location
		x = loc[0]
		y = loc[1]
		checks = [(x, y - walk), (x, y + walk), (x + walk, y -walk), (x + walk, y), (x + walk, y +walk), (x-walk, y-walk), (x-walk, y), (x-walk, y+walk)]
		positions = [guard.location, rook.location, rook.location, bishop.location, knight.location, teleporter.location]
		guards = []

		for pos in positions:
			for check in checks:
				if pos == check:
					guards.append(pos)

		noGo = []
		for position in guards:
			if x == position[0]:
				noGo.append((position[0]+1 , position[1]))
				noGo.append((position[0]-1 , position[1]))
			if y == position [1]:
				noGo.append(position) 
				noGo.append((position[0], position[1] + 1))
				noGo.append((position[0], position[1]-1))

        # Fix options
		for fail in noGo:
			if fail in checks:
				checks.remove(fail)

	def lineOfSight(self, guard, rook, bishop, knight, teleporter):
		"""
    	Line of Sight

    	Moves Billy by a factor of 1 according to Line of Sight Algorithm.
    	If unable to move Billy the CAUGHT parameter is changed to True
		"""
		options = self.abstractLineOfSight(1, guard, rook, bishop, knight, teleporter)
		self.caughtCheck(options)

	def lineOfSight_Sprint(self, CAUGHT, guard, rook, bishop, knight, teleporter):
		"""
		Line of Sight Sprint

		Moves Billy by a factor of 2 according to Line of Sight Algorithm.
		Again, if unable to move Billy the CAUGHT parameter is changed to True
		"""
		options = self.abstractLineOfSight(2, guard, rook, bishop, knight, teleporter)
		self.caughtCheck(CAUGHT, options)# May need to fix this.  Sprint is two movements, not jumping two squares. 

	def caughtCheck(self, probability=0.1):
		"""
		Survival Calculator (weapon)

		Calculates whether Billy survives given 
		a certain probability of survival
			True     survived
			False    caught

		probability parameter must be less than or equal to 1

		This is to be used with Billy's Weapon implementation
		"""
		options = [False, True]
		x = numpy.random.choice(2, 1, [probability, 1-probability]) # 2 is length of Options, and 1 is the number of outputs we want.  
		result = options[x] # We use the output of our random function as an index for choosing True or False
		self.CAUGHT = result
		return result

class guard(player):

	def __init__(self, border, location, center=(0,0), centerAlarm=False, LB_Alarm=False, RB_Alarm=False, TL_Alarm=False, TR_Alarm=False):
		"""
		Generic Guard Class

		For building other Guards

		Requires a border parameter
		"""
		super().__init__(border, location)
		self.center = center
		self.centerAlarm= centerAlarm
		self.LB_Alarm = LB_Alarm
		self.RB_Alarm = RB_Alarm
		self.TL_Alarm = TL_Alarm
		self.TR_Alarm = TR_Alarm

	def outsideBorder(self, points=None):
		"""
		Outside Border
		
		Checks 1 of 2 things

			1. If current location is outside of border
				Returns True if outside of border or False if within the border

			2. If any points are outside of border
				returns list of all points inside or on Border
		"""
		border = self.border
		if not points:
			if abs(self.locX) > border or abs(self.locY) > border:
				return True # If outside of Border
			else:
				return False # If inside of border
		else:
			goodPoints = []
			for point in points:
				if not(abs(point[0]) > border or abs(point[1]) > border):
					goodPoints.append(point)
			return goodPoints

	def randomMove_from_movements(self, points):
		"""
		Random Move from Movements

		Randomly moves player given a set of possible "movements" after checking and removing any "movements" that are outside the border
			Note! This is not a list of locations, but a list of directions desribed as tuples

		random Move will check if it possible location is > border then updates location
		"""
		checks = list(map(lambda x: addTuple(x, self.location), points)) # convert those movements into locations
		points = self.outsideBorder(checks) # produce a new list of locations that are not outside the border
		self.setLocation(rand.choice(points)) # randomly set location of player to one of those locations

	def alarmCheck(self):
		"""
		Alarm Check

		I still need to figure out what exactly this does, and what to do with the quartile alarms. 

		"""
		if self.location == (0,0):
			self.centerAlarm = True

class squareGuard(guard):
	"""
	Square Guard

	Guard that traverses a square perimeter around the center (0,0)
	"""
	def __init__(self, Sqborder):
		"""
		Initialize Perimeter Guard

		Patrols a square perimeter
		"""
		# Set location on a corner of the perimeter
		x = rand.choice((-Sqborder, Sqborder))
		y = rand.choice((-Sqborder, Sqborder))
		loc = (x,y)
		border = Sqborder + 1 # Just make the border of the board bigger than our perimeter. 
		super().__init__(border, loc)

		self.perimeter = Sqborder
		self.probability = [1/2, 1/2] # left or right

	def squareGuard_Option_Calculator(self):
		options = (-1,1)
		ops = len(options) 
		bDist = self.perimeter
          
        # Where corners should be
		cornerX1 = bDist # right
		cornerX2 = -bDist # left
		cornerY1 = bDist # top
		cornerY2 = -bDist # bottom
        
        # Check if it's in between the corners
		x = rand.randrange(0,2)
		if (self.location == (cornerX1, cornerY1)): # top right corner
			movOps = ((-1,0), (0,-1))
			return movOps
		elif (self.location == (cornerX1, cornerY2)): # bottom right corner
			movOps = ((-1, 0), (0,1))
			return movOps
		elif (self.location == (cornerX2, cornerY1)): # top left corner
			movOps = ((1,0), (0,-1))
			return movOps
		elif (self.location == (cornerX2, cornerY2)): # bottom left corner
			movOps = ((1,0),(0,1))
			return movOps
		elif self.locX() == cornerX1 or self.locX() == cornerX2: # If the location is on the far left or right
			movOps = ((0,1),(0,-1))
			return movOps
		elif self.locY() == cornerY1 or self.locY() == cornerY2: # If the location is on the top or bottom
			movOps = ((1,0),(-1,0))
			return movOps
		else:
			raise Exception('ERROR: Guard Random Border Step') # This Needs some work

	def randomStep(self):
		"""
		Random Step

		calculates possible options for movements, chooses one randomly, then updates. 
		"""
		options = self.squareGuard_Option_Calculator()
		move = rand.choice(options)
		self.move(move)

	def lineOfSight(self, billy):
		"""
		Line of Sight

		Moves Square guard along path but if billy is nearby, it tends the guard toward Billy
		"""
		perimeter = self.generatePerimeter()
		billLoc = billy.location
		
		if billLoc in perimeter:
			closest = float("inf")
			for movement in self.squareGuard_Option_Calculator():
				dist = distance(movement, billLoc)
				if dist < closest:
					smallest = dist
			self.move(closest)
		else:
			self.randomStep()

	"""
	Old Random Step
	def randomStep(self): # This is more complicated than I want it to be
		options = (-1,1)
		ops = len(options) 
		bDist = self.perimeter
          
        # Where corners should be
		cornerX1 = bDist # right
		cornerX2 = bDist # left
		cornerY1 = bDist # top
		cornerY2 = bDist # bottom
        
        # Check if it's in between the corners
		x = rand.randrange(0,2)
		if (self.location == (cornerX1, cornerY1)): # top right corner
			movOps = ((-1,0), (0,-1))
			self.move(movOps[x])
		elif (self.location == (cornerX1, cornerY2)): # bottom right corner
			movOps = ((-1, 0), (0,1))
			self.move(movOps[x])
		elif (self.location == (cornerX2, cornerY1)): # top left corner
			movOps = ((1,0), (0,-1))
			self.move(movOps[x])
		elif (self.location == (cornerX2, cornerY2)): # bottom left corner
			movOps = ((1,0),(0,1))
			self.move(movOps[x])
		elif self.locX() == cornerX1 or self.locX() == cornerX2: # If the location is on the far left or right
			self.moveY(options[rand.randrange(0,ops)])
		elif self.locY() == cornerY1 or self.locY() == cornerY2: # If the location is on the top or bottom
			self.moveX(options[rand.randrange(0, ops)])
		else:
			raise Exception('ERROR: Guard Random Border Step') # This Needs some work
	"""

class pathGuard(guard):
	"""
	Path Guard

	Guard that traverses some path, represented as a list of points called Trail
	"""
	def __init__(self, trail, border=float("inf")):
		"""
		Initializes Generic Guard with Trail

		Trail is a list of points
		Border default is infinity because in general the trail will be set manually
		thereby removing the need for a border check
		"""
		loc = rand.choice(trail)
		super().__init__(border, loc)
		self.trail = trail
		self.index = trail.index(loc) # pointer to spot on trail
		self.probability = [1/2, 1/2] # left or right

	def randomStep(self):
		"""
		Random Step

		Randomly traverse trail List one step at a time
		"""
		self.index = (self.index + rand.choice(-1,1)) % len(self.trail) # Update trail index to point to next or previous location point
		self.setLocation(self.trail[self.index]) # Update location to new list location

	def pathCheck(self):
		"""
		Path Check

		Checks if:
			* any trail points are outside the border
			* or if any trail points are more than 1 unit away from each other
		Returns True if all Good
		Raises Exception if not Good
		"""
		borderPoints = []
		badPoints = []
		e1 = None # Exception 1
		e2 = None # Exception 2

		# Border Check
		if not(self.border == float("inf")): # If the border is infinity, no point in looping through
			for point in trail:
				if abs(point[0]) > self.border or abs(point[1]) > self.border:
					borderPoints.append(point)
				if not not borderPoints: # Returns True if there is something in the list
					e1 = Exception("Points:", borderPoints, "are not within defined border!") # Prints all the problem points

		# Unit Check
		for index in len(trail) -1 :
			if abs(trail[index][0] - trail[index + 1][0]) > 1 or abs(trail[index][1] - trail[index][1]) > 1:
				badPoints.append([trail(index), trail[index +1]])
			if not not badPoints: # Returns True if there is something in the list
				e2 = Exception("Points", badPoints, "are not one unit away from each other!") # Prints all the problem points
		
		if not e1 and not e2: # Checks if there were exceptions
			return True # If not function returns True
		else: 
			raise e1 
			raise e2
			return False # If so, raises exceptions and returns False

	def lineOfSight(self, billy):
		"""
		Line of Sight

		If billy is nearby the guard will tend toward Billy
		"""
		perimeter = self.generatePerimeter()
		target = billy.location

		if target in perimeter:
			loc1 = self.path[self.index+1]
			loc2 = self.path[self.index -1]

			dist1 = distance(loc1, target)
			dist2 = distance(loc2, target)

			if dist1 > dist2:
				self.setLocation(self.path[self.index -1])
			else:
				self.setLocation(self.path[self.index + 1])
		else:
			self.randomStep()

class bishop(guard):
	"""
	Bishop

	Guard that moves in diagonal movements
	"""
	def __init__(self, border, location=float("inf")):
		"""
		Initializes Bishop

		Default is some random location.
		"""

		super().__init__(border, location)
		self.probX = [1/2, 1/2] # left or right
		self.probY = [1/2, 1/2] # up or down

	def randomStep(self, stepSize=1):
		"""
		Random Step

		Randomly step in a diagonal Direction within the border
		Step Size is default 1
		"""
		points = list(itertools.product((stepSize, -stepSize), (stepSize, -stepSize))) # Produces a list of all possible movements
		self.randomMove_from_movements(points)

	def lineOfSight(self, Billy, amount=0.1):
		"""
		Line of Sight 

			amount = how much we adjust probabilities. Default is 0.1 (10%)

		Checks if Billy is close by.  If so increases the probability by %10 to go towards billy.
		"""
		target = billy.location()
		perimeter = self.generatePerimeter()

		# check if target is in perimeter
		if target in perimeter:
			x = target[0] - self.locX()
			y = target[1] - self.locY()

			# Adjust probabilities
			self.adjustProbabilities(x, self.probX, amount)
			self.adjustProbabilities(y, self.probY, amount)

			# Calculate new random location with new probabilties
			options = [-1,1]
			x = int(numpy.random.choice(options, 1, self.probX))
			y = int(numpy.random.choice(options, 1, self.probY))

			self.setLocation((x,y)) # update locations

		else: # If target is not in perimeter just do a random step
			self.randomStep()

	def adjustProbabilities(self, x, probability, amount):
			"""
			Adjust Probabilities

				x: difference between locations
				probability: probability for that movement
				amount: amount to change

				if the change is 1 or -1 change probabilities, else no change.
			"""
			if x == 1:
				probability[1] += amount
				probability[0] -= amount
			elif x == -1:
				probability[1] -= amount
				probability[0] += amount

class rook(guard):
	"""
	Rook

	Guard that moves up, down, left, or right
	"""
	def __init__(self, border, location=float("inf")):
		"""
		Initializes Rook

		Just uses general guard class.  
		"""
		super().__init__(border, location)
		self.probability = [1/4, 1/4, 1/4, 1/4] #up, down, left, right

	def randomStep(self, stepSize=1):
		"""
		Random Step

		Randomly step left, right, up or down, within the border
		Step size is default 1
		"""
		points = [(stepSize,0), (0,stepSize), (-stepSize,0), (0,-stepSize)] # all possible paths
		self.randomMove_from_movements(points)

	def lineOfSight(self, billy):
		"""
		Line of Sight

		Yeah...it's the same as the other line of sight functions.  I probably could have made an abstraction for this....
		"""
		perimeter = self.generatePerimeter()
		target = billy.location
		movements = [(stepSize,0), (0,stepSize), (-stepSize,0), (0,-stepSize)]

		if target in perimeter:
			shortest = float("inf")
			for move in movements:
				dist = distance(target, move)
				if dist < shortest:
					shortest = dist
			self.move(shortest)
		else:
			self.randomStep()

class knight(guard):
	"""
	Knight

	Guard that moves in an "L" pattern
	"""
	def __init__(self, border, location=float("inf")):
		"""
		Initializes Knight

		Just uses general guard class.
		"""
		super().__init__(border, location)
		self.probability = [1/4, 1/4, 1/4, 1/4]  # Top left, top right, bottom right, bottom left.

	def randomStep(self):
		vertOrHoriz = rand.choice((1,0)) # Up/down or left/right
		longL = rand.choice(1,-1) # positive or negative for long part of "L"
		shortL = rand.choice(1,-1) # postive or negative for short part of the "L"

		if vertOrHoriz == 0:
			self.moveX(longL)
			self.moveX(longL)
			self.moveX(longL)
			self.moveY(shortL)
		else:
			self.moveY(longL)
			self.moveY(longL)
			self.moveY(longL)
			self.moveX(shortL)

class teleporter(guard):
	"""
	Teleporter

	Guard that randomly jumps within the board
	"""
	def __init__(self, border, location=float("inf")):
		"""
		Initialize Teleporter

		General guard class
		"""
		super().__init__(border, location)

	def randomStep(self):
		"""
		Random Step

		Randomly chooses a point inside the board and sets the 
		location of the guard to that point
		"""
		border = self.border
		x = rand.randrange(-border, border+1)
		y = rand.randrange(-border, border+1)
		self.setLocation((x,y))
