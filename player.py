#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Player Class
-------------

Author: James Solum

This class will be the basis for basic methods for creating
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

class player(object):
	"""
	Generic Player Super Class

	Initializes location on the game board and 
	provides helpful location update methods
	"""
	def __init__(self, loc, border):
		"""
		Initialized player with:
			Location   tuple
		"""
		self.location = loc
		self.OutOfBounds = False

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
		x = loc[0] + self.location[0]
		y = loc[1] + self.location[1]

		# Check if location is out of bounds
		if abs(x) > border or abs(y) > border:
			self.OutOfBounds = True

		self.location = (x,y)

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

	def setRandomLocation(self):
		"""
		Random Location

		Give our player a random location other than (0,0)
		"""
		loc = (rand.randint(-self.border, self.border) - border, rand.randint(-self.border, self.border))
        while(loc == (0,0)):
            loc = (rand.randint(-self.border, self.border) - border, rand.randint(-self.border, self.border))
        self.location = loc

class billy(player):

	def __init__(self, loc=(0,0), weapon=False, probability=[1/3, 1/3, 1/3]):
		"""
		Billy Class

		Implements random walk algorithms, smart Billy, and Line of Sight
		"""
		super().__init__(loc)
		self.weapon = weapon
		self.probX = probability
		self.probY = probability

	def caughtCheck(CAUGHT, options):
		"""
		Caught Check

		Utilized in Line of Sight, and line of Sight Sprint

		If not Caught, location is updated randomly.  If Caught, CAUGHT boolean is updated to True
		"""
		if not options:
            CAUGHT = True
        else:
            loc = rand.choice(options)
            self.location(loc)# Used in Line of Sight

	def randomMove(self, maxStep):
		"""
		Random Step

		Randomly move Billy by maximum step at a time.  
			maxStep   int
		Cannot move (0,0)
		"""
		x = rand.choice(-maxStep,0,maxStep)
		if x == 0:
			y = rand.choice(-maxStep,maxStep)
		elif:
			y = rand.randint(-maxStep,,maxStep)
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
		self.randomMove(2)

	def smartUpdate(self):
		"""
		Smart Update

		Every step from the center he is 10% more likely to move towards the closest border
		"""

		# Write here

	def superBilly(self):
		"""
		Super Billy

		Combines all of Billy's abilities to update his position
		"""

		# Write here

	def abstractLineOfSight(self, walk, guard, rook, bishop, knight, teleporter): # This is more complicated than I want it to be
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

    def lineOfSight(self, CAUGHT, guard, rook, bishop, knight, teleporter):
    	"""
    	Line of Sight

    	Moves Billy by a factor of 1 according to Line of Sight Algorithm.
    	If unable to move Billy the CAUGHT parameter is changed to True
    	"""
    	options = self.abstractLineOfSight(1, guard, rook, bishop, knight, teleporter)
    	caughtCheck(CAUGHT, options)

    def lineOfSight_Sprint(self, CAUGHT, guard, rook, bishop, knight, teleporter):
    	"""
		Line of Sight Sprint

		Moves Billy by a factor of 2 according to Line of Sight Algorithm.
		Again, if unable to move Billy the CAUGHT parameter is changed to True
    	"""
    	options = self.abstractLineOfSight(2, guard, rook, bishop, knight, teleporter)
    	caughtCheck(CAUGHT, options)

	def survived(self, probability):
		"""
		Survival Calculator (weapon)

		Calculates whether Billy survives given 
		a certain probability of survival
			True     survived
			False    caught

		probability parameter must be less than or equal to 1

		This is to be used with Billy's Weapon implementation
		"""
		options = [True, False]
		x = numpy.random.choice(2, 1, [probability, 1-probability]) # 2 is length of Options, and 1 is the number of outputs we want.  
		return options[x] # We use the output of our random function as an index for choosing True or False

class squareGuard(player):
	"""
	Square Guard

	Guard that traverses a square perimeter around the center (0,0)
	"""
	def __init__(self, border):
		"""
		Initialize Perimeter Guard

		Patrols a square perimeter
		"""
		# Set location on the perimeter
		x = random.choice(-border, border)
		y = random.choice(-border, border)
		loc = (x,y)

		super().__init__(loc)
		self.border = border

	def guardBorderStep(self): # This is more complicated than I want it to be
		options = (-1,1)
        ops = len(options) 
        bDist = self.borderdist
        center = self.center
          
        # Where corners should be
        cornerX1 = center[0] + bDist # right
        cornerX2 = center[0] - bDist # left
        cornerY1 = center[1] + bDist # top
        cornerY2 = center[1] - bDist # bottom
        
        # Check if it's in between the corners
        x = randrange(0,2)
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
            self.moveY(options[randrange(0,ops)])
        elif self.locY() == cornerY1 or self.locY() == cornerY2: # If the location is not on the top or bottom
            self.moveX(options[randrange(0, ops)])
        else:
            raise Exception('ERROR: Guard Random Border Step') # This Needs some work

class genericGuard(player):
	"""
	Generic Guard

	Guard that traverses some path, represented as a list of points
	"""
	def __init__(self, trail):
		"""
		Initializes Generic Guard with Trail

		Trail is a list of points
		"""
		loc = rand.choice(trail)
		super().__init__(loc)
		self.trail = trail
		self.index = trail.index(loc)

	def randomStep(self):
		"""
		Random Step

		Randomly traverse trail List one step at a time
		"""
		self.index = (self.index + rand.choice(-1,1)) % len(self.trail) # Update trail index to point to next or previous location point
		self.setLocation(self.trail[self.index]) # Update location to new list location

class bishop(player):

	def __init__(self, loc, border):




























