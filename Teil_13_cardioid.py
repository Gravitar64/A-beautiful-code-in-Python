import pygame as pg
import math

TOTAL = 200
faktor = 0
winkelschritt = math.tau / TOTAL
breite, höhe = 1150, 1150
zentrum = (breite//2, höhe//2)
zx, zy = zentrum
radius = breite//2-16

def i2Pos(i):
  winkel = winkelschritt * i + math.pi
  x = int(zx + radius * math.cos(winkel))
  y = int(zy + radius * math.sin(winkel))
  return (x,y)

pg.init()
screen = pg.display.set_mode((breite, höhe))
screen2 = pg.Surface((breite,höhe))
farbe = pg.Color(150,150,150)

pg.draw.circle(screen2,(255,255,255),zentrum,radius,2)
startpunkte = []
for punkt in range(TOTAL):
  pos = i2Pos(punkt)
  pg.draw.circle(screen2,(0,150,255),pos,6)
  startpunkte.append(pos)


clock = pg.time.Clock()
weitermachen = True
while weitermachen:
  screen.blit(screen2,(0,0))
  faktor += 0.002
  clock.tick(70)
  for event in pg.event.get():
    if event.type == pg.QUIT or \
            (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
      weitermachen = False
  
  for i, startpunkt in enumerate(startpunkte):
    ziel_i = (i * faktor) % TOTAL
    farbe.hsva=(360 / TOTAL * i,100,100)
    pg.draw.line(screen,farbe,startpunkt,i2Pos(ziel_i),1)
  
  screen3 = pg.font.SysFont('cour',82).render(f'{faktor:6.1f}',False,(farbe))
  screen.blit(screen3,(3,10))
  pg.display.flip()
pg.quit()
