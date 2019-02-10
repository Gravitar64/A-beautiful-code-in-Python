import pygame as pg
import math
import arrow
import googlemaps
import requests
from google_maps_places_credentials import API_Key
from astral import Astral 
LOCATION = 'Berlin'

a = Astral()
a.solar_depression = 'astronomical'
city = a[LOCATION]
print(LOCATION, city.region, city.timezone) 
sun = city.sun(date=arrow.now(), local=True)
print (sun)

sonnenstand = ['astronomical_twilight_begin', 'nautical_twilight_begin',
               'civil_twilight_begin', 'sunrise', 'sunset',
               'civil_twilight_end', 'nautical_twilight_end', 'astronomical_twilight_end']
helligkeit = [10, 20, 30, 80, 30, 20, 10]

gmaps = googlemaps.Client(key=API_Key)
geocode_result = gmaps.geocode(LOCATION)
lat, lng = geocode_result[0]['geometry']['location'].values()
timezone = gmaps.timezone((lat, lng))['timeZoneId']

data = requests.get(
    f'https://api.sunrise-sunset.org/json?lat={lat}&lng={lng}&date=today&formatted=0')
data = data.json()
print(data)
zeiten = []
for s in sonnenstand:
  time = arrow.get(data['results'][s])
  time = time.to(timezone)
  zeiten.append(time.time())

pg.init()
w = 1000
screen = pg.display.set_mode([w, w])
center = (w//2, w//2)
farbe = pg.Color(0)

flaechen = []
for i in range(0, len(zeiten)-1):
  up = zeiten[i].hour+zeiten[i].minute/60
  down = zeiten[i+1].hour+zeiten[i+1].minute/60
  if up > down:
    down += 24
  startWinkel = int((360 / 24) * up + (360 / 4))
  endWinkel = int((360 / 24) * down + (360 / 4))
  pointList = [center]
  for p in range(startWinkel, endWinkel):
    winkel = math.radians(p)
    x = int(center[0]+w*0.39*math.cos(winkel))
    y = int(center[0]+w*0.39*math.sin(winkel))
    pointList.append((x, y))
  pointList.append(center)
  flaechen.append(pointList)


weitermachen = True
clock = pg.time.Clock()
while weitermachen:
  screen.fill((0, 0, 0))
  clock.tick(10)
  for event in pg.event.get():
    if event.type == pg.QUIT:
      weitermachen = False

  # Dämmerungszonen zeichnen
  for i, pl in enumerate(flaechen):
    farbe.hsva = (60, 100, helligkeit[i])
    pg.draw.polygon(screen, farbe, pl, 0)

  pg.draw.circle(screen, 255, center, int(w * 0.4), 5)

  # Stunden zeichnen
  for s in range(0, 24, 1):
    winkel = (2*math.pi / 24) * s + (2*math.pi / 4)
    x = int(center[0]+w*0.45*math.cos(winkel))
    y = int(center[0]+w*0.45*math.sin(winkel))
    textsurface = pg.font.SysFont('impact', 40).render(
        f'{s}', False, (255, 255, 255))
    screen.blit(textsurface, (x - textsurface.get_width() //
                              2, y - textsurface.get_height() // 2))

  # Minuten zeichnen
  for s in range(0, 60, 5):
    winkel = (2*math.pi / 60) * s - (2*math.pi / 4)
    x = int(center[0]+w*0.35*math.cos(winkel))
    y = int(center[0]+w*0.35*math.sin(winkel))
    textsurface = pg.font.SysFont('impact', 20).render(
        f'{s}', False, (50, 50, 50))
    screen.blit(textsurface, (x - textsurface.get_width() //
                              2, y - textsurface.get_height() // 2))

  d = arrow.utcnow()
  d = d.to(timezone)
  h = d.hour
  m = d.minute
  s = d.second

  # Stundenzeiger
  h = h + m / 60
  winkel = winkel = (2*math.pi / 24) * h + (2*math.pi / 4)
  x = int(center[0]+w*0.2*math.cos(winkel))
  y = int(center[0]+w*0.2*math.sin(winkel))
  pg.draw.line(screen, (255, 255, 255), center, (x, y), 20)

  # Minutenzeiger
  m = m + s / 60
  winkel = winkel = (2*math.pi / 60) * m - (2*math.pi / 4)
  x = int(center[0]+w*0.3*math.cos(winkel))
  y = int(center[0]+w*0.3*math.sin(winkel))
  pg.draw.line(screen, (255, 255, 255), center, (x, y), 10)

  # Sekundenzeiger
  winkel = winkel = (2*math.pi / 60) * s - (2*math.pi / 4)
  x = int(center[0]+w*0.4*math.cos(winkel))
  y = int(center[0]+w*0.4*math.sin(winkel))
  pg.draw.line(screen, (255, 0, 0), center, (x, y), 2)

  pg.display.flip()


pg.quit()
