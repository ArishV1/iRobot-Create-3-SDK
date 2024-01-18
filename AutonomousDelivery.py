from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

import AuxAutonomousDelivery as aux

# === CREATE ROBOT OBJECT
robot = Create3(Bluetooth("C-3PO"))

# === FLAG VARIABLES
HAS_COLLIDED = False
HAS_REALIGNED = False
HAS_FOUND_OBSTACLE = False
HAS_ARRIVED = False

# === OTHER NAVIGATION VARIABLES
SENSOR2CHECK = 0
IR_ANGLES = [-65.3, -38.0, -20.0, -3.0, 14.25, 34.0, 65.3]
DESTINATION = (-120, 90)
ARRIVAL_THRESHOLD = 5

bumper = False


# ==========================================================
# FAIL SAFE MECHANISMS

# EITHER BUTTON
@event(robot.when_touched, [True, True])  # User buttons: [(.), (..)]
async def when_either_button_touched(robot):
    global bumper
    bumper = True
    await robot.set_wheel_speeds(0,0)
    await robot.set_lights(Robot.LIGHT_ON, Color(255, 0, 0))

# EITHER BUMPER
@event(robot.when_bumped, [True, True])  # [left, right]
async def when_either_bumped(robot):
    global bumper
    bumper = True
    await robot.set_wheel_speeds(0,0)
    await robot.set_lights(Robot.LIGHT_ON, Color(255, 0, 0))

# ==========================================================

# === REALIGNMENT BEHAVIOR
async def realignRobot(robot):
    global DESTINATION
    global HAS_REALIGNED
    currentPosition = await robot.get_position()
    angle1 = aux.getCorrectionAngle(currentPosition.heading)
    await robot.turn_right(angle1)
    relativeAngle = aux.getAngleToDestination(currentPosition, DESTINATION)
    HAS_REALIGNED = True
    await robot.turn_right(relativeAngle)


# === MOVE TO GOAL
async def moveTowardGoal(robot):
    global HAS_FOUND_OBSTACLE, IR_ANGLES, SENSOR2CHECK
    await robot.set_wheel_speeds(10,10)
    IR_readings = (await robot.get_ir_proximity()).sensors
    minProximity, minAngle = aux.getMinProxApproachAngle(IR_readings, IR_ANGLES)
    if minProximity <= 20.0:
        await robot.set_wheel_speeds(0,0)
        if minAngle > 0:
            await robot.turn_left(90 - minAngle)
            SENSOR2CHECK = 6
        else:
            await robot.turn_right(90 + minAngle)
            SENSOR2CHECK = 0
        HAS_FOUND_OBSTACLE = True


# === FOLLOW OBSTACLE
async def followObstacle(robot):
    global HAS_FOUND_OBSTACLE, HAS_REALIGNED, SENSOR2CHECK
    await robot.set_wheel_speeds(10,10)
    IR_Readings = (await robot.get_ir_proximity()).sensors
    minimumProximity = 4095/(IR_Readings[SENSOR2CHECK] + 1)
    if minimumProximity < 20.0:
        if SENSOR2CHECK == 6:
            await robot.set_wheel_speeds(0,0)
            await robot.turn_left(3)
            await robot.set_wheel_speeds(5,5)
        elif SENSOR2CHECK == 0:
            await robot.set_wheel_speeds(0,0)
            await robot.turn_right(3)
            await robot.set_wheel_speeds(5,5)
    elif minimumProximity > 100.0:
        await robot.move(30)
        HAS_REALIGNED = False
        HAS_FOUND_OBSTACLE = False


# === NAVIGATION TO DELIVERY
@event(robot.when_play)
async def makeDelivery(robot):
    global HAS_ARRIVED, HAS_COLLIDED, HAS_REALIGNED, HAS_FOUND_OBSTACLE
    global DESTINATION, ARRIVAL_THRESHOLD, IR_ANGLES, SENSOR2CHECK, bumper
    while HAS_ARRIVED == False:
        pos = await robot.get_position()
        x = pos.x
        y = pos.y
        HAS_ARRIVED = aux.checkPositionArrived((x,y), DESTINATION, ARRIVAL_THRESHOLD)
        if HAS_ARRIVED:
            HAS_ARRIVED = True
            await robot.set_lights(Robot.LIGHT_SPIN,Color(0,255,0))
            await robot.set_wheel_speeds(0,0)
            break
        else:
            if not HAS_REALIGNED and not HAS_FOUND_OBSTACLE:
                await realignRobot(robot)
            if not HAS_FOUND_OBSTACLE and HAS_REALIGNED:
                await moveTowardGoal(robot)
            if HAS_FOUND_OBSTACLE:
                await followObstacle(robot)
            if bumper == True:
                await robot.set_wheel_speeds(0,0)
                break



# start the robot
robot.play()
