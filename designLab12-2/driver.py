import math
import lib601.util as util

# which point in the path we should aim for.
loc_in_path = 0

turning = True

def drive(path, pos, angle):
    """
    this function should return a tuple (fv, rv), where
    fv is the forward velocity the robot should use on this step, and
    rv is the rotational velocity the robot should use on this step
    in order to follow the desired path
    pos is the robot's current position, as an instance of util.Point
    angle is the robot's current angle in radians
    """

    # will follow the suggested algorithm:
    #   * turn towards the new point without moving forward
    #   * move forward until close enough

    global loc_in_path
    global turning

    # if we made it to the end..
    if loc_in_path == len(path):
        return(0,0)

    if pos.distance(path[loc_in_path]) < 0.1:
        turning = True
        loc_in_path += 1
        return(0,0)

    copy_pos = None
    copy_next = None
    difference = 100000
    theta_d = None
    if turning:
        k_a = -2
        # not sure if calling methods on Points alters the original.. I think it does?
        copy_pos = util.Point(pos.xy_tuple()[0], pos.xy_tuple()[1])
        copy_next = util.Point(path[loc_in_path].xy_tuple()[0], path[loc_in_path].xy_tuple()[1])

        copy_next = copy_next.add(copy_pos.scale(-1)).scale(-1)

        ## GOD EXPLAIN CLEARLY HOW ANGLE_TO WORKS!!!! I WASTED SO MUCH TIME FIGURING THIS OUT -_-

        theta_d = copy_next.angle_to(util.Point(0,0))

        difference = (angle_difference(angle, theta_d))#%math.pi

        if abs(difference) < 0.01:
            turning = False
            #print("TURNING FALSE")
            fv = 0
            rv = 0
        else:
            rv = k_a*difference
            fv = 0
    else:
        k_d = 1
        distance = pos.distance(path[loc_in_path])
        # checks for closeness to goal at the start of this function. Don't need to check here
        fv = k_d#*distance
        rv = 0

    #print("turning " + str(turning))
    #print("distance " + str(pos.distance(path[loc_in_path])))
    #print("angle difference " + str(difference))
    #print("theta_d " + str(theta_d))
    #print("robot angle " + str(angle))
    #print("going to " + str(path[loc_in_path].xy_tuple()))
    #print(str(copy_pos))#.xy_tuple()))
    #print(str(copy_next))#.xy_tuple()))
    #print()

    return (fv, rv)


def angle_difference(theta1, theta2):
    """
    Computes the difference between theta1 and theta2, and reports the result
    as an angle that is guaranteed to be between -pi and pi
    """
    diff = theta1 - theta2
    while diff > math.pi:
        diff -= 2*math.pi
    while diff < -math.pi:
        diff += 2*math.pi
    return diff
