# Your AI for CTF must inherit from the base Commander class.  See how this is
# implemented by looking at the commander.py in the ./api/ folder.
from api import Commander

# The commander can send 'Commands' to individual bots.  These are listed and
# documented in commands.py from the ./api/ folder also.
from api import commands

# The maps for CTF are layed out along the X and Z axis in space, but can be
# effectively be considered 2D.
from api import Vector2


class IntermedCommander(Commander):
    """
    Rename and modify this class to create your own commander and add mycmd.Placeholder
    to the execution command you use to run the competition.
    """

    def initialize(self):
        """Use this function to setup your bot before the game starts."""
        self.verbose = True    # display the command descriptions next to the bot labels
        
    def tick(self):
        """Override this function for your own bots.  Here you can access all the information in self.game,
        which includes game information, and self.level which includes information about the level."""
        
        # Uncomment to log level information
        #self.log.debug(LevelHelper(self.level))
        
        # Uncomment to log flags and bots information
        #self.log.debug(GameHelper(self.game))
        
        # for all bots which aren't currently doing anything
        for bot in self.game.bots_available:
            if bot.flag:
                # if a bot has the flag run to the scoring location
                flagScoreLocation = self.game.team.flagScoreLocation
                self.issue(commands.Charge, bot, flagScoreLocation, description = 'Run to my flag')
            else:
                # otherwise run to where the flag is
                enemyFlag = self.game.enemyTeam.flag.position
                self.issue(commands.Charge, bot, enemyFlag, description = 'Run to enemy flag')

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
    
