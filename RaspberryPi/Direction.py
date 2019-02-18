def getDirection(averageX):
    
    if averageX is None:
        return 3
    centered = averageX - 160

    if abs(centered) <= 60:
        return 0
    elif centered < -60:
        return 1
    elif centered > 60:
        return 2
