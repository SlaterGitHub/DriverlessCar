def getDirection(averageX):
    centered = averageX - 160

    if abs(centered) <= 60:
        direction = "0"
    elif centered < -60:
        direction = "1"
    elif centered > 60:
        direction = "2"
    else:
        direction = "3"
    return direction
