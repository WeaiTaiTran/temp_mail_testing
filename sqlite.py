import sqlite3
import os
import time
import datetime
from cryptohash import sha1


DATA = "./data"
TEMP_PATH = f"{DATA}/{time.time()}"
if not os.path.exists(DATA):
    os.mkdir(DATA)
    print(f"Created {DATA}")

# if not os.path.exists(TEMP_PATH):
#     os.mkdir(TEMP_PATH)
#     print("Created Temp Path")

profilePath = f"{DATA}/profile_mail.db"
mainBoxPath = f"{DATA}/mail_box.db"
testLog = f"{DATA}/test_log.db"

connectSql = sqlite3.connect(profilePath)
cursor = connectSql.cursor()

try :
    res = cursor.execute("SELECT * FROM profile")
except : 
    cursor.execute("CREATE TABLE profile(id INTEGER PRIMARY KEY, state_token, token, email, account, domain, type, org, date_created)")
    print("Created Mail Profile")
    
connectSqlMailBox = sqlite3.connect(mainBoxPath)
cursorMailBox = connectSqlMailBox.cursor()

try : 
    resMailBox = cursorMailBox.execute("SELECT * FROM mail_box")
except :
    cursorMailBox.execute("CREATE TABLE mail_box(id, state_token, email_token, send_from, subject, date, attachments, body, textBody, htmlBody)")
    print("Created Mail Box")
    
connectSqlTestLog = sqlite3.connect(testLog)
cursorTestLog = connectSqlTestLog.cursor()

try : 
    resTestLog = cursorTestLog.execute("SELECT * FROM test_log")
except :
    cursorTestLog.execute("CREATE TABLE test_log(id INTEGER PRIMARY KEY, state_token, case_runing, date_created, case_invite_classroom, case_invite_classroom_two, case_invite_org, case_invite_org_two, case_invite_classroom_org, case_add_subject_permission)")
    print("Created Test Log")

def updateLog(log):
    cursorTestLog.execute(f"UPDATE test_log SET {log['key']}='{log['value']}' WHERE state_token='{log['stateToken']}'")
    connectSqlTestLog.commit()
    
def createLog(log):
    dateCreate = createTimeStamp()
    cursorTestLog.execute(f"INSERT INTO test_log(state_token, date_created) VALUES(?, ?)", (log['stateToken'], dateCreate))
    connectSqlTestLog.commit()
    res = cursorTestLog.execute(f"SELECT * FROM test_log WHERE state_token='{log['stateToken']}'").fetchall()
    print(res)
    
def createMailProfile(profile):
    dateCreate = createTimeStamp()
    token = sha1(f"{profile['email']}{profile['type']}{dateCreate}")
    
    emailValid = cursor.execute(f"SELECT * FROM profile WHERE email='{profile['email']}'").fetchall()
    if len(emailValid) > 0:
        print("Email Valid in Database")
    else:
        cursor.execute("INSERT INTO profile(token, state_token, email, account, domain, type, org, date_created) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", (token, profile['stateToken'], profile['email'], profile['account'], profile['domain'], profile['type'], profile['org'], dateCreate))
        connectSql.commit()
    res = cursor.execute(f"SELECT * FROM profile WHERE email='{profile['email']}'").fetchall()
    print(res)
    
def createTimeStamp(date = None):
    if date is None:
        timeNow = datetime.datetime.now()
        currentTime = timeNow.strftime("%Y-%m-%d %H:%M:%S")
    else:
        currentTime = date
    timeStamp = time.mktime(datetime.datetime.strptime(currentTime, "%Y-%m-%d %H:%M:%S").timetuple())
    return timeStamp

def importMailLetter(letter, emailToken):
    idValid = cursorMailBox.execute(f"SELECT * FROM mail_box WHERE id={letter['id']}").fetchall()
    if len(idValid) > 0:
        print(f"Letter Valid In Database {letter['id']} - {letter['subject']}")
    else :
        cursorMailBox.execute("INSERT INTO mail_box(id, state_token, email_token, send_from, subject, date, body, textBody, htmlBody) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", (letter['id'], letter['stateToken'],emailToken, letter['from'], letter['subject'], createTimeStamp(letter['date']), letter['body'], letter['textBody'], letter['htmlBody']))
        connectSqlMailBox.commit()
        res = cursorMailBox.execute(f"SELECT * FROM mail_box WHERE id={letter['id']} and state_token='{letter['stateToken']}'").fetchall()
        print(res)

def queryDB(type):
    if type == 1:
        return cursor.execute("SELECT email FROM profile LIMIT 2").fetchall()
    elif type == 2: 
        return cursorMailBox.execute("SELECT * FROM mail_box").fetchall()
    elif type == 3:
        return cursorTestLog.execute("SELECT * FROM test_log").fetchall()
    else:
        return {
            "status": "error type"
        }
# TODO : Find Solution To Test Database

#* TYPE 1 : Created Mail - Invite ClassRoom BY Email
#* TYPE 2 : Created Mail - Invite ORG BY Email
#* TYPE 3 : Affter TYPE 1 and TYPE 2 Done
