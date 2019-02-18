import MySQLdb
from Connection2 import deform, reform

host = "dbrysl.ccwooq5jrcka.eu-west-2.rds.amazonaws.com"
user = "rysl"
password = ""
dbName = "rysl_general_db"

db = MySQLdb.connect(host = host,
                        user = user,
                        passwd = password,
                        db = dbName)

cur = db.cursor()

def getAll():
    entries = []
    cur.execute("SELECT * FROM Drives")
    for (x) in cur:
        x[4] = reform(x[4], 3, 320, 240)
        entries.append(x)
    return entires

def upload(runTime, lastDistance, lastSpeed, fail, frame):
    PK = int(cur.execute("SELECT carID FROM Drives")) - 1
    frame = deform(frame)
    try:
        cur.execute("INSERT INTO Drives VALUES (%s, %s, %s, %s, %s, %s)", (PK, int(runTime), int(lastDistance), int(lastSpeed), frame, int(fail)))
        db.commit()
    except:
        db.rollback()

def getFoS(fail):
    entires = []
    cur.execute("SELECT * FROM Drives WHERE fail = %s", (int(fail)))
    for (x) in cur:
        entries.append(x)
    return entires
