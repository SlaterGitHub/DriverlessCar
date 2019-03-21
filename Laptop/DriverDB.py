import MySQLdb
from Connection2 import deform, reform
"""import libraries"""

host = "cardb.ccwooq5jrcka.eu-west-2.rds.amazonaws.com"
user = "carrysl"
password = "Monkey12"
dbName = "carinfo"

"""Database details"""

db = MySQLdb.connect(host = host,
                        user = user,
                        passwd = password,
                        db = dbName)
"""Connect to database"""

cur = db.cursor()
"""Create a cursor to interact with database"""

def getAll():
    cur.execute("SELECT * FROM Drives")
    entries = getData(cur)
    return entries
    """Get everything from Drives table and pass it through getData"""

def upload(runTime, lastDistance, lastSpeed, fail, frame):
    PK = int(cur.execute("SELECT carID FROM Drives"))
    frame = deform(frame)
    try:
        cur.execute("INSERT INTO Drives VALUES (%s, %s, %s, %s, %s, %s)", (PK, int(runTime), int(lastDistance), int(lastSpeed), frame, int(fail)))
        db.commit()
    except:
        db.rollback()
    """Upload data to database through cursor and commit data to make sure it
    stays in the database, if it does not upload properly then undo the upload"""

def getFoS(fail):
    cur.execute("SELECT * FROM Drives WHERE fail = %s", (int(fail)))
    entries = getData(cur)
    return entries
    """Get either fail and success drives and pass them through getData"""

def getData(cur):
    entries = []
    for (x) in cur:
        x = list(x)
        x[4] = reform(x[4], 3, 320, 240)
        entries.append(x)
    return entries
    """create an empty list and for every row found in the database convert it
    from a tuple to a list. Get the fourth index and reform it to get a frame
    then add the entire row to the list"""
