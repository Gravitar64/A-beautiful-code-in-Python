import pygame as pg
import math

multiplier = 2 
modulus = 9
winkelschritt = math.tau / modulus
breite = höhe = 1080
zentrum = (breite//2, höhe//2)
zx, zy = zentrum
radius = breite//2-16

def i2Pos(i):
  winkel = winkelschritt * i - math.pi/2
  x = int(zx + radius * math.cos(winkel))
  y = int(zy + radius * math.sin(winkel))
  return (x,y)


pg.init()
fenster = pg.display.set_mode((breite, höhe))
screen2 = pg.Surface((breite,höhe))
farbe = pg.Color(150,150,150)

pg.draw.circle(screen2,(255,255,255),zentrum,radius,2)
startpunkte = []
for punkt in range(modulus):
  pos = i2Pos(punkt)
  pg.draw.circle(screen2,(0,150,255),pos,6)
  startpunkte.append(pos)


clock = pg.time.Clock()
while True:
  fenster.blit(screen2,(0,0))
  clock.tick(5)
  for event in pg.event.get():
    if event.type == pg.QUIT: quit() 
  
  for i, startpunkt in enumerate(startpunkte):
    ziel_i = (i * multiplier) % modulus
    pg.draw.line(fenster,'#6E001F',startpunkt,i2Pos(ziel_i),1)
  
  screen3 = pg.font.SysFont('cour',82).render(f'x {multiplier}',False,(farbe))
  screen4 = pg.font.SysFont('cour',82).render(f'mod {modulus}',False,(farbe))
  screen4_rect = screen4.get_rect(topright=(breite,10))
  fenster.blit(screen3,(3,10))
  fenster.blit(screen4,screen4_rect)
  pg.display.flip()
pg.quit()