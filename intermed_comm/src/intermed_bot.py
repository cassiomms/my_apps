# You AI for CTF must inherit from the base Commander class.  See how this is
# implemented by looking at the commander.py in the ./api/ folder.
from api import Commander

# The commander can send 'Commands' to individual bots.  These are listed and
# documented in commands.py from the ./api/ folder also.
from api import commands

# The maps for CTF are layed out along the X and Z axis in space, but can be
# effectively be considered 2D.
from api import Vector2

# To check if a object if from a specific type:
import types

# Used for sin, cos, and PI=3.14159...
import math

class IntermedCommander(Commander):
	"""
	Rename and modify this class to create your own commander and add mycmd.Placeholder
	to the execution command you use to run the competition.
	"""
	
	def findSpots(self):
		"""
		This method returns possible cover positions on the map based on obstacle positions
		
		@return Cover position all over the map		
		
		TODO
		- Better algorithm to add cover positions?
		"""
		
		positions = {}
		positions['cover'] = set()
		#Cover is based on the team flag position
		
		# Iterate over the map, looking for places for cover
		for x in range(0, len(self.level.blockHeights)):
			for y in range(0, len(self.level.blockHeights[x])):
				if self.level.blockHeights[x][y] > 2: # Maybe its best to be > 0 or 1 ?
					
					#We are in an obstacle, based on our team flag spawn position, find the cover spot
					
					# Get an vector pointing to our flag
					dirVector = (self.game.team.flagSpawnLocation - Vector2(x, y)).normalized()
					#self.log.debug(dirVector)
					
					#Try to find a spot to cover near the obstacle location, going to the flag
					for mult in range(1, 6):
						if self.level.blockHeights[int(x+mult*dirVector.x)][int(y+mult*dirVector.y)] == 0:
							positions['cover'].add(Vector2(int(x+mult*dirVector.x), int(y+mult*dirVector.y)))
							break
					
		return positions
	
	
	def closestCover(self, bot_position):
		"""
		This method returns the closest cover position to a bot
		
		@param bot_position The bot position
		
		@return Closest cover position to this bot
		"""
		
		
		distances = [(bot_position.distance(cover), cover) for cover in self.positions['cover']]
		distances.sort()
		#self.log.debug(distances)
		
		return distances[0][1]
	
	def setupCassio(self):
		
		#debugging map information
		#self.log.debug(LevelHelper(self.level))
		self.positions = self.findSpots()
		#self.log.debug(self.positions)
	
	def testCassio(self):
		
		"""
		TODO
		
		- Better facing directions than random ones :P
		
		"""
		
		for bot in self.game.bots_available:
			
			if len(self.positions['cover']) > 0:
				
				if (bot.position.distance(self.level.findNearestFreePosition(self.closestCover(bot.position)))) > 0.5:
					self.issue(commands.Charge, bot, self.level.findNearestFreePosition(self.closestCover(bot.position)), description='Going to defend %s %s' % (self.closestCover(bot.position).x, self.closestCover(bot.position).y))
				else:
					self.issue(commands.Defend, bot, description = 'Defending %s %s' % (bot.position.x, bot.position.y), facingDirection = [(self.level.findRandomFreePositionInBox(self.level.area), 0.5) for __i in range(0, 30)])		
	

	def closestFriendToFlag(self, enemy=True):
		"""This function returns the closest friend bot to a flag
		@param enemy - if it is true enemy flag is considered. Friend flag if False
		@return - The closest bot to the considered flag.		
		"""

		# Enemy flag position
		flagPosition = self.game.enemyTeam.flagSpawnLocation
	
		# If enemy==True, we must consider our flag
		if not enemy:
			flagPosition = self.game.team.flagSpawnLocation			

		# Candidates for bot closest to the considered flag and for minimun squared distance of the flag
		closestBot = self.game.bots_alive[0]
		minDist = flagPosition.squaredDistance(closestBot.position)

		# Loop through all the bots that are alive:
		for bot in self.game.bots_alive:

			candidateDist = bot.position.squaredDistance(flagPosition)
			# Update to better candidates if needed:
			if candidateDist < minDist:
				minDist = candidateDist
				closestBot = bot

		# Return the bot closest to the considered flag
		return closestBot
			

	def surroundPosition(self, bots, positionToDefend, radius, typeOfMovement = commands.Attack):
		""" This method will issue the command to surround a particular position to a bot or a group of bots.
		@param bots: a list containing the bots to surround the position. May be only one bot (not a list).
		@param positionToDefend: the position to be surrounded.
		@param radius: distance from position that the bots will to be. 
		@param typeOfMovement: Attack, Move or Charge to positionToDefend
		"""
		
		# This will make it easier to send only one bot to defend the position:
		if not isinstance(bots, (types.ListType, types.TupleType)):
			bots = [bots]
	
		# Generating positions for the bots: 
		positions = []
		for pos in range(len(bots)):
			# Using the parametric equation of a circunference with center in positionToDefend:
			x = radius * math.cos(2*math.pi*pos/len(bots)) + positionToDefend.x
			y = radius * math.sin(2*math.pi*pos/len(bots)) + positionToDefend.y

			# Finding the nearest free position in the map, if the position cannot be found we use positionToDefend:
			candidate = self.level.findNearestFreePosition(Vector2(x,y))
			if candidate == None: candidate = positionToDefend

			positions.append(candidate)
	
		# Issueing the commands to the bots: 
		i = 0
		for bot in bots:
			self.issue(typeOfMovement, bot, positions[i], description = str(positions[i]))
			i = i + 1

	def defaultStrategy(self):

		# for all bots which aren't currently doing anything
		for bot in self.game.bots_available:
		
			if bot.flag:
				# if a bot has the flag run to the scoring location
				flagScoreLocation = self.game.team.flagScoreLocation
				self.issue(commands.Charge, bot, flagScoreLocation, description = str(self.closestFriendToFlag(False)))
			else:
				# otherwise run to where the flag is
				enemyFlag = self.game.enemyTeam.flag.position
				self.issue(commands.Charge, bot, enemyFlag, description = str(self.closestFriendToFlag()))

		return 

	def testPedro(self):
		
		# Issueing the bot closest to the flag:
		#closestBot = self.closestFriendToFlag()[0]
		#self.issue(commands.Charge, closestBot, self.game.enemyTeam.flag.position, description = 'This is SPARTA!')
		
		
		# for all bots which aren't currently doing anything
		for bot in self.game.bots_available:
		
			if bot == self.closestFriendToFlag():
				
				if bot.flag:
					# if a bot has the flag run to the scoring location
					flagScoreLocation = self.game.team.flagScoreLocation
					self.issue(commands.Charge, bot, flagScoreLocation, description = 'Run Rudolph, Run!')
				else:
					# otherwise run to where the flag is
					enemyFlag = self.game.enemyTeam.flag.position
					self.issue(commands.Charge, bot, enemyFlag, description = 'This is SPARTAA!!')
					
			else: 
				
				if bot.position.distance(self.game.team.flag.position) < 8 :
					self.issue(commands.Defend, bot, description = 'YOU SHALL NOT PASS!!', facingDirection = self.game.enemyTeam.botSpawnArea[0])
				else: 
					self.surroundPosition(self.game.bots_available, self.game.team.flag.position, 5, commands.Charge)
					
		return
	
	def initialize(self):
		"""Use this function to setup your bot before the game starts."""
		self.done = False
		self.verbose = True    # display the command descriptions next to the bot labels
		
	
	def tick(self):
		"""Override this function for your own bots.  Here you can access all the information in self.game,
		which includes game information, and self.level which includes information about the level."""
		
		# Uncomment to log level information
		#self.log.debug(LevelHelper(self.level))
		
		# Uncomment to log flags and bots information
		#self.log.debug(GameHelper(self.game))
		
		# Test strategy here	
		#self.defaultStrategy()
		#self.testPedro()
		if not self.done:
			self.setupCassio()
		self.done = True
		
		self.testCassio()
		
		return
	
	def shutdown(self):
		"""Use this function to teardown your bot after the game is over, or perform an
		analysis of the data accumulated during the game."""
		pass

	
	


class LevelHelper():
	def __init__(self, level):
		self.level = level
	
	def __str__(self):
		res = ''
		res += 'width: %s\n' % self.level.width
		res += 'height: %s\n' % self.level.height
		res += 'blockHeights: %s\n' % self.level.blockHeights
		res += 'teamNames: %s\n' % self.level.teamNames
		res += 'flagSpawnLocations: %s\n' % self.level.flagSpawnLocations
		res += 'flagScoreLocations: %s\n' % self.level.flagScoreLocations
		res += 'botSpawnAreas: %s\n' % self.level.botSpawnAreas
		res += 'characterRadius: %s\n' % self.level.characterRadius
		res += 'FOVangle: %s\n' % self.level.FOVangle
		res += 'firingDistance: %s\n' % self.level.firingDistance
		res += 'walkingSpeed: %s\n' % self.level.walkingSpeed
		res += 'runningSpeed: %s\n' % self.level.runningSpeed
		res += 'gameLength: %s\n' % self.level.gameLength
		res += 'initializationTime: %s\n' % self.level.initializationTime
		res += 'respawnTime: %s\n' % self.level.respawnTime
		return res

class GameHelper():
	def __init__(self, game):
		self.game = game
	
	def state_switch(self, index):
		states = [
		'STATE_UNKNOWN',
		'STATE_IDLE',
		'STATE_DEFENDING',
		'STATE_MOVING',
		'STATE_ATTACKING',
		'STATE_CHARGING',
		'STATE_SHOOTING',
		'STATE_TAKINGORDERS'
		]
		return states[index]
	
	def __str__(self):
		res = ''
		res += 'Our team: %s\n' % self.game.team.name
		res += 'The enemy team: %s\n' % self.game.enemyTeam.name
		
		res += '---------Flags: -----------\n'
		for flag in self.game.flags.itervalues():
			res += '\tname: %s\n\tteam: %s\n\tposition: %s\n\tcarrier: %s\n\trespawnTimer: %s\n\n' % (flag.name, flag.team.name, flag.position, flag.carrier, flag.respawnTimer)
		
		res += '---------Alive bots: -----------\n'
		for bot in self.game.bots_alive:
			res += '\tname: %s\n\thealth: %s\n\tstate: %s\n\tposition: %s\n\tfacing: %s\n\tseenLast: %s\n\tflag: %s\n\tvisibleEnemies: %s\n\tseenBy: %s\n\n' % (bot.name, bot.health, self.state_switch(bot.state), bot.position, bot.facingDirection, bot.seenlast, bot.flag, bot.visibleEnemies, bot.seenBy)
		
		return res

