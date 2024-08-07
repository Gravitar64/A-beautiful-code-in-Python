import pygame as pg
import pandas as pd
import math


def zeichne_text(text, pos, größe, farbe, hg=False, 𝜃=0):
  t = pg.font.SysFont('arial', größe).render(text, True, farbe)
  t = pg.transform.rotate(t, -math.degrees(𝜃))
  t_rect = t.get_rect(center=pos)
  if hg: pg.draw.rect(fenster, 'black', t_rect)
  fenster.blit(t, t_rect)


def pol2kart(r, 𝜃):
  return r * math.cos(𝜃) + breite/2, r * math.sin(𝜃) + höhe/2


def lin_map(v, s1, s2, t1, t2):
  return (v-s1) / (s2-s1) * (t2-t1) + t1


def anom2pos(anomalie, monat):
  r = lin_map(float(anomalie), -1, 1, min(kreise), max(kreise))
  return pol2kart(r, kreis/12*monat - kreis/4)


def gen_hintergrund():
  for i, r in enumerate(kreise, start=-1):
    pg.draw.circle(fenster, farbe_hintergrund, (breite/2, höhe/2), r, 3)
    zeichne_text(f'{i} °C', (breite/2, höhe/2-r), 28, farbe_hintergrund, hg=True)

  r = max(kreise)+40
  for monat in range(1, 13):
    𝜃 = kreis/12*monat
    pos = pol2kart(r, 𝜃 - kreis/4)
    zeichne_text(daten.columns[monat], pos, 48, farbe_hintergrund, 𝜃=𝜃)


daten = pd.read_csv('https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv', header=1)


pg.init()
größe = breite, höhe = 1000, 1000
fenster = pg.display.set_mode(größe)
farbe_hintergrund = '#CCC52C'
farbe_linie = pg.Color(0)
kreise = [breite/2 * r / 100 for r in [20, 50, 80]]
kreis = math.tau

linien = [(zeile[0], anom2pos(zeile[monat], monat), float(zeile[monat]))
          for index, zeile in daten.iterrows() for monat in range(1, 13)
          if zeile[monat] != '***']


clock = pg.time.Clock()
FPS = 80

gen_hintergrund()

for (jahr, p1, _), (_, p2, anomalie) in zip(linien, linien[1:]):

  clock.tick(FPS)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT or \
       ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE:
      quit()

  hue = min(lin_map(anomalie, -1, 1, 180, 360), 360)
  farbe_linie.hsva = hue, 100, 100
  pg.draw.line(fenster, farbe_linie, p1, p2, 3)
  zeichne_text(str(jahr), (breite/2, höhe/2), 70, farbe_linie, hg=True)
  pg.display.flip()

gen_hintergrund()
pg.display.flip()


while True:
  clock.tick(FPS)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT or \
       ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE:
      quit()