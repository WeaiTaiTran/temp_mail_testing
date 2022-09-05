import requests

QUANLITY_CLASSROOM = 400
QUANLITY_ORG = 200
QUANLITY_ORG_CLASSROOM = 200

url = "https://www.1secmail.com/api/v1/"
email = "1zzd9jyudu8g@qiott.com"
user = "1zzd9jyudu8g"
domain = "qiott.com"
mail_id = "5664249"
created_account = "?action=genRandomMailbox&count=200"
login_account = f"?action=getMessages&login={user}&domain={domain}"
check_mail = f"?action=readMessage&login={user}&domain={domain}&id={mail_id}"
api = f"{url}{check_mail}"
response = requests.get(url=api)

print(response.json())