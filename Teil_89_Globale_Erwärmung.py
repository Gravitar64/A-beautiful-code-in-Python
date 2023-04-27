import pandas as pd
import pygame as pg
import math


def gen_hintergrund():

  for r in radien:
    pg.draw.circle(fenster, farbe_hintergrund, (breite/2, höhe/2), r, 3)

  radius_text = max(radien)+40
  for i in range(1, 13):
    winkel = math.tau/12*i - math.tau/4
    pos = pol2kart(radius_text, winkel)
    zeichne_text(data.columns[i],pos,48,farbe_hintergrund,math.degrees(-winkel)-90)
    if i != 12: continue
    for i, r in enumerate(radien):
      pos = pol2kart(r-15, winkel)
      zeichne_text(f'{"+" if -1+i > 0 else ""}{-1+i}°C',pos,28,farbe_hintergrund)


def lin_map(s1, s2, t1, t2, v):
  return (v - s1) / (s2 - s1) * (t2 - t1) + t1


def pol2kart(r, w):
  return r * math.cos(w) + breite/2, r * math.sin(w) + höhe/2


def zeichne_text(text,pos,größe,farbe,rotation=0, hg=False):
  t = pg.font.SysFont('arial', größe).render(text, False, farbe)
  t = pg.transform.rotate(t, rotation)
  t_rect = t.get_rect(center=pos)
  fenster.blit(t, t_rect)
  if hg: pg.draw.rect(fenster,'black',t_rect)



größe = breite, höhe = 1000, 1000
radien = [r*breite/200 for r in [20, 50, 80]]

data = pd.read_csv('https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv', header=1)
linien = [(row[0], pol2kart(lin_map(-1, 1, min(radien), max(radien), float(row[monat])), math.tau/12*monat - math.tau/4))
          for _, row in data.iterrows() 
          for monat in range(1, 13) if row[monat] != '***']

pg.init()
fenster = pg.display.set_mode(größe)
farbe_linie = pg.Color(0)
farbe_hintergrund = '#CCC52C'
clock = pg.time.Clock()
FPS = 40

gen_hintergrund()

for (j1, p1), (j2, p2) in zip(linien, linien[1:]):
  r = ((breite/2-p1[0])**2 + (höhe/2-p1[1])**2) ** 0.5
  hue = min(lin_map(min(radien),max(radien),179,359,r),359)
  farbe_linie.hsva = hue,100,100
  zeichne_text(str(j2),(breite/2, höhe/2),70,farbe_linie,hg=True)
  pg.draw.line(fenster, farbe_linie, p1, p2, 3)
  pg.display.flip()
  clock.tick(FPS)

gen_hintergrund()
pg.display.flip()

while True:
  clock.tick(FPS)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT or \
            ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE:
      quit()
