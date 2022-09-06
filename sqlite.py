import sqlite3
import os
import time
import datetime
from cryptohash import sha1


DATA = "./data"

if not os.path.exists(DATA):
    os.mkdir(DATA)
    print(f"Created {DATA}")

profilePath = f"{DATA}/profile_mail.db"
mainBoxPath = f"{DATA}/mail_box.db"
testLog = f"{DATA}/test_log.db"

connectSql = sqlite3.connect(profilePath)
cursor = connectSql.cursor()

try :
    res = cursor.execute("SELECT * FROM profile")
except : 
    cursor.execute("CREATE TABLE profile(id INTEGER PRIMARY KEY, token, email, account, domain, type, date_created)")
    print("Created Mail Profile")
    
connectSqlMailBox = sqlite3.connect(mainBoxPath)
cursorMailBox = connectSqlMailBox.cursor()

try : 
    resMailBox = cursorMailBox.execute("SELECT * FROM mail_box")
except :
    cursorMailBox.execute("CREATE TABLE mail_box(id, email_token, send_from, subject, date, attachments, body, textBody, htmlBody)")
    print("Created Mail Box")
    
connectSqlTestLog = sqlite3.connect(testLog)
cursorTestLog = connectSqlTestLog.cursor()

try : 
    resTestLog = cursorTestLog.execute("SELECT * FROM test_log")
except :
    cursorTestLog.execute("CREATE TABLE test_log(id INTEGER PRIMARY KEY, date_created, log)")
    print("Created Test Log")

def createMailProfile(profile):
    dateCreate = createTimeStamp()
    token = sha1(f"{profile['email']}{profile['type']}{dateCreate}")
    
    emailValid = cursor.execute(f"SELECT * FROM profile WHERE email='{profile['email']}'").fetchall()
    if len(emailValid) > 0:
        print("Email Valid in Database")
    else:
        cursor.execute("INSERT INTO profile(token, email, account, domain, type, date_created) VALUES(?, ?, ?, ?, ?, ?)", (token, profile['email'], profile['account'], profile['domain'], profile['type'], dateCreate))
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
    idValid = cursorMailBox.execute(f"SELECT * FROM mail_box WHERE id='{letter['id']}'").fetchall()
    if len(idValid) > 0:
        print("Letter Valid In Database")
    else :
        cursorMailBox.execute("INSERT INTO mail_box(id, email_token, send_from, subject, date, attachments, body, textBody, htmlBody) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", (letter['id'], emailToken, letter['from'], letter['subject'], createTimeStamp(letter['date']), letter['attachments'], letter['body'], letter['textBody'], letter['htmlBody']))
        connectSqlMailBox.commit()
    res = cursorMailBox.execute(f"SELECT * FROM mail_box WHERE id={letter['id']}").fetchall()
    print(res)
    
def queryDB(type):
    if type == 1:
        return cursor.execute("SELECT * FROM profile").fetchall()
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

print(queryDB(2))