# Problem Set 11: Simulating robots
# Name:
# Collaborators:
# Time:

import math
#import random
import ps11_visualize
from pylab import *

# === Provided classes

class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).

        x: a real number indicating the x-coordinate
        y: a real number indicating the y-coordinate
        """
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: integer representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)
    def __str__ (self):
        return str(self.getX())+","+  str(self.getY())

# === Problems 1 and 2

class RectangularRoom(object):
    
    #print random.sample([1,2,3,4,5,6,7,8,9], 3)
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.
        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        import random
        initFracDirt = .8
        
        
        self.width = width
        self.height = height
        
        self.dirtyDict={}


        coords = []
        for dimension1 in range(0, width):
            for dimension2 in range(0, height):
                self.dirtyDict[(dimension1, dimension2)]='clean'
                coords.append((dimension1,dimension2))
                
        
        sampleSize = int(round(initFracDirt*len(coords)))
        dirtyList = random.sample(coords,sampleSize)
        for tile in dirtyList:
            self.dirtyDict[tile] = 'dirty'

    def dirtyTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.
        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        if not int(pos.getX())==pos.getX() or int(pos.getY())==pos.getY(): #if pos does not lie on a boundry between tiles...
            self.dirtyDict[int(pos.getX()), int(pos.getY())]='dirty'            
        

    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.
        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        if not int(pos.getX())==pos.getX() or int(pos.getY())==pos.getY(): #if pos does not lie on a boundry between tiles...
            self.dirtyDict[int(pos.getX()), int(pos.getY())]='clean'

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        if self.dirtyDict[(m, n)]=="clean":
            return True
        elif self.dirtyDict[(m, n)]=="dirty":
            return False
            
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.width*self.height
        
    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        numClean=0
        for type in self.dirtyDict.values():
            if type == "clean":
                numClean+=1
        return numClean
    
    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        xPos = random.randrange(0, self.width)
        yPos = random.randrange(0, self.height)
        
        print "This statement is for debugging and xPos is: ",  xPos, ",and yPos is: ",  yPos
        return Pos(xPos, yPos)
        
    def isPositionInRoom(self, pos):
        """
        Return True if POS is inside the room.

        pos: a Position object.
        returns: True if POS is in the room, False otherwise.
        """
        return (0<= pos.getX() < self.width and 0<= pos.getY() < self.height)


class BaseRobot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in
    the room.  The robot also has a fixed speed.

    Subclasses of BaseRobot should provide movement strategies by
    implementing updatePositionAndClean(), which simulates a single
    time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified
        room. The robot initially has a random direction d and a
        random position p in the room.

        The direction d is an integer satisfying 0 <= d < 360; it
        specifies an angle in degrees.

        p is a Position object giving the robot's position.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        import random
        self.food = 10
        self.d = random.randrange(0, 360)
        #print "Initial direction is :" ,  self.d
        temp = random.randrange(0,  len(room.dirtyDict.keys())) #
        self.p = Position(room.dirtyDict.keys()[temp][0], room.dirtyDict.keys()[temp][1])
        self.speed=speed
        self.room =room
        self.room.cleanTileAtPosition(self.p)
    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.p
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.d
    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        if not self.room.isPositionInRoom(position):
            raise "Position not in the room."
        self.p = position
        
    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        if type(direction) != type(5):
            raise "Direction must be an integer"
        if direction > 360 or direction <0:
            raise "Direction must be between 0 and 360"
        self.d = direction

    def setRobotHunger(self, change):
        self.food -= change

    def getRobotFood(self):
        return self.food
        


class Robot(BaseRobot):
    """
    A Robot is a BaseRobot with the standard movement strategy.

    At each time-step, a Robot attempts to move in its current
    direction; when it hits a wall, it chooses a new direction
    randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        import random
        positionCandidate = self.getRobotPosition().getNewPosition(self.getRobotDirection(), self.speed)        
        #print "position candidate is: " ,  positionCandidate
        while not self.room.isPositionInRoom(positionCandidate):
            self.setRobotDirection(random.randrange(0, 360))
            positionCandidate = self.getRobotPosition().getNewPosition(self.getRobotDirection(), self.speed)
        self.setRobotPosition(positionCandidate)
        
        #feed this robot if there was food right there...
       # if self.room.dirtyDict[positionCandidate] == 'dirty':
       #     self.food += 1
        self.room.cleanTileAtPosition(positionCandidate)

        

# === Problem 3

def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type, visualize):
    """
    Runs NUM_TRIALS trials of the simulation and returns a list of
    lists, one per trial. The list for a trial has an element for each
    timestep of that trial, the value of which is the percentage of
    the room that is clean after that timestep. Each trial stops when
    MIN_COVERAGE of the room is clean.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE,
    each with speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    Visualization is turned on when boolean VISUALIZE is set to True.

    um_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. Robot or
                RandomWalkRobot)
    visualize: a boolean (True to turn on visualization)
    """
    trialsList = []
    for trial in range(num_trials):
        if visualize:
            anim = ps11_visualize.RobotVisualization(num_robots, width, height)
        trialsList.append([]) #append a list to hold the results of this trial
        currentRoom = RectangularRoom(width, height) #make a new room for each trial
        roboList = []
        for botNum in range(num_robots):          #make the right number of robots
            roboList.append(robot_type(currentRoom, speed)) #all of the bots clean the same room
          #  print "making Robot: ",  botNum
        time =0
        while float(currentRoom.getNumCleanedTiles())/float(currentRoom.getNumTiles())<min_coverage:#true if the min coverage is not clean
            if visualize:
                anim.update(currentRoom, roboList)
            #print "in the while loop and clean portion is: ",  float(currentRoom.getNumCleanedTiles())/float(currentRoom.getNumTiles())
            trialsList[trial].append(float(currentRoom.getNumCleanedTiles())/float(currentRoom.getNumTiles()))
            for bot in roboList:          #hey all you robots...
                #get hungrier...
                bot.setRobotHunger(-1)
             #   if bot.getRobotHunger < 1:
                    

                bot.updatePositionAndClean() #... clean the floor, stupid minions!
        if visualize:
            anim.done()
    return trialsList        

# === Provided function
def computeMeans(list_of_lists):
    """
    Returns a list as long as the longest list in LIST_OF_LISTS, where
    the value at index i is the average of the values at index i in
    all of LIST_OF_LISTS' lists.

    Lists shorter than the longest list are padded with their final
    value to be the same length.
    """
    # Find length of longest list
    longest = 0
    for lst in list_of_lists:
        if len(lst) > longest:
           longest = len(lst)
    # Get totals
    tots = [0]*(longest)
    for lst in list_of_lists:
        for i in range(longest):
            if i < len(lst):
                tots[i] += lst[i]
            else:
                tots[i] += lst[-1]
    # Convert tots to an array to make averaging across each index easier
    tots = pylab.array(tots)
    # Compute means
    means = tots/float(len(list_of_lists))
    return means

def averageLengthOfLists(listOfLists):
    numLists = len(listOfLists)
    sumOfLengths=0
    for list in listOfLists:
        sumOfLengths += len(list)
    return float(sumOfLengths)/float(numLists)
    
# === Problem 4
def showPlot1():
    """
    Produces a plot showing dependence of cleaning time on room size.
    """
    
    fiveByFiveList = runSimulation(1, 1.0, 5, 5, 0.75, 5, Robot, False)
    tenByTenList = runSimulation(1, 1.0, 10, 10, 0.75, 5, Robot, False)
    fifteenByFifteenList = runSimulation(1, 1.0, 15, 15, 0.75, 5, Robot, False)
    twentyByTwentyList = runSimulation(1, 1.0, 20, 20, 0.75, 5, Robot, False)
    twentyFiveByTwentyFiveList = runSimulation(1, 1.0, 25, 25, 0.75, 5, Robot, False)
    
    fiveByAverage = averageLengthOfLists(fiveByFiveList)
    tenByAverage = averageLengthOfLists(tenByTenList)
    fifteenByAverage = averageLengthOfLists(fifteenByFifteenList)
    twentyByAverage = averageLengthOfLists(twentyByTwentyList)
    twentyFiveByAverage = averageLengthOfLists(twentyFiveByTwentyFiveList)
    
    areas = [5*5, 10*10, 15*15,  20*20,  25*25]
    
    plot(areas, [fiveByAverage, tenByAverage, fifteenByAverage, twentyByAverage, twentyFiveByAverage])
    xlabel('Room Area')
    ylabel('Average number of Time Steps')
    title('Mean time vs Room Area')
    show()

    
def showPlot2():
    """
    Produces a plot showing dependence of cleaning time on number of robots.
    """
    listOfTrialLists=[]
    for i in range(10):
        listOfTrialLists.append(runSimulation(i+1, 1, 25, 25, 0.75, 5,Robot, False))
    listOfAverageTimes=[]
    for i in range(10):
        listOfAverageTimes.append(averageLengthOfLists(listOfTrialLists[i]))
    
    plot([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], listOfAverageTimes)
    xlabel ('Num Robots')
    ylabel ('Time Steps')
    title('Time vs Number of Robots')
    show()

def showPlot3():
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    widthToHeights=[20/20, float(25)/float(16), 40/10, float(50)/float(8), 80/5, 100/4]
    
    firstAvg = averageLengthOfLists(runSimulation(2, 1.0, 20, 20, 0.75, 10, Robot, False))
    secondAvg=averageLengthOfLists(runSimulation(2, 1.0, 25, 16, 0.75, 10, Robot, False))
    thirdAvg=averageLengthOfLists(runSimulation(2, 1.0, 40, 10, 0.75, 10, Robot, False))
    fourthAvg=averageLengthOfLists(runSimulation(2, 1.0, 50, 8, 0.75, 10, Robot, False))
    fifthAvg=averageLengthOfLists(runSimulation(2, 1.0, 80, 5, 0.75, 10, Robot, False))
    sixthAvg=averageLengthOfLists(runSimulation(2, 1.0, 100, 4, 0.75, 10, Robot, False))
    
    plot(widthToHeights, [firstAvg, secondAvg,thirdAvg, fourthAvg, fifthAvg, sixthAvg])
    xlabel('Ratio of Room Width to Height')
    ylabel('Time Steps')
    title('Time vs Width to Height Ratio for Two Robots')
    show()

def showPlot4():
    """
    Produces a plot showing cleaning time vs. percentage cleaned, for
    each of 1-5 robots.
    """
    coverages = [.1, .2, .3, .4, .5, .6, .7, .8, .9, 1.0]
    oneBot = []
    twoBot =[]
    threeBot =[]
    fourBot=[]
    fiveBot=[]
    for amount in coverages:
        oneBot.append(averageLengthOfLists(runSimulation(1, 1.0, 25, 25, amount, 5, Robot, False)))
        twoBot.append(averageLengthOfLists(runSimulation(2, 1.0, 25, 25, amount, 5, Robot, False)))
        threeBot.append(averageLengthOfLists(runSimulation(3, 1.0, 25, 25, amount, 5, Robot, False)))
        fourBot.append(averageLengthOfLists(runSimulation(4, 1.0, 25, 25, amount, 5, Robot, False)))
        fiveBot.append(averageLengthOfLists(runSimulation(5, 1.0, 25, 25, amount, 5, Robot, False)))
    plot(coverages, oneBot, coverages, twoBot, coverages, threeBot, coverages, fourBot, coverages, fiveBot)
    xlabel('Percent of Room Cleaned')
    ylabel('Time Steps')
    title('Mean Time vs Percent of Room Cleaned for 1 through 5 Robots')
    show()
    


# === Problem 5

class RandomWalkRobot(BaseRobot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement
    stratellgy: it chooses a new direction at random after each
    time-step.
    """
    def updatePositionAndClean(self):
        
        import random
        self.setRobotDirection(random.randrange(0, 360))
        positionCandidate = self.getRobotPosition().getNewPosition(self.getRobotDirection(), self.speed)        
        #print "position candidate is: " ,  positionCandidate
        while not self.room.isPositionInRoom(positionCandidate):
            self.setRobotDirection(random.randrange(0, 360))
            positionCandidate = self.getRobotPosition().getNewPosition(self.getRobotDirection(), self.speed)
        self.setRobotPosition(positionCandidate)
        self.room.cleanTileAtPosition(positionCandidate)

# === Problem 6

def showPlot5():
    """
    Produces a plot comparing the two robot strategies.
    """
    # TODO: Your code goes here
def testing():
#    pos1 = Position(2, 8)
#    room1 = RectangularRoom(5, 10)
#    room1.cleanTileAtPosition(pos1)
#    pos2 = Position(5, 11)
#    
#    robo1=Robot(room1, 5)
#    print "The robot has position: ", [robo1.p.getX(), robo1.p.getY()]  ,  " and direction:",  robo1.d
#    robo1.updatePositionAndClean()
    num_robots = 10
    speed = 1.0
    width =25
    height =25
    min_coverage =0.8
    num_trials = 5
    robot_type = RandomWalkRobot
    visualize = True
    results = runSimulation(num_robots, speed, width, height, min_coverage,  num_trials, robot_type, visualize)
    print 'here'
    print computeMeans(results)
    
showPlot4()
testing()    
