from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

# robot is the instance of the robot that will allow us to call
# its methods and to define events with the @event decorator.
robot = Create3(Bluetooth("ARISH"))

CORRECT_CODE = "341124"
code=""

# LEFT BUTTON
@event(robot.when_touched, [True, False])  # User buttons: [(.), (..)]
async def when_left_button_touched(robot):
    global code
    code+="1"
    await robot.play_note(Note.C5, 0.20)
    await checkUserCode(robot)


# RIGHT BUTTON
@event(robot.when_touched, [False, True])  # User buttons: [(.), (..)]
async def when_right_button_touched(robot):
    global code
    code+="2"
    await robot.play_note(Note.D5, 0.20)
    await checkUserCode(robot)


# LEFT BUMP
@event(robot.when_bumped, [True, False])  # [left, right]
async def when_left_bumped(robot):
    global code
    code+="3"
    await robot.play_note(Note.E5, 0.20)
    await checkUserCode(robot)


# RIGHT BUMP
@event(robot.when_bumped, [False, True]) # [left, right]
async def when_right_bumped(robot):
    global code
    code+="4"
    await robot.play_note(Note.F5, 0.20)
    await checkUserCode(robot)


async def checkUserCode(robot):
    global code
    if len(code)==len(CORRECT_CODE):
        if code==CORRECT_CODE:
            await robot.set_lights(Robot.LIGHT_BLINK,Color(0,255,0))
            await robot.set_lights(Robot.LIGHT_BLINK,Color(0,0,255))
            await robot.play_note(Note.A5, 2.00)
            await robot.play_note(Note.B3, 2.00)
            await robot.turn_left(20)
            await robot.play_note(Note.B3, 2.00)
            await robot.turn_right(20)
            await robot.play_note(Note.B3, 2.00)
            await robot.arc(Robot.DIR_LEFT, 180, 4)
            await robot.play_note(Note.A5, 2)
            await robot.arc(Robot.DIR_RIGHT, 180, 4)
            await robot.play_note(Note.A5, 2.00)
            code=""
        else:
            await robot.set_lights(Robot.LIGHT_BLINK,Color(255,0,0))
            await robot.play_note(Note.D3, 4.00)
            await robot.play_note(Note.E4, 4.00)
            await robot.play_note(Note.G3, 4.00)
            code=""
        


@event(robot.when_play)
async def play(robot):
    await checkUserCode(robot)


robot.play()
