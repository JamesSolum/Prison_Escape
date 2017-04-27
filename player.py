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

def borderPoint(loc, border):
	"""
	Border Point

	Generates a list of border points that are closest to the given location
	"""
	distances =[]
	closest =[]
	options = [(loc[0], border), (loc[0], -border), (border, loc[1]), (-border, loc[1]), (border, border), (-border, -border), (border, -border), (-border, border)]

	for point in options:
		dist = distance(loc, point)
		distances.append(dist)
	distances.sort()
	closest.append(distances[0])

	for i in range(1,len(distances)-1):
		if distances[i] == closest[0]:
			closest.append(distances[i])
		else:
			break
	return closest

def closestPerimsToBorder(perim, border):
	allDistances = []
	points = []

	for loc in perim:
		options = [(loc[0], border), (loc[0], -border), (border, loc[1]), (-border, loc[1]), (border, border), (-border, -border), (border, -border), (-border, border)]
		shortestDist = float("inf")
		for op in options:
			dist = distance(op, loc)
			if dist < shortestDist:
				shortestDist = dist
		allDistances.append(shortestDist) # The distance between each perimeter point and its closest border is now stored 
	x = min(allDistances) # minimum value
	index = allDistances.index(x) # index for smallest value
	points.append(perim[index])

	for i in range(index+1,len(allDistances)-1):
		if allDistances[i] == allDistances[index]:
			points.append(perim[i])

	return points

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

	def __init__(self, border, location=(0,0), weapon=False, probability=[1/4, 3/8, 3/8], caught=False):
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
			return loc# Used in Line of Sight # Having an issue with this function

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

	def smartUpdateOld(self, increment=0.1, subtract=0.05):
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

			self.probX[xSign] += abs(x)*(increment+subtract) # here is an issue
			self.probY[ySign] += abs(y)*(increment+subtract) # here is another issue

			self.probX = list(map(lambda x: x-subtract, self.probX))
			self.probY = list(map(lambda x: x-subtract, self.probY))

			x = int(numpy.random.choice(3, 1, p=self.probX)) -1
			y = int(numpy.random.choice(3, 1, p=self.probY)) -1

			self.move((x,y))
		else:
			self.randomStep()

	def closestPerimsToBorder(self):
		perim = self.generatePerimeter()
		border = self.border
		allDistances = []
		points = []

		for loc in perim:
			options = [(loc[0], border), (loc[0], -border), (border, loc[1]), (-border, loc[1]), (border, border), (-border, -border), (border, -border), (-border, border)]
			shortestDist = float("inf")
			for op in options:
				dist = distance(op, loc)
				if dist < shortestDist:
					shortestDist = dist
			allDistances.append(shortestDist) # The distance between each perimeter point and its closest border is now stored 
		x = min(allDistances) # minimum value
		index = allDistances.index(x) # index for smallest value
		points.append(perim[index])

		for i in range(index+1,len(allDistances)):
			if allDistances[i] == allDistances[index]:
				points.append(perim[i])

		return points

	def smartUpdate(self, l=False, p=0.04): # p is (100/5)/border+1
		if not(self.location == (0,0)):
			perimeter = self.generatePerimeter()
			points = self.closestPerimsToBorder()
			
			pointProb = []

			for point in points:
				perimeter.remove(point) # remove point from perimeter
				multiplier = max(abs(point[0]), abs(point[1])) -1 # because at (0,0) there is no probability
				prob = multiplier*p # find probability
				pointProb.append(prob) # add to list

			perimProb = [(1-sum(pointProb))/(len(perimeter))]*len(perimeter)

			perimeter.extend(points)
			perimProb.extend(pointProb)

			if not(l):
				index = int(numpy.random.choice(8, 1, p=perimProb))
				loc = perimeter[index]
				self.location = loc
			else:
				return [perimeter, perimProb]

		else:
			if not(l):
				self.randomStep()
			else:
				return self.generatePerimeter()

	def superBilly(self, guards):
		"""
		Super Billy

		Combines smart Update and Line of Sigth
		"""
		los = self.abstractLineOfSight(guards) #available line of sight locations
		smart = self.smartUpdate(l=True) #available smart locations

		common = []
		probabilities = []

		for index in range(0, len(smart[0])-1): # create a list of all common points
			if smart[0][index] in los:
				common.append(smart[0][index]) # update list of common points
				probabilities.append(smart[1][index]) # update list of probabilities

		if not(common):
			self.lineOfSight(guards)
		else:
			loc = rand.choice(common)
			self.setLocation(loc)

	def abstractLineOfSight(self, guards):
		"""
		Abstract Line of Sight
		takes a list of guards

		Abstraction for line of Sight
			paramters: all players
			returns: list of possible movements

		"""

		perim = self.generatePerimeter()

		for g in guards:
			spots = g.generatePerimeter()
			for spot in spots:
				if spot in perim:
					perim.remove(spot)

		return perim

	def lineOfSight(self, guards):
		"""
    	Line of Sight
    	takes a list of guards

    	Moves Billy by a factor of 1 according to Line of Sight Algorithm.
    	If unable to move Billy the CAUGHT parameter is changed to True
		"""
		options = self.abstractLineOfSight(guards)
		loc = self.caughtCheck(options)
		self.setLocation(loc)
		"""
	def lineOfSight_Sprint(self, CAUGHT, guard, rook, bishop, knight, teleporter):
		"""
		"""
		Line of Sight Sprint

		Moves Billy by a factor of 2 according to Line of Sight Algorithm.
		Again, if unable to move Billy the CAUGHT parameter is changed to True
		"""
		"""
		options = self.abstractLineOfSight(2, guard, rook, bishop, knight, teleporter)
		self.caughtCheck(CAUGHT, options)# May need to fix this.  Sprint is two movements, not jumping two squares. 
		"""

	def weaponCheck(self, guard, p=0.1):
		"""
		Weapon

		Calculates whether Billy survives given a certain
		probability of survival
		"""
		if self.weapon:
			options = [True, False]
			for g in guard:
				if self.location == g.location:
					x = numpy.random.choice([0,1], 1, p=[p, 1-p]) # 10% chance he is caught
					if options[int(x)]:
						self.location = (0,0) # Reset location
						self.weapon = False
						self.Caught = False
					else:
						self.Caught=True

class guard(player):

	def __init__(self, border, location, center=(0,0)):
		"""
		Generic Guard Class

		For building other Guards

		Requires a border parameter
		"""
		super().__init__(border, location)
		self.center = center

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
			if abs(self.locX()) > border or abs(self.locY()) > border:
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

	def lineOfSightAbstract(self, billy, perim):
		options = []

		loc = self.location
		
		billyList = billy.generatePerimeter()

		for target in billyList:
			if target in perim:
				options.append(target)

		if target in perim:
			self.setLocation(rand.choice(options))  
		else:
			self.randomStep()

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
			closeDist = float("inf")
			for movement in self.squareGuard_Option_Calculator():
				dist = distance(movement, billLoc)
				if dist < closeDist:
					closest = movement
					closeDist = distance(closest, billLoc)
			self.move(closest)
		else:
			self.randomStep()

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
		self.index = (self.index + rand.choice((-1,1))) % len(self.trail) # Update trail index to point to next or previous location point
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
		trail = self.trail
		e1 = None # Exception 1
		e2 = None # Exception 2

		# Border Check
		if not(self.border == float("inf")): # If the border is infinity, no point in looping through
			for point in trail:
				if abs(point[0]) > self.border or abs(point[1]) > self.border:
					borderPoints.append(point)
				if not not borderPoints: # Returns True if there is something in the list
					Exception("Points:", borderPoints, "are not within defined border!") # Prints all the problem points

		# Unit Check
		for index in range(0,len(trail) -1):
			if abs(trail[index][0] - trail[index + 1][0]) > 1 or abs(trail[index][1] - trail[index+1][1]) > 1:
				badPoints.append([trail[index], trail[index +1]])
			if not not badPoints: # Returns True if there is something in the list
				raise Exception("Points", badPoints, "are not one unit away from each other!") # Prints all the problem points
		
		return True # If everything is good return True

	def lineOfSight(self, billy):
		"""
		Line of Sight

		If billy is nearby the guard will tend toward Billy
		"""
		perimeter = self.generatePerimeter()
		target = billy.location
		trailLength = len(self.trail)

		if target in perimeter:
			loc1 = self.trail[(self.index+1)%trailLength]
			loc2 = self.trail[(self.index -1)%trailLength]

			dist1 = distance(loc1, target)
			dist2 = distance(loc2, target)

			if dist1 > dist2:
				self.setLocation(self.trail[(self.index -1)%trailLength])
			else:
				self.setLocation(self.trail[(self.index + 1)%trailLength])
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

	def lineOfSightOld(self, billy, amount=0.1):
		"""
		Line of Sight 

			amount = how much we adjust probabilities. Default is 0.1 (10%)

		Checks if Billy is close by.  If so increases the probability by %10 to go towards billy.
		"""
		target = billy.location
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
			x = int(numpy.random.choice(options, 1, p=self.probX))
			y = int(numpy.random.choice(options, 1, p=self.probY))

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

	def lineOfSight(self, billy):
		"""
		Line of Sight


		If Billy is nearby then randomly choose location near or on Billy
		"""
		loc = self.location
		perim = [(loc[0]+1,loc[1]+1),(loc[0]+1,loc[1]-1),(loc[0]-1,loc[1]+1),(loc[0]+1,loc[1]+1)]
		self.lineOfSightAbstract(billy, perim)

class rook(guard):
	"""
	Rook

	Guard that moves up, down, left, or right
	"""
	def __init__(self, border, probability=[1/4,1/4,1/4,1/4], location=float("inf")):
		"""
		Initializes Rook

		Just uses general guard class.  
		"""
		super().__init__(border, location)
		self.probability = probability #up, down, left, right

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
		loc = self.location
		perim = [(loc[0]+1,loc[1]+1),(loc[0]+1,loc[1]-1),(loc[0]-1,loc[1]+1),(loc[0]+1, loc[1]+1)]
		self.lineOfSightAbstract(billy, perim)

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
		longL = rand.choice((1,-1)) # positive or negative for long part of "L"
		shortL = rand.choice((1,-1)) # postive or negative for short part of the "L"

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
	def __init__(self, border, center=(0,0), location=float("inf")):
		"""
		Initialize Teleporter

		General guard class
		"""
		super().__init__(border, location)
		self.center = center

	def randomStep(self):
		"""
		Random Step

		Randomly chooses a point inside the board and sets the 
		location of the guard to that point
		"""
		border = self.border
		centerX = self.center[0]
		centerY = self.center[1]
		x = rand.randrange(centerX - border, centerX + border+1)
		y = rand.randrange(centerY-border, centerY + border+1)
		self.setLocation((x,y))

	def alarmCheck(self, alarm):
		if alarm.triggered:
			self.border = alarm.border
			self.center = alarm.location

	def quartileAlarmMove(self, alarm1, alarm2, alarm3, alarm4):
		self.alarmCheck(alarm1)
		self.alarmCheck(alarm2)
		self.alarmCheck(alarm3)
		self.alarmCheck(alarm4)

		self.randomStep()

class alarm(player):
	def __init__(self,border, location, triggered=False):
		super().__init__(border,location)
		self.triggered = triggered

	def trigger():
		self.triggered = True
		return self.triggered

	def reset():
		self.triggered = False

class centerAlarm(alarm):
	def __init__(self, border, location=(0,0), triggered=False):
		super().__init__(border, location, triggered)

	def guardCheck(self, guard): # list of guards
		for g in guard:
			if abs(g.location[0]) <= self.border and abs(g.location[1]) <= self.border:
				self.triggered = True
				return self.triggered

class quartileAlarm(alarm):
	def __init__(self, location, border=0, triggered=False):
		super().__init__(border, location, triggered)

	def billyCheck(self, billy):
		if billy.location == self.location:
			self.triggered = True
			return self.triggered

