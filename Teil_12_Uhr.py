import pygame as pg, math, arrow, googlemaps, requests
from google_maps_places_credentials import *

locations = 'Nienhagen bei Celle,Sheffield UK,Jerez de la Frontera,Moskau,Las Vegas,Baranquilla,Chicago,Sydney,Wellington'.split(',')

sonnenstand = ['astronomical_twilight_begin', 'nautical_twilight_begin',
               'civil_twilight_begin', 'sunrise', 'sunset',
               'civil_twilight_end', 'nautical_twilight_end', 'astronomical_twilight_end']
helligkeit = [5, 10, 15, 30, 15, 10, 5]
temperatur = 0
wind = 0

def rotate(surface, angle, pivot, offset):
    """Rotate the surface around the pivot point.

    Args:
        surface (pygame.Surface): The surface that is to be rotated.
        angle (float): Rotate by this angle.
        pivot (tuple, list, pygame.math.Vector2): The pivot point.
        offset (pygame.math.Vector2): This vector is added to the pivot.
    """
    rotated_image = pg.transform.rotozoom(surface, -angle, 1)  # Rotate the image.
    rotated_offset = offset.rotate(angle)  # Rotate the offset vector.
    # Add the offset vector to the center/pivot point to shift the rect.
    rect = rotated_image.get_rect(center=pivot+rotated_offset)
    return rotated_image, rect  # Return the rotated image and shifted rect.


def changeOrt(location):
  #hole die Geo-Koordinaten und die Timezone zum Ort (LOCATION) von Google 
  gmaps = googlemaps.Client(key=API_Key)
  geocode_result = gmaps.geocode(location)
  location = geocode_result[0]['address_components'][0]['long_name']
  lat, lng = geocode_result[0]['geometry']['location'].values()
  timezone = gmaps.timezone((lat, lng))['timeZoneId']

  #hole die Sonnenauf-/untergangszeiten zu den Geo-Koordinaten von 
  #sunrise-sunset.org und speicher die Uhrzeiten unter zeiten
  d = arrow.now().to(timezone)
  datum = d.format('YYYY-MM-DD')
  data = requests.get(
      f'https://api.sunrise-sunset.org/json?lat={lat}&lng={lng}&date={datum}&formatted=0')
  data = data.json()
  zeiten = []
  for s in sonnenstand:
    time = arrow.get(data['results'][s])
    time = time.to(timezone)
    zeiten.append(time.time())

  sunrise = arrow.get(data['results']['sunrise']).to(timezone)
  sunset = arrow.get(data['results']['sunset']).to(timezone)
  print(sunrise.format('HH:mm:ss'), sunset.format('HH:mm:ss'))
  return zeiten, location, timezone

zeiten, location, timezone = changeOrt(locations[0])

#hole die aktuelle Temperatur
def wetterDatenHolen(location):
  weather = requests.get(f'https://api.apixu.com/v1/current.json?key={Weather_Key}&q={location}')
  weather = weather.json()
  temp = weather['current']['temp_c']
  wind = str(weather['current']['wind_kph'])
  wind += ' km/h  '+weather['current']['wind_dir']
  return temp, wind



#pygame wird vorbereitet
pg.init()
w = 1200
r = w // 2
screen = pg.display.set_mode([w, w])
center = (r, r)
farbe = pg.Color(0)
pic_uhr = pg.transform.scale(pg.image.load('Uhr_v2.png'), (w,w))
pic_stunde = pg.transform.scale(pg.image.load('Stundenzeiger_v2.png'), (23, int(r*0.45)))
pic_minute = pg.transform.scale(pg.image.load('Minutenzeiger_v2.png'), (15, int(r*0.7)))
pic_kone = pg.transform.scale(pg.image.load('kone_v2.png'), (60,60))



#für die Dämmerungsstufen werden flächen(polygone) vorbereitet
def flächenBerechnen(zeiten):
  flaechen = []
  for i in range(0, len(zeiten)-1):
    up = zeiten[i].hour+zeiten[i].minute/60
    down = zeiten[i+1].hour+zeiten[i+1].minute/60
    if up > down:
      down += 24
    startWinkel = (360 / 24) * up + (360 / 4)
    endWinkel = (360 / 24) * down + (360 / 4)
    
    pointList = [center]
    while startWinkel < endWinkel:
      winkel = math.radians(startWinkel)
      x = int(center[0]+r*0.9*math.cos(winkel))
      y = int(center[0]+r*0.9*math.sin(winkel))
      pointList.append((x, y))
      startWinkel += 0.01
    pointList.append(center)
    flaechen.append(pointList)
  return flaechen

#hier wird endlos das Bild neu aufgebaut mit fps = clock.tick()
d = arrow.now().to(timezone)
flaechen = flächenBerechnen(zeiten)
temperatur, wind = wetterDatenHolen(location)
lastMinute = d.minute
weitermachen = True
clock = pg.time.Clock()
startOrt = 0
while weitermachen:
  d = arrow.now().to(timezone)
  if d.minute != lastMinute:
    lastMinute = d.minute
    startOrt = (startOrt +1)  % len(locations)
    zeiten, location, timezone = changeOrt(locations[startOrt])
    flaechen = flächenBerechnen(zeiten)
    d = arrow.now().to(timezone)
    temperatur, wind = wetterDatenHolen(location)
  datum = d.format('DD.MM.YYYY')
  screen.fill((0, 0, 0))
  clock.tick(1)
  #wenn das Fenster geschlossen wird, wird die while-Schleife verlassen
  for event in pg.event.get():
    if event.type == pg.QUIT:
      weitermachen = False

  # vorbereitete Flächen für die Dämmerungsstufen zeichnen
  for i, pl in enumerate(flaechen):
    farbe.hsva = (60, 20, helligkeit[i])
    pg.draw.polygon(screen, farbe, pl, 0)

  screen.blit(pic_uhr, (0,0))
  
  # Ort, Datum, Temperatur und Wind zeichnen
  textsurface = pg.font.SysFont('impact', 48).render(
        f'{location}', False, (188,203,224))
  screen.blit(textsurface, (center[0] - textsurface.get_width() // 2, center[1]-r*0.6))
  
  textsurface = pg.font.SysFont('impact', 32).render(
        f'{datum}', False, (188,203,224))
  screen.blit(textsurface, (center[0] - textsurface.get_width() // 2, 
  center[1]+r*0.10+textsurface.get_height()))

  textsurface = pg.font.SysFont('impact', 24).render(
        f'{temperatur} °C', False, (188,203,224))
  screen.blit(textsurface, (center[0] - textsurface.get_width() // 2, 
  center[1]+r*0.45+textsurface.get_height()))

  textsurface = pg.font.SysFont('impact', 24).render(
        f'{wind}', False, (188,203,224))
  screen.blit(textsurface, (center[0] - textsurface.get_width() // 2, 
  center[1]+r*0.5+textsurface.get_height()))

  offset = pg.math.Vector2(1,pic_stunde.get_height()*0.37)
  rotated_image, rect = rotate(pic_stunde, 360/24*(d.hour+d.minute/60), center, offset)
  screen.blit(rotated_image, rect)
  
  offset = pg.math.Vector2(1,pic_minute.get_height()*0.43)
  rotated_image, rect = rotate(pic_minute, 360/60*d.minute+180, center, offset)
  screen.blit(rotated_image, rect)
  
  screen.blit(pic_kone, (center[0]-pic_kone.get_width()//2, center[1]-pic_kone.get_height()//2))
  
  pg.display.flip()


pg.quit()
