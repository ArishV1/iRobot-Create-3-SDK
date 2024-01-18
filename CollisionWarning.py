from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

# robot is the instance of the robot that will allow us to call
# its methods and to define events with the @event decorator.
robot = Create3(Bluetooth("ARISH")) 

y=True

# LEFT BUTTON
@event(robot.when_touched, [True, False])  # User buttons: [(.), (..)]
async def when_left_button_touched(robot):
    global y
    await robot.set_wheel_speeds(0,0)
    await robot.set_lights(Robot.LIGHT_ON,Color(255,0,0))
    y=False


# RIGHT BUTTON
@event(robot.when_touched, [False, True])  # User buttons: [(.), (..)]
async def when_right_button_touched(robot):
    global y
    await robot.set_wheel_speeds(0,0)
    await robot.set_lights(Robot.LIGHT_ON,Color(255,0,0))
    y=False


# EITHER BUMPER
@event(robot.when_bumped, [True, True])  # [left, right]
async def when_either_bumped(robot):
    global y
    await robot.set_wheel_speeds(0,0)
    await robot.set_lights(Robot.LIGHT_ON,Color(255,0,0))
    y=False

@event(robot.when_play)
async def avoidCollision(robot):
    global y
    x=True
    while x:
        if y==False:
            await robot.set_wheel_speeds(0, 0)
            await robot.set_lights(Robot.LIGHT_ON,Color(255,0,0))
            break
        readings = (await robot.get_ir_proximity()).sensors
        proximity = 4095/(readings[3] + 1)
        
        if proximity<=float(5):
            await robot.set_lights(Robot.LIGHT_ON,Color(255,0,0))
            await robot.set_wheel_speeds(0,0)
            await robot.play_note(Note.D7, 1.00)
            x=False
        elif proximity<=float(30):
            await robot.set_wheel_speeds(1,1)
            await robot.play_note(Note.D6, 0.1)
            await robot.set_lights(Robot.LIGHT_BLINK,Color(255,65,0))
        elif proximity<=float(100):
            await robot.set_wheel_speeds(4,4)
            await robot.set_lights(Robot.LIGHT_BLINK,Color(255,255,0))
            await robot.play_note(Note.D5, 0.1)
        elif proximity>100:
            await robot.set_wheel_speeds(8,8)
            await robot.set_lights(Robot.LIGHT_BLINK,Color(0,255,0))
        else:
            await robot.set_wheel_speeds(8,8)
        

# start the robot
robot.play()
