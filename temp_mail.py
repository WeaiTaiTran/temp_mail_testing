import requests
import re
import json

QUANLITY_CLASSROOM = 400
QUANLITY_ORG = 200
QUANLITY_ORG_CLASSROOM = 200

# user = "1zzd9jyudu8g"
# domain = "qiott.com"
# mail_id = "5664249"
# login_account = f"?action=getMessages&login={user}&domain={domain}"
# check_mail = f"?action=readMessage&login={user}&domain={domain}&id={mail_id}"
# # response = requests.get(url=api)
url = "https://www.1secmail.com/api/v1"

def create_mail(amount):
    created_account = "?action=genRandomMailbox&count={amount}"
    api = f"{url}/{created_account}"
    response = requests.get(url=api)
    return response.json()

def excute_mail(mail):
    account = re.search(r'(\w.+)@', mail).group(1)
    domain = re.search(r'@(\w.+)', mail).group(1)
    return account, domain

def get_mail_box_id(account, domain):
    login_account = f"?action=getMessages&login={account}&domain={domain}"
    api = f"{url}/{login_account}"
    response = requests.get(url=api)
    return response.json()

def access_mail_box(account, domain, mail_box):
    mail_box = f"?action=readMessage&login={account}&domain={domain}&id={mail_box}"
    api = f"{url}/{mail_box}"
    response = requests.get(url=api)
    return response.json()


# print(get_mail_box_id("1zzd9jyudu8g", "qiott.com"))
# print(json.dumps(access_mail_box("1zzd9jyudu8g", "qiott.com", 5817139)))
# TODO : Solution - Create Mail -> Excute Mail -> Insert Database -> Call API Add Mail Eduplax Staging -> Get Mail Box ID -> Access Mail Box -> Insert Letter To Database -> Query Database Check Subject -> Query Database Check HTMLbody