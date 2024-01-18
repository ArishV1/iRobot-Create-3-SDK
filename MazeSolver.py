from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

import AuxMazeSolver as aux

bumper = False

# === CREATE ROBOT OBJECT
robot = Create3(Bluetooth("AVA"))

# === FLAG VARIABLES
HAS_COLLIDED = False
HAS_ARRIVED = False

# === BUILD MAZE DICTIONARY
N_X_CELLS = 3
N_Y_CELLS = 3
CELL_DIM = 50
MAZE_DICT = aux.createMazeDict(N_X_CELLS, N_Y_CELLS, CELL_DIM)
MAZE_DICT = aux.addAllNeighbors(MAZE_DICT, N_Y_CELLS, N_Y_CELLS)

# === DEFINING ORIGIN AND DESTINATION
PREV_CELL = None
START = (0,0)
CURR_CELL = START
DESTINATION = (2,0)
MAZE_DICT[CURR_CELL]["visited"] = True

# === PROXIMITY TOLERANCES
WALL_THRESHOLD = 120


# ==========================================================
# FAIL SAFE MECHANISMS

# EITHER BUTTON
@event(robot.when_touched, [True, True])  # User buttons: [(.), (..)]
async def when_either_button_touched(robot):
    global bumper
    await robot.set_wheel_speeds(0, 0)
    await robot.set_lights(Robot.LIGHT_ON, Color(255, 0, 0))
    bumper = True


# EITHER BUMPER
@event(robot.when_bumped, [True, True])  # [left, right]
async def when_either_bumped(robot):
    global bumper
    await robot.set_wheel_speeds(0, 0)
    await robot.set_lights(Robot.LIGHT_ON, Color(255, 0, 0))
    bumper = True


# ==========================================================
# MAZE NAVIGATION AND EXPLORATION

# === NAVIGATE TO CELL

async def navigateToNextCell(robot, next_move, orientation):
    global MAZE_DICT, PREV_CELL, CURR_CELL, CELL_DIM

    potential_neighbors=aux.getPotentialNeighbors(CURR_CELL, orientation)
    print(potential_neighbors)

    if next_move==potential_neighbors[0]:
        await robot.turn_left(90)
    if next_move==potential_neighbors[1]:
        pass
    if next_move==potential_neighbors[2]:
        await robot.turn_right(90)
    if next_move==potential_neighbors[3]:
        await robot.turn_left(180)

    await robot.move(CELL_DIM)

    MAZE_DICT[CURR_CELL]['visited']=True
    PREV_CELL=CURR_CELL
    CURR_CELL=(next_move[0], next_move[1])



# === EXPLORE MAZE
@event(robot.when_play)
async def navigateMaze(robot):
    global HAS_COLLIDED, HAS_ARRIVED
    global PREV_CELL, CURR_CELL, START, DESTINATION
    global MAZE_DICT, N_X_CELLS, N_Y_CELLS, CELL_DIM, WALL_THRESHOLD

    while not HAS_COLLIDED and not HAS_ARRIVED:
        
        pose = (await robot.get_position())

        
        if pose is not None:
            
            heading = pose.heading

            
            print("x = {}, y = {}, theta = {}".format(pose.x, pose.y, heading))

            
            await robot.wait(1)

            
            if aux.checkCellArrived(CURR_CELL, DESTINATION):
                HAS_ARRIVED = True
                await robot.set_wheel_speeds(0, 0)
                await robot.set_lights(Robot.LIGHT_ON, Color(0, 255, 0))
                break

            
            orientation = aux.getRobotOrientation(heading)
            potential_neighbors = aux.getPotentialNeighbors(CURR_CELL, orientation)

            
            sensor_readings = (await robot.get_ir_proximity()).sensors  
            walls_around_cell = aux.getWallConfiguration(sensor_readings[0], sensor_readings[3], sensor_readings[6], WALL_THRESHOLD)
            print("walls_around_cell", walls_around_cell)
           
            navigable_neighbors = aux.getNavigableNeighbors(walls_around_cell, potential_neighbors, PREV_CELL, N_X_CELLS, N_Y_CELLS)
            print("navigable_neighbors",navigable_neighbors)
            
            MAZE_DICT = aux.updateMazeNeighbors(MAZE_DICT, CURR_CELL, navigable_neighbors)
            MAZE_DICT = aux.updateMazeCost(MAZE_DICT, START, DESTINATION)

            
            next_move = aux.getNextCell(MAZE_DICT, CURR_CELL)
            print("next move", next_move)
            
            await navigateToNextCell(robot, next_move, orientation)

        if bumper == True:
            await robot.set_wheel_speeds(0, 0)

    
    await robot.set_wheel_speeds(0, 0)
    await robot.set_lights(Robot.LIGHT_ON, Color(0, 255, 0))




# start the robot
robot.play()
