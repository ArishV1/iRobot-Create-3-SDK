import math as m

def getCorrectionAngle(heading):
    actualAngle = 90 - heading
    if actualAngle <= 0 and actualAngle >= -90:
        correctionAngle = int(actualAngle) * -1
    elif actualAngle < -90 and actualAngle >= -180:
        correctionAngle = int(actualAngle) * -1
    elif actualAngle > 0 and actualAngle <= 90:
        correctionAngle = int(actualAngle) * -1
    else:
        correctionAngle = int(actualAngle) * -1
    return correctionAngle

"""
print(getCorrectionAngle(135.6))
print(getCorrectionAngle(25))
"""

def getAngleToDestination(current_position,destination):
    x = current_position.x
    y = current_position.y
    xFinal, yFinal = destination
    radianAngle = m.atan2(xFinal - x, yFinal - y)
    degreeAngle = m.degrees(radianAngle)
    return int(degreeAngle)

"""
currentPosition = (1, 1)
destination = (5, 3)
print(getAngleToDestination(currentPosition, destination))

currentPosition = (5, 5)
destination = (1, 1)
print(getAngleToDestination(currentPosition, destination))
"""


def getMinProxApproachAngle(readings, angles):
    minProximity = 10000000
    minAngle = 0
    for reading in readings:
        proximity = 4095/(reading + 1)
        if proximity < minProximity:
            minProximity = proximity
            x = readings.index(reading)
            minAngle = angles[x]
    return (minProximity, minAngle)


"""
IR_ANGLES = [-65.3, -38.0, -20.0, -3.0, 14.25, 34.0, 65.3]
readings = [4, 347, 440, 408, 205, 53, 27]
print(getMinProxApproachAngle(readings, IR_ANGLES))

IR_ANGLES = [-65.3, -38.0, -20.0, -3.0, 14.25, 34.0, 65.3]
readings = [731, 237, 202, 229, 86, 120, 70]
print(getMinProxApproachAngle(readings, IR_ANGLES))
"""


def checkPositionArrived(current_position, destination, threshold):
    deltax = destination[0] - current_position[0]
    deltay = destination[1] - current_position[1]
    distance = m.sqrt((m.pow(deltax, 2) + m.pow(deltay, 2)))
    return distance <= threshold

"""
print(checkPositionArrived((97, 99), (100, 100), 5.0))
print(checkPositionArrived((50, 50), (45, 55), 5))
"""
