import imp
import sys
import math
import soarWorld
import create_maze
import lib601.util as util

from soar.io import io

if sys.version_info >= (3,5):
    import checkoff35 as checkoff
else:
    import checkoff34 as checkoff

import search
import driver
import robotmaze
for i in (search,driver,robotmaze,create_maze):
    imp.reload(i)
from search import search
from driver import drive
from robotmaze import RobotMaze, color_cell, make_maze_successors

import tk
tk.setInited()

worldname = 'dl12World'
#worldname = 'bigEmptyWorld'

def get_path(worldname, maze):
    if worldname == 'dl12World':
        #pass # your code here
        path = search(make_maze_successors(maze), maze.start, lambda x: x == maze.goal, False, True)
        ans = []
        for p in path:
            ans.append(maze.indices_to_point((p[0], p[1])))
        return ans
    else:
        return [util.Point(0.911250, 0.911250), util.Point(1.721250, 0.506250), util.Point(2.531250, 1.316250), util.Point(1.721250, 1.721250), util.Point(0.911250, 2.126250), util.Point(1.721250, 2.936250), util.Point(2.531250, 2.531250)]


PATH_TO_WORLD = '%s.py' % worldname
cells_wide = 150
cells_high = 150
world = create_maze.get_maze_text(PATH_TO_WORLD, (10.11, 0.687), cells_high, cells_wide)

bounds = {'dl12World': (0.0,0.0,10.8,10.8),
          'bigEmptyWorld': (0.0,0.0,4.05,4.05)}


# this function is called when the brain is loaded
def on_load():
    checkoff.get_data(globals())
    (robot.window, robot.initial_location) = \
                   soarWorld.plot_soar_world_dw(PATH_TO_WORLD)
    b = bounds[worldname]
    robot.maze = RobotMaze(world, b[0], b[1], b[2], b[3],
                           robot.window, robot.initial_location)
    robot.path = get_path(worldname, robot.maze)
    if robot.path:
        robot.window.draw_path([i.x - \
                               robot.initial_location.x \
                               for i in robot.path],
                              [i.y - \
                               robot.initial_location.y \
                               for i in robot.path], color = 'blue')
    else:
        print('no plan from', robot.maze.start, 'to', robot.maze.goal)
    robot.slime_x = []
    robot.slime_y = []


# this function is called when the start button is pushed
def on_start():
    pass


# this function is called 10 times per second
def on_step():
    x, y, theta = io.get_position(cheat=True)
    robot.slime_x.append(x)
    robot.slime_y.append(y)
    checkoff.update(globals())

    # the following lines compute the robot's current position and angle
    current_point = util.Point(x,y).add(robot.initial_location)
    current_angle = theta

    forward_v, rotational_v = drive(robot.path, current_point, current_angle)
    io.set_forward(forward_v)
    io.set_rotational(rotational_v)


# called when the stop button is pushed
def on_stop():
    for i in range(len(robot.slime_x)):
        robot.window.drawPoint(robot.slime_x[i], robot.slime_y[i], 'red')
    if worldname == 'bigEmptyWorld' and sys.exc_info() == (None, None, None):
        code = checkoff.generate_code(globals())
        if isinstance(code, bytes):
            code = code.decode()
        print('Code for Driving in Tutor:\n%s' % code)


# called when brain or world is reloaded (before setup)
def on_shutdown():
    pass
