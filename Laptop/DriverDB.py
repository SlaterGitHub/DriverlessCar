import MySQLdb
from Connection2 import deform, reform

host = "dbrysl.ccwooq5jrcka.eu-west-2.rds.amazonaws.com"
user = "rysl"
password = "HomeOfBaseData19"
dbName = "rysl_general_db"

db = MySQLdb.connect(host = host,
                        user = user,
                        passwd = password,
                        db = dbName)

cur = db.cursor()

def getAll():
    cur.execute("SELECT * FROM Drives")
    entries = getData(cur)
    return entries

def upload(runTime, lastDistance, lastSpeed, fail, frame):
    PK = int(cur.execute("SELECT carID FROM Drives"))
    frame = deform(frame)
    try:
        cur.execute("INSERT INTO Drives VALUES (%s, %s, %s, %s, %s, %s)", (PK, int(runTime), int(lastDistance), int(lastSpeed), frame, int(fail)))
        db.commit()
    except:
        db.rollback()

def getFoS(fail):
    cur.execute("SELECT * FROM Drives WHERE fail = %s", (int(fail)))
    entries = getData(cur)
    return entries

def getData(cur):
    entries = []
    for (x) in cur:
        x = list(x)
        x[4] = reform(x[4], 3, 320, 240)
        entries.append(x)
    print("done")
    return entries
