import plotly.express as px
import requests

e = requests.get('http://api.open-notify.org/iss-now.json').json()
lati = float(e['iss_position']['latitude'])
long = float(e['iss_position']['longitude'])
map = px.scatter_geo(lat=[lati], lon=[long], size=[20])
map.show()