from enum import Enum
from time import sleep
import time
import sqlite
import temp_mail
import graphQL
import unittest
from cryptohash import sha1


LIMIT = 200
TIME = 10

class MAIL_TYPE(Enum):
    MAIL_INVITE_NOT_ACCOUNT = 1
    MAIL_INVITE_ORG_NOT_ACCOUNT = 2
    MAIL_INVITE_HAVE_ACCOUNT = 3
    MAIL_INVITE_ORG_HAVE_ACCOUNT = 4

class Identify(Enum):
    classRoomID = 499
    subjectID = 48
    classRomIDOrg = 213
    
class Role(Enum):
    STUDENT = "STUDENT"
    ADMIN = "ADMIN"
    TEACHER = "TEACHER"
    
class ORG(Enum):
    ACTIVE = 1
    DEACTIVE = 0

STATE_TOKEN = sha1(f"Testing Mail : {time.time()}")
print(STATE_TOKEN)

sqlite.createLog({
    "stateToken": STATE_TOKEN
})

def importProfile(type, amount, org):
    listMail = temp_mail.create_mail(amount)
    print(listMail)
    for mail in listMail:
        account, domain = temp_mail.excute_mail(mail)
        data = {
            "email" : mail,
            "account": account,
            "domain": domain,
            "type": type,
            "org": org,
            "stateToken": STATE_TOKEN
        }
        sqlite.createMailProfile(data)
    print({
        "status": 200
    })
    return listMail

def importLetter(type):
    listProfile = sqlite.cursor.execute(f"SELECT token, account, domain FROM profile WHERE type={type} and state_token='{STATE_TOKEN}'").fetchall()
    for profile in listProfile:
        if type == MAIL_TYPE.MAIL_INVITE_NOT_ACCOUNT :
            sqlite.cursor.execute(f"UPDATE profile SET type={MAIL_TYPE.MAIL_INVITE_HAVE_ACCOUNT.value}")
        elif type == MAIL_TYPE.MAIL_INVITE_ORG_NOT_ACCOUNT:
            sqlite.cursor.execute(f"UPDATE profile SET type={MAIL_TYPE.MAIL_INVITE_ORG_HAVE_ACCOUNT.value}")
        sqlite.connectSql.commit()
        
        token, account, domain = profile
        inbox = temp_mail.get_mail_box_id(account=account, domain=domain)
        for mail in inbox:
            # if mail['subject'] == "testing":
            letterDetail = temp_mail.access_mail_box(account=account, domain=domain, mail_box=mail['id'])
            data = {
                "id": mail['id'],
                "from": mail['from'],
                "subject": mail['subject'],
                "date": mail['date'],
                "body": letterDetail['body'],
                "textBody": letterDetail['textBody'],
                "htmlBody": letterDetail['htmlBody'],
                "stateToken": STATE_TOKEN
            }
            sqlite.importMailLetter(letter=data, emailToken=token)
            # print(f"Letter Detail: {letterDetail}")
        print(f"Mail Box - {account}: {inbox}")
    return 200

class TestingMail(unittest.TestCase):
    
    def test_invite_classroom(self):
        amount = 1
        listMail = importProfile(MAIL_TYPE.MAIL_INVITE_NOT_ACCOUNT.value, amount, ORG.DEACTIVE.value)
        graphQL.SendMail(Identify.classRoomID.value, listMail)
        sleep(TIME)
        importLetter(MAIL_TYPE.MAIL_INVITE_NOT_ACCOUNT.value)
        eduplaxCount = sqlite.cursorMailBox.execute(f"SELECT * FROM mail_box WHERE subject='eduplaX - Lời mời tham gia lớp học.' and state_token='{STATE_TOKEN}'").fetchall()
        eduplaxCount2 = sqlite.cursorMailBox.execute("SELECT * FROM mail_box WHERE subject='eduplaX - Chào mừng đến với lớp học.'and state_token='{STATE_TOKEN}'").fetchall()
        print(f"Mail mời tham gia lớp học {len(eduplaxCount)}/{amount}")
        print(f"Chào mừng đến với lớp học. {len(eduplaxCount2)}/{amount}")
        self.assertEqual(amount, len(eduplaxCount))
        self.assertEqual(amount, len(eduplaxCount2))
    
    def test_invite_org(self):
        amount = 1
        stateToken = STATE_TOKEN
        listMail = importProfile(MAIL_TYPE.MAIL_INVITE_ORG_NOT_ACCOUNT.value, amount, ORG.ACTIVE.value)
        graphQL.addOrganizationUsers(listMail)
        sleep(TIME)
        importLetter(MAIL_TYPE.MAIL_INVITE_ORG_NOT_ACCOUNT.value)
        eduplaxCount = sqlite.cursorMailBox.execute("SELECT * FROM mail_box WHERE subject='eduplaX - Lời mời tham gia trường học.' and state_token='{stateToken}'").fetchall()
        print(f"eduplaX - Lời mời tham gia trường học. {len(eduplaxCount)}/{amount}")
        self.assertEqual(amount, len(eduplaxCount))
    
    def test_invite_org_classroom(self):
        amount = 1
        stateToken = STATE_TOKEN
        listMail = sqlite.cursorMailBox.execute(f"SELECT email FROM mail_box WHERE type={MAIL_TYPE.MAIL_INVITE_ORG_HAVE_ACCOUNT.value} and state_token='{stateToken}' LIMIT {amount}")
        graphQL.SendMailOrg(Identify.classRomIDOrg.value,Role.STUDENT.value,  listMail)
        sleep(TIME)
        importLetter(MAIL_TYPE.MAIL_INVITE_ORG_NOT_ACCOUNT.value)
        eduplaxCount = sqlite.cursorMailBox.execute("SELECT * FROM mail_box WHERE subject='eduplaX - Lời mời tham gia lớp học.' and state_token='{stateToken}'").fetchall()
        print(f"Mail mời tham gia lớp học {len(eduplaxCount)}/{amount}")
        self.assertEqual(amount, len(eduplaxCount))
        
    def test_add_subject_permissons(self):
        amount = 1
        stateToken = STATE_TOKEN
        listMail = sqlite.cursorMailBox.execute(f"SELECT email FROM mail_box WHERE type={MAIL_TYPE.MAIL_INVITE_ORG_HAVE_ACCOUNT.value} and state_token='{stateToken}' LIMIT {amount}")
        graphQL.addSubjectPermissions(listMail, Identify.subjectID.value)
        sleep(TIME)
        importLetter(MAIL_TYPE.MAIL_INVITE_HAVE_ACCOUNT.value)
        
# importLetter(MAIL_TYPE.MAIL_INVITE_CLASSROOM_NOT_ACCOUNT.value)
