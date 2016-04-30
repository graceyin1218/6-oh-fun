from lib601.plotWindow import PlotWindow
from soar.io import io
import beliefGraph
import imp
imp.reload(beliefGraph)
import lib601.idealReadings as idealReadings
import lib601.markov as markov
from lib601.dist import *
import lib601.sonarDist as sonarDist
import os,os.path
import math
import sys
if sys.version_info >= (3,5):
    import checkoff35 as checkoff
else:
    import checkoff34 as checkoff
import lib601.util as util

####################################################################
###
### Preliminaries -- do not change the following code
###
####################################################################

labPath = os.getcwd()
WORLD_FILE = os.path.join(labPath,'baseWorld.py')
FORWARD_VELOCITY = 0.2 # meters / second
TIMESTEP_LENGTH = 0.1 # seconds


# Where the robot will be in the world
(x_min, x_max) = (0.5, 7.7)
robotY = y = 1.0

# Distance and Gain for Wall Following
desiredRight = 0.5
Kp,Ka = (10.0,2.0)

# Maximum "good" sonar reading
sonarMax = 1.5

#method to discretize values into boxes of size gridSize
def discretize(value, gridSize, maxBin=float('inf'), valueMin = 0):
    return min(int((value - valueMin)/gridSize), maxBin)

#method to clip x to be within lo and hi limits, inclusive
def clip(x, lo, hi):
    return max(lo, min(x, hi))

####################################################################
###
###          Probabilistic Models -- you may change this code
###
####################################################################

# Number of discrete locations and discrete observations
num_states = 100 
num_observations = 30


def naive_obs_model(s):
    return delta_dist(ideal[s])

def uniform_obs_model(s):
    return uniform_dist(range(num_observations))

def obs_model(s):
    #pass # your code here
    ideal_val = ideal[s]
    width = int(num_observations *.2)
    return mixture(triangle_dist(ideal_val, width, 0, num_observations-1), square_dist(0,num_observations), 0.8)

def naive_trans_model(s):
    return delta_dist(clip(s+1, 0, num_states-1))

def trans_model(s):
    dict = {}
    #find step as a fraction of state
    state_size = (x_max-x_min)/num_states
    step = FORWARD_VELOCITY*TIMESTEP_LENGTH/state_size
    whole_states = math.floor(step)
    if s+step >= num_states:
        return DDist({num_states-1:1})
    for i in range(num_states):
        dict[i] = 0
        if i == s + whole_states:
            if s+whole_states == num_states-1:
                dict[i] = 1
                break
            dict[i] = 1-(step-whole_states)
        if i == s + whole_states + 1:
            dict[i] = step-whole_states
    return DDist(dict)
    #pass # your code here
#    state_width = (x_max-x_min) / num_states
#    states_moved = (FORWARD_VELOCITY * TIMESTEP_LENGTH) / state_width
#    fullstates = int(states_moved)
#    nominal = clip(s + fullstates, 0, num_states - 1)
#    n2 = clip(nominal + 1, 0, num_states - 1)
#    p_mix = (states_moved-fullstates)
#    return mixture(delta_dist(n2), delta_dist(nominal), p_mix)

def confident_location(belief):
    return (-1, False)
    state_width = (x_max-x_min)/num_states
    #width of parking space in states
    parking_width = int(0.75/state_width)
    margin = int(0.15/state_width)
    most_prob_state = 0
    for state in belief.support():
        if belief.prob(state) > belief.prob(most_prob_state):
            most_prob_state = state
    if belief.prob(most_prob_state) < 90:
        return (most_prob_state, False)
    if ideal[most_prob_state] < 5: ## figure out what value works best...
        return (most_prob_state, False)
    lowerbound = -1
    upperbound = -1
    for state in belief.support():
        if abs(state-most_prob_state) < margin:
            if lowerbound == -1:
                lowerbound = state
            elif upperbound == -1:
                upperbound = state
    if ideal[lowerbound] == ideal[most_prob_state]:
        if ideal[upperbound] == ideal[most_prob_state]:
            return (most_prob_state, True)
    return (most_prob_state, False)
    #return (-1,False) #your code here

uniform_init_dist = square_dist(0, num_states)
spiked_init_dist = delta_dist(24)

INIT_DIST_TO_USE = uniform_init_dist
OBS_MODEL_TO_USE = obs_model#naive_obs_model
TRANS_MODEL_TO_USE = trans_model#naive_trans_model
REAL_ROBOT = False

######################################################################
###
###          Brain Methods -- do not change the following code
###
######################################################################

# Robot's Ideal Readings
ideal = idealReadings.compute_ideal_readings(WORLD_FILE, x_min, x_max, robotY, num_states, num_observations)

def get_parking_spot(ideal):
    avg = sum(ideal)/float(len(ideal))
    i = len(ideal)-1
    while i>0 and ideal[i]>avg:
        i -= 1
    j = i
    while j>0 and ideal[j]<avg:
        j -= 1
    i = j
    while i>0 and ideal[i]>avg:
        i -= 1
    return (i+1+j)/2


def on_load():
    global ideal, confident, parking_spot, target_theta, target_x

    parking_spot = get_parking_spot(ideal)
    target_x = None
    confident = False
    
    if not (hasattr(robot,'g') and robot.g.winfo_exists()):
        robot.g = beliefGraph.Grapher(ideal)
        robot.nS = num_states
    if robot.nS != num_states:
        robot.g.destroy()
        robot.g = beliefGraph.Grapher(ideal)
        robot.nS = num_states
    robot.hmm = markov.HMM(INIT_DIST_TO_USE,
                           TRANS_MODEL_TO_USE,
                           OBS_MODEL_TO_USE)
    robot.estimator = robot.hmm.make_state_estimator()
    robot.g.updateDist()
    robot.g.updateBeliefGraph([robot.estimator.belief.prob(s) \
                               for s in range(num_states)])
    robot.probMeasures = []
    robot.data = []
    target_theta = None

def on_start():
    if not REAL_ROBOT:
        checkoff.get_data(globals())

def on_step():
    if not REAL_ROBOT:
        checkoff.update(globals())
    global confident, target_x, target_theta
    sonars = io.get_sonars()

    pose = io.get_position(not REAL_ROBOT)
    (px, py, ptheta) = pose

    if confident:
        if target_theta is None:
            target_theta = util.fix_angle_plus_minus_pi(ptheta+math.pi/2)
        ptheta = util.fix_angle_plus_minus_pi(ptheta)
        if px>target_x+.05 and abs(ptheta)<math.pi/4:
            io.Action(fvel=-0.2,rvel=0).execute() #drive backwards if necessary
        elif px<target_x and abs(ptheta)<math.pi/4:
            io.Action(fvel=0.2,rvel=0).execute()  #drive to desired x location
        elif ptheta<target_theta-.05:
            io.Action(fvel=0,rvel=0.2).execute()  #rotate
        elif sonars[3]>.3:
            io.Action(fvel=0.2,rvel=0).execute()  #drive into spot
        else:
            io.Action(fvel=0,rvel=0).execute()  #congratulate yourself (or call insurance company)
        return

    
    # Quality metric.  Important to do this before we update the belief state, because
    # it is always a prediction
    if not REAL_ROBOT:
        parkingSpaceSize = .75
        robotWidth = 0.3
        margin = (parkingSpaceSize - robotWidth) / 2 
        robot.probMeasures.append(estimate_quality_measure(robot.estimator.belief,
                                                         x_min, x_max, num_states, margin,
                                                         px))
        trueS = discretize(px, (x_max - x_min)/num_states, valueMin = x_min)
        trueS = clip(trueS, 0, num_states-1)
        n = len(robot.probMeasures)
        
    # current discretized sonar reading
    left = discretize(sonars[0], sonarMax/num_observations, num_observations-1)
    if not REAL_ROBOT:
        robot.data.append((trueS, ideal[trueS], left))
    # obsProb
    obsProb = sum([robot.estimator.belief.prob(s) * OBS_MODEL_TO_USE(s).prob(left) \
                   for s in range(num_states)])

    # GRAPHICS
    if robot.g is not None:
        # redraw ideal distances (compensating for tk bug on macs)
        # draw robot's true state
        if not REAL_ROBOT:
            if trueS < num_states:
                robot.g.updateDist()
                robot.g.updateTrueRobot(trueS)
        # update observation model graph
        robot.g.updateObsLabel(left)
        robot.g.updateObsGraph([OBS_MODEL_TO_USE(s).prob(left) \
                                for s in range(num_states)])

    robot.estimator.update(left)
    (location, confident) = confident_location(robot.estimator.belief)

    if confident:
        target_x = (parking_spot-location)*(x_max-x_min)/float(num_states) + px
        print('I am at x =',location,': proceeding to parking space')
        if not REAL_ROBOT:
            checkoff.localized(globals())

    # GRAPHICS
    if robot.g is not None:
        # update world drawing
        # update belief graph
        robot.g.updateBeliefGraph([robot.estimator.belief.prob(s)
                                   for s in range(num_states)])

    # DL6 Angle Controller
    (distanceRight, theta) = sonarDist.get_distance_right_and_angle(sonars)
    if not theta:
       theta = 0
    e = desiredRight-distanceRight
    ROTATIONAL_VELOCITY = Kp*e - Ka*theta
    io.set_forward(FORWARD_VELOCITY)
    io.set_rotational(ROTATIONAL_VELOCITY)

def on_stop():
    if not REAL_ROBOT:
        code = checkoff.generate_code(globals())
        if isinstance(code, bytes):
            code = code.decode()
        print("Hex Code for Tutor:\n%s" % code, file=sys.stderr)
        p = PlotWindow()
        p.plot(robot.probMeasures)
        p.axes[0].set_ylim([0.0,1.0])

def on_shutdown():
    pass

def estimate_quality_measure(belief, x_min, x_max, num_states, delta, trueX):
    minGood = max(trueX - delta, x_min)
    maxGood = min(trueX + delta, x_max)
    stateSize = (x_max - x_min) / num_states
    minGoodDiscrete = max(0, discretize(minGood, stateSize, valueMin = x_min))
    maxGoodDiscrete = min(num_states-1,
                          discretize(maxGood, stateSize, valueMin = x_min)) + 1

    minGoodReconstituted = minGoodDiscrete * stateSize + x_min
    maxGoodReconstituted = maxGoodDiscrete * stateSize + x_min

    fracLowBinInRange = 1 - ((minGood - minGoodReconstituted) / stateSize)
    fracHighBinInRange = 1 - ((maxGoodReconstituted - maxGood) / stateSize)

    total =  sum(belief.prob(s) for s in range(minGoodDiscrete+1, maxGoodDiscrete))
    lowP = belief.prob(minGoodDiscrete) * fracLowBinInRange
    highP = belief.prob(maxGoodDiscrete) * fracHighBinInRange
    return total + lowP + highP
