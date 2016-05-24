import math
import lib601.util as util
import lib601.dist as dist

sonar_max = 1.5

class DynamicRobotMaze:
    ROBOT_DIAMETER = 0.44 # meters, approximate
    #ROBOT_MARGIN_FROM_WALL = 7 #= abs(ROBOT_DIAMETER*(x1-x0)/width)
    def __init__(self, height, width, x0, y0, x1, y1):
        self.width = width
        self.height = height
        self.x0,self.x1 = x0,x1
        self.y0,self.y1 = y0,y1
#        global ROBOT_MARGIN_FROM_WALL
#        global ROBOT_DIAMETER
        self.ROBOT_MARGIN_FROM_WALL = int(abs(0.44*(width)/(x1-x0)))
        print("width" + str(self.width))
        print("height" + str(self.height))

#        print(x1)
#        print(x0)
#        print(width)
        print("Margin: " + str(self.ROBOT_MARGIN_FROM_WALL))
#        self.grid = [[True for c in range(width)] for r in range(height)]
        self.grid = [[0.25 for c in range(width)] for r in range(height)]

    def point_to_indices(self, point):
        ix = int(math.floor((point.x-self.x0)*self.width/(self.x1-self.x0)))
        iix = min(max(0,ix),self.width-1)
        iy = int(math.floor((point.y-self.y0)*self.height/(self.y1-self.y0)))
        iiy = min(max(0,iy),self.height-1)
        return ((self.height-1-iiy,iix))

    def indices_to_point(self, loc):
        (r,c) = loc
        x = self.x0 + (c+0.5)*(self.x1-self.x0)/self.width
        y = self.y0 + (self.height-r-0.5)*(self.y1-self.y0)/self.height
        return util.Point(x,y)

    def is_clear(self, loc):
        (r,c) = loc
        if not (0 <= r < self.height and 0 <= c < self.width):
            return 1 #False
        return self.grid[r][c]

    def is_passable(self, loc):
        (r,c) = loc
        threshold = 0.8
        margin = self.ROBOT_MARGIN_FROM_WALL #7 ############## CHANGE
        for i in range(margin):
            for j in range(margin):
                #if loc[0]+i >= self.width or loc[0]-i < 0:
                #    return False
                #if loc[1]+j >= self.height or loc[1]-j < 0:
                #    return False

#                print("hi")
#                if not self.is_clear((loc[0]+i,loc[1]+j)):
#                    return False
#                if not self.is_clear((loc[0]+i,loc[1]-j)):
#                    return False
#                if not self.is_clear((loc[0]-i,loc[1]+j)):
#                    return False
#                if not self.is_clear((loc[0]-i,loc[1]-j)):
#                    return False

                if self.is_clear((r+i, c+j)) > threshold:
                    return False
                if self.is_clear((r+i, c-j)) > threshold:
                    return False
                if self.is_clear((r-i, c+j)) > threshold:
                    return False
                if self.is_clear((r-i, c-j)) > threshold:
                    return False

        return True
        #return self.is_clear((r,c))

    def prob_occupied(self, loc):
        (r,c) = loc
#        return float(not self.grid[r][c])
        return self.grid[r][c]

    prob_error = 0.8
    # 0 == clear
    # 1 == wall

    def sonar_hit(self, loc):
        (r,c) = loc
#        self.grid[r][c] = False
        d = dist.DDist({1:(self.grid[r][c]), 0:(1-self.grid[r][c])})
        def prob_hit_given_wall(x): #x is 0 or 1
            if x == 1:
                return dist.DDist({1.: 0.8, 0.: 0.2})
            return dist.DDist({1.: 0.1, 0.: 0.9})
        self.grid[r][c] = dist.bayes_rule(d, prob_hit_given_wall, 1).prob(1.)

    def sonar_pass(self, loc):
        (r,c) = loc
#        self.grid[r][c] = True
        d = dist.DDist({1: self.grid[r][c], 0: (1-self.grid[r][c])})
        def prob_hit_given_wall(x):
            if x == 1:
                return dist.DDist({1.: 0.8, 0.: 0.2})
            return dist.DDist({1.: 0.1, 0.: 0.9})
        self.grid[r][c] = dist.bayes_rule(d, prob_hit_given_wall, 0).prob(1.)


def make_maze_successors(maze):
    def successors(state):
        (r,c) = state
        out = []
        for (dr,dc) in [(1,0),(0,1),(-1,0),(0,-1)]:
            nr,nc = r+dr,c+dc
            if maze.is_passable((nr,nc)):
                out.append(((nr,nc), 1))
        return out
    return successors

