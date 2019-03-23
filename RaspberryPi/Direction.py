def getDirection(averageX):

    if averageX is None:
        return 3
    centered = averageX - 160

    if abs(centered) <= 30:
        return 0
    elif centered < -30:
        return 1
    elif centered > 30:
        return 2
"""Check if averageX is None, if it is then that means there is no road so 3 (stop)
if returned, if not then check if the point is between -60 and 60 if so then
the car must go 0 (forward), if the point is less than -60 then the car must go 1
(left) and if its more than 60 it must go 2 (right)"""
