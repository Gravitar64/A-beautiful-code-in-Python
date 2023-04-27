import pygame as pg
import pandas as pd
import math


def pol2kart(r, w):
  return r * math.cos(w) + breite/2, r * math.sin(w) + höhe/2


def gen_hintergrund():
  for r in radien:
    pg.draw.circle(fenster, farbe_hintergrund, (breite/2, höhe/2), r, 3)

  radius_text = max(radien)+40
  for i in range(1, 13):
    winkel = math.tau/12*i - math.tau/4
    pos = pol2kart(radius_text, winkel)
    zeichne_text(daten.columns[i], pos, 48, farbe_hintergrund, -math.degrees(math.tau/12*i))
    if i != 12: continue
    for i, r in enumerate(radien):
      pos = pol2kart(r-15, winkel)
      zeichne_text(f'{i-1} °C', pos, 28, farbe_hintergrund)




def zeichne_text(text, pos, größe, farbe, rotation=0,hg=False):
  t = pg.font.SysFont('arial', größe).render(text, True, farbe)
  t = pg.transform.rotate(t, rotation)
  t_rect = t.get_rect(center=pos)
  if hg: pg.draw.rect(fenster,'black',t_rect)
  fenster.blit(t, t_rect)


def lin_map(v,s1,s2,t1,t2):
  return (v-s1) / (s2-s1) * (t2 - t1) + t1


pg.init()
größe = breite, höhe = 1000, 1000
fenster = pg.display.set_mode(größe)
radien = [breite/200 * r for r in [20, 50, 80]]
farbe_hintergrund = '#CCC52C'
farbe_linie = pg.Color(0)

daten = pd.read_csv('https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv', header=1)

linien = []
for index,zeile in daten.iterrows():
  for monat in range(1,13):
    jahr = zeile[0]
    if zeile[monat] == '***': break
    anomalie = float(zeile[monat])
    radius = lin_map(anomalie, -1, 1, min(radien), max(radien))
    pos = pol2kart(radius, math.tau/12*monat - math.tau/4)
    linien.append((jahr, pos, anomalie))



clock = pg.time.Clock()
FPS = 40

gen_hintergrund()

for (j1,p1,a1), (j2,p2,a2) in zip(linien,linien[1:]):
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT or \
       ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE:
      quit()
  
  hue = min(lin_map(a1,-1,1,180,359),359)
  farbe_linie.hsva = hue,100,100
  pg.draw.line(fenster, farbe_linie, p1, p2, 3)
  zeichne_text(str(j1), (breite/2, höhe/2), 70, farbe_linie, hg=True)
  clock.tick(FPS)
  pg.display.flip()


while True:
  clock.tick(FPS)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT or \
       ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE:
      quit()