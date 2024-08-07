import requests
from twilio.rest import Client
import Teil_52_Twilio_credentials as cred 

URL = "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_Landkreisdaten/FeatureServer/0/query?where=GEN%20%3D%20'NORDFRIESLAND'%20OR%20GEN%20%3D%20'FLENSBURG'%20OR%20GEN%20%3D%20'REGION%20HANNOVER'%20OR%20GEN%20%3D%20'CELLE'&outFields=cases7_per_100k_txt,GEN,last_update&returnGeometry=false&orderByFields=GEN ASC&outSR=&f=json"

inzidenzen = requests.get(URL).json()
last_update = inzidenzen['features'][0]['attributes']['last_update']
whatsapp = f'Stand: {last_update}\n\n'
for inzidenz in inzidenzen['features']:
  landkreis = inzidenz['attributes']['GEN']
  inz = inzidenz['attributes']['cases7_per_100k_txt']
  whatsapp += f'{inz}\t {landkreis}\n'

client = Client(cred.ACCOUNT_SID, cred.AUTH_TOKEN)
client.messages.create(body=whatsapp, from_= cred.FROM, to=cred.TO)