import sys
import maze
from importlib import reload
reload(maze)
import search
reload(search)
from mazeGraphics import *

import lib601.util as util
import lib601.markov as markov
from soar.io import io
import soar.outputs.simulator as sim

if sys.version_info >= (3,5):
    import noiseModel35 as noiseModel
    import checkoff35 as checkoff
else:
    import noiseModel34 as noiseModel
    import checkoff34 as checkoff

import time
import math
import random
import sonarDist

###### SETUP

NOISE_ON = True

sl13World = [0.15, util.Point(7.0, 1.0), (-0.5, 8.5, -0.5, 6.5)]
bigFrustrationWorld = [0.2, util.Point(7.0, 1.0), (-0.5, 8.5, -0.5, 8.5)]
frustrationWorld = [0.15, util.Point(3.5, 0.5), (-0.5, 5.5, -0.5, 5.5)]
raceWorld = [0.1, util.Point(2.0, 5.5), (-0.5, 5.5, -0.5, 8.5)]
bigPlanWorld = [0.25, util.Point(3.0, 1.0), (-0.5, 10.5, -0.5, 10.5)]
realRobotWorld = [0.1, util.Point(1.5,0.0), (-2.0, 6.0, -2.0, 6.0)]
robotRaceWorld = [0.1, util.Point(3.0,0.0), (-2.0, 6.0, -2.0, 6.0)]

THE_WORLD = raceWorld#bigFrustrationWorld #sl13World
(grid_square_size, goal_point, (x_min, x_max, yMin, yMax)) = THE_WORLD

# graphics options
show_heatmap = True#False
show_passable = False
keep_old_windows = False

###### SOAR CONTROL

# this function is called when the brain is (re)loaded
def on_load():
    global goal_point
    #initialize robot's internal map
    width = int((x_max-x_min)/grid_square_size)
    height = int((yMax-yMin)/grid_square_size)
    robot.map = maze.DynamicRobotMaze(height,width,x_min,yMin,x_max,yMax)
    robot.goalIndices = robot.map.point_to_indices(goal_point)

    goal_point = robot.map.indices_to_point(robot.goalIndices)

    sim.SONAR_VARIANCE = (lambda mean: 0.001) if NOISE_ON else (lambda mean: 0) #sonars are accurate to about 1 mm
    robot.plan = None
    robot.successors = maze.make_maze_successors(robot.map)
    #initialize graphics
    robot.windows = []
    if show_heatmap:
        robot.windows.append(HeatMapWindow(robot.map))
    robot.windows.append(PathWindow(robot.map, show_passable))
    for w in robot.windows:
        w.redraw_world()
        w.render()
    

#    print(robot.map.is_passable((40,55)))

# this function is called when the start button is pushed
def on_start():
    robot.done = False
    robot.count = 0
    robot.start_time = time.time()
    checkoff.get_data(globals())


# this function is called 10 times per second
def on_step():
    global inp
    robot.count += 1
    inp = io.SensorInput(cheat=True)


    # discretize sonar readings
    # each element in discrete_sonars is a tuple (d, cells)
    # d is the distance measured by the sonar
    # cells is a list of grid cells (r,c) between the sonar and the point d meters away
    discrete_sonars = []
    for (sonar_pose, distance) in zip(sonarDist.sonar_poses,inp.sonars):
        if NOISE_ON:
            distance = noiseModel.noisify(distance, grid_square_size)
        if distance >= 5:
            sensor_indices = robot.map.point_to_indices(inp.odometry.transformPose(sonar_pose).point())
            hit_indices = robot.map.point_to_indices(sonarDist.sonar_hit(1, sonar_pose, inp.odometry))
            ray = util.line_indices(sensor_indices, hit_indices)
            discrete_sonars.append((distance, ray))
            continue
        sensor_indices = robot.map.point_to_indices(inp.odometry.transformPose(sonar_pose).point())
        hit_indices = robot.map.point_to_indices(sonarDist.sonar_hit(distance, sonar_pose, inp.odometry))
        ray = util.line_indices(sensor_indices, hit_indices)
        discrete_sonars.append((distance, ray))


    # figure out where robot is
    start_point = inp.odometry.point()
    startCell = robot.map.point_to_indices(start_point)

    def plan_wont_work():
        for point in robot.plan:
            if not robot.map.is_passable(point):
                return True
        return False

    # if necessary, make new plan
    if robot.plan is None or plan_wont_work(): #discrete_sonars[3][0] < 0.3: ###### or if the robot is about to crash into a wall
        print('REPLANNING')
        robot.plan = search.uniform_cost_search(robot.successors,
                              robot.map.point_to_indices(inp.odometry.point()),
                              lambda x: x == robot.goalIndices,
                              lambda x: 0)


    # make the path less jittery

    #print(robot.plan)
    to_remove = []
    if robot.plan is not None:
        for i in range(len(robot.plan)-2):
            line = util.LineSeg(util.Point(robot.plan[i][0], robot.plan[i][1]), util.Point(robot.plan[i+1][0], robot.plan[i+1][1]))
            if line.dist_to_point(util.Point(robot.plan[i+2][0], robot.plan[i+2][1])) < 0.1:
                to_remove.append(robot.plan[i+1])
    print(to_remove)
    for i in to_remove:
        robot.plan.remove(i)

    #print(robot.plan)
    #print()

    # graphics (draw robot's plan, robot's location, goal_point)
    # do not change this block
    for w in robot.windows:
        w.redraw_world()
    robot.windows[-1].mark_cells(robot.plan,'blue')
    robot.windows[-1].mark_cell(robot.map.point_to_indices(inp.odometry.point()),'gold')
    robot.windows[-1].mark_cell(robot.map.point_to_indices(goal_point),'green')


    # update map
    for (d,cells) in discrete_sonars:
        #print(cells)
        if d < 5:
            robot.map.sonar_hit(cells[-1])
        for i in range(len(cells)-1):
            robot.map.sonar_pass(cells[i])


    # if we are within 0.1m of the goal point, we are done!
    if start_point.distance(goal_point) <= 0.1:
        io.Action(fvel=0,rvel=0).execute()
        code = checkoff.generate_code(globals())
        if isinstance(code, bytes):
            code = code.decode()
        raise Exception('Goal Reached!\n\n%s' % code)

    # otherwise, figure out where to go, and drive there
    destination_point = robot.map.indices_to_point(robot.plan[0])
    while start_point.isNear(destination_point,0.1) and len(robot.plan)>1:
        robot.plan.pop(0)
        destination_point = robot.map.indices_to_point(robot.plan[0])

    currentAngle = inp.odometry.theta
    angleDiff = start_point.angleTo(destination_point)-currentAngle
    angleDiff = util.fix_angle_plus_minus_pi(angleDiff)
    fv = rv = 0
    if start_point.distance(destination_point) > 0.1:
        if abs(angleDiff) > 0.1:
            rv = 4*angleDiff
        else:
            fv = 4*start_point.distance(destination_point)
    io.set_forward(fv)
    io.set_rotational(rv)


    # render the drawing windows
    # do not change this block
    for w in robot.windows:
        w.render()

# called when the stop button is pushed
def on_stop():
    stopTime = time.time()
    print('Total steps:', robot.count)
    print('Elapsed time in seconds:', stopTime - robot.start_time)

def on_shutdown():
    if not keep_old_windows:
        for w in robot.windows:
            w.window.destroy()
