import email
from subprocess import call
from time import sleep
from webbrowser import get
import requests

KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.IntcImRhdGFcIjp7XCJkb21haW5cIjpcImdtYWlsLmNvbVwiLFwidXNlcm5hbWVcIjpcInJhbmRvbVwiLFwic2VydmVyXCI6XCJzZXJ2ZXItMVwiLFwidHlwZVwiOlwiYWxpYXNcIn0sXCJjcmVhdGVkX2F0XCI6MTY2NzM4NTM2N30i.IotcXOXEi6dqnQiOrG0MT3S9AJkMIZDC-nxIoDHEwgk"
RAPIAPI_KEY = "f871a22852mshc3ccc49e34af1e8p126682jsn734696f1f081"
API = f"https://public-sonjj.p.rapidapi.com/email/gm/get?key={KEY}&rapidapi-key={RAPIAPI_KEY}&username=random&domain=gmail.com&server=server-1&type=alias"
API_TWO = "https://smailpro.com/app/key"
MAX_ITEMS = 100

dataAPITWO = {
  "domain": "gmail.com",
  "username": "random",
  "server": "server-1",
  "type": "alias"
}
listMail = [1]

def GET_MAIL(): 
    dataJson = requests.get(url = API).json()
    email = dataJson['items']['email']
    if dataJson['code'] == 200:
        return email
    else : 
        KEY = GET_KEY()
        GET_MAIL()

def GET_KEY():
    dataJson = requests.get(url = API_TWO, data=dataAPITWO).json()
    key = dataJson['items']
    if dataJson['code'] == 200:
        return key
    else : 
        raise(f"Error : {dataJson['code']}")

while listMail.count(int) < MAX_ITEMS :
        getMail = GET_MAIL()
        print(f"Mail Created : {getMail}")
        listMail.append(getMail)
        print(listMail.count(int))

# print(listMail.count(int))
# with open('readme.txt', 'w') as f:
#     f.write(f"{listMail}")