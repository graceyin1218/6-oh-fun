import sys
import random
import lib601.util as util

if sys.version_info >= (3,5):
    from mazeAnswers35 import Maze
else:
    from mazeAnswers34 import Maze

class RobotMaze(Maze):
    ROBOT_DIAMETER = 0.44 # meters, approximate

    def __init__(self, mapText, x0, y0, x1, y1, window=None, ril=None):
        Maze.__init__(self, mapText) #run Maze's __init__ on this instance
        self.x0 = float(x0)
        self.y0 = float(y0)
        self.x1 = float(x1)
        self.y1 = float(y1)
        self.window = window
        self.ril = ril
        self.mapText = mapText
    
    def point_to_indices(self, point):
        state_width = (self.x1-self.x0) / self.width
        c = int((point.x-self.x0)/state_width)
        c = min(max(0, c), self.width-1)
        state_height = (self.y1-self.y0) / self.height
        r = self.height - 1 - int((point.y-self.y0)/state_height)
        r = min(max(0, r), self.height-1)
        return (r,c)

    def indices_to_point(self, loc):
        (r, c) = loc
        x = self.x0 + (c+0.5)*(self.x1-self.x0)/self.width
        y = self.y0 + (self.height-r-0.5)*(self.y1-self.y0)/self.height
        return util.Point(x,y)

    def is_passable(self, loc):
        #s = Maze.is_passable(self, loc)
        #if not s:
        #    return False
        
        margin = 7 ############## CHANGE
        for i in range(margin):
            for j in range(margin):
                if loc[0]+i >= self.width or loc[0]-i < 0:
                    return False
                if loc[1]+j >= self.height or loc[1]-j < 0:
                    return False
                if self.mapText[loc[0]+i][loc[1]+j] == "#":
                    return False
                if self.mapText[loc[0]+i][loc[1]-j] == "#":
                    return False
                if self.mapText[loc[0]-i][loc[1]+j] == "#":
                    return False
                if self.mapText[loc[0]-i][loc[1]-j] == "#":
                    return False
                """
                if loc[0]+i < self.width:
                    if loc[1]+j < self.height:
                        if self.mapText[loc[0]+i][loc[1]+j] == "#": 
                            return False
                    if loc[1]-j >= 0:
                        if self.mapText[loc[0]+i][loc[1]-j] == "#":
                            return False
                if loc[0]-i > 0:
                    if loc[1] + j >= self.height or loc[1] - j < 0:
                        if self.mapText[loc[0]-i][loc[1]+j] == "#":
                            return False
                        if self.mapText[loc[0]-i][loc[1]-j] == "#":
                            return False
                """
                """
                if self.mapText[i][-j] == "#":
                    return False
                if self.mapText[-i][j] == "#":
                    return False
                if self.mapText[-i][-j] == "#":
                    return False
                """
                """
                if not is_passable((loc[0]+i, loc[1]+j)):
                    return False
                if not is_passable((loc[0]-i, loc[1]+j)):
                    return False
                if not is_passable((loc[0]+i, loc[1]-j)):
                    return False
                if not is_passable((loc[0]-i, loc[1]+j)):
                    return False
                """
        return True

def color_cell(maze, loc, color='PapayaWhip'):
    """
    Colors the cell at location loc (specified as an (r,c) tuple) to 
    be the specified color (by default, LPK's favorite color, Papaya Whip).
    Possible colors are: ('black', 'white', 'red', 'green', 'blue', 'purple',
    'orange', 'darkGreen', 'gold', 'chocolate', 'PapayaWhip', 'MidnightBlue',
    'HotPink', 'chartreuse')
    """
    state_width = (maze.x1-maze.x0) / maze.width
    p = maze.indices_to_point(loc)
    ril = maze.ril
    maze.window.drawSquare(p.x - ril.x, p.y - ril.y,
                            state_width, color=color)
    maze.window.canvas.update()


def make_maze_successors(maze):
    def s(state):
        (r,c) = state
        color_cell(maze, state)
        potential = [(r+i, c+j) for (i,j) in [(1,0),(0,1),(-1,0),(0,-1)]]
        #random.shuffle(potential)
        return [cell for cell in potential if maze.is_passable(cell)]
    return s

