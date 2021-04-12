import requests, json
from twilio.rest import Client
import Twilio_credentials as cred


URL = "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_Landkreisdaten/FeatureServer/0/query?where=%20GEN%20%3D%20'NORDFRIESLAND'OR%20GEN%20%3D%20'FLENSBURG'&outFields=GENGEN%20%3D%20'HANNOVER'%20ORGEN%20%3D%20'CELLE'%20,last_update,cases7_per_100k_txt&returnGeometry=false&outSR=&f=json"

inzidenzen = requests.get(URL).json()
last_update = inzidenzen['features'][0]['attributes']['last_update']

whats_app_text = f'Stand: {last_update}\n\n'
for inzidenz in inzidenzen['features']:
  landkreis = inzidenz['attributes']['GEN']
  inzidenz = inzidenz['attributes']['cases7_per_100k_txt']
  whats_app_text += f'{inzidenz}\t {landkreis}\n'

client = Client(cred.ACCOUNT_SID, cred.AUTH_TOKEN)
client.messages.create(body=whats_app_text, from_=cred.FROM, to=cred.TO)