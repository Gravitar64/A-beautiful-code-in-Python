import requests
import json
import ssl, smtplib
from email.mime.text import MIMEText
import EMail_credentials as cred 

URL = "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_Landkreisdaten/FeatureServer/0/query?where=GEN%20%3D%20'CELLE'%20OR%20GEN%20%3D%20'NORDFRIESLAND'OR%20GEN%20%3D%20'FLENSBURG'&outFields=GEN,last_update,cases7_per_100k&returnGeometry=false&outSR=&f=json"

inzidenzen = requests.get(URL).json()
last_update = inzidenzen['features'][0]['attributes']['last_update']
email_text = '7-Tage-Inzidenzen je 100.000 Einwohner\n\n'
for inzidenz in inzidenzen['features']:
  landkreis = inzidenz['attributes']['GEN']
  inzidenz = inzidenz['attributes']['cases7_per_100k']
  email_text += f'Landkreis {landkreis:<20} {inzidenz:>5.1f}\n'

with smtplib.SMTP(host='smtp.web.de',port=587) as server:
  server.starttls(context=ssl.create_default_context())
  server.login(cred.FROM, cred.PASSWORD)
  msg = MIMEText(email_text)
  msg["From"] = cred.FROM
  msg["To"] = cred.TO
  msg["Subject"] = f'Inzidenzen vom {last_update}'
  server.sendmail(cred.FROM, cred.TO, msg.as_string())

 