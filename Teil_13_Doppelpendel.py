from dataclasses import dataclass
import math
import pygame as pg

PI = math.pi
G = 1
BREITE = 900
HÖHE = 600


@dataclass
class Pendel():
  pos: tuple
  winkel: float
  länge: int
  masse: int
  acc: float = 0
  vel: float = 0

  def endPos(self):
    x = int(self.pos[0] + self.länge*math.sin(self.winkel))
    y = int(self.pos[1] + self.länge*math.cos(self.winkel))
    return (x, y)

  def show(self):
    ePos = self.endPos()
    pg.draw.line(screen, (255, 255, 255), self.pos, ePos, 3)
    pg.draw.circle(screen, (255, 0, 0), ePos, self.masse)


pg.init()
#für das Pendel, wird nach jedem Frame wieder gelöscht
screen = pg.display.set_mode([BREITE, HÖHE])
#für die Linie, die der Position des 2ten Pendels folgt
screen2 = pg.Surface([BREITE, HÖHE])

p1 = Pendel((BREITE//2, 50), PI/2, 200, 10)
pos = p1.endPos()
p2 = Pendel(pos, PI/2, 200, 10)
oldPos = p2.endPos()

# Hauptschleife zum Bildschirmzeichnen und zur Auswertung der Ereignisse
clock = pg.time.Clock()
weitermachen = True
while weitermachen:
  # Frames per second setzen
  clock.tick(60)
  screen.fill((0, 0, 0))
  #Linie wird über BLIT auf den screen gestanzt
  screen.blit(screen2, (0, 0))
  # Events auswerten
  for event in pg.event.get():
    # wenn Fenster geschlossen wird
    if event.type == pg.QUIT:
      weitermachen = False

  p1.acc = -G*(2*p1.masse+p2.masse)*math.sin(p1.winkel)-p2.masse \
    * G * math.sin(p1.winkel - 2*p2.winkel) \
    - 2 * math.sin(p1.winkel - p2.winkel) * p2.masse \
    * (p2.vel**2*p2.länge + p1.vel**2*p1.länge*math.cos(p1.winkel-p2.winkel))
  p1.acc = p1.acc / (p1.länge*(2*p1.masse+p2.masse -
                               p2.masse*math.cos(2*p1.winkel-2*p2.winkel)))

  p2.acc = 2*math.sin(p1.winkel-p2.winkel)*(p1.vel**2*p1.länge*(p1.masse+p2.masse) \
    + G * (p1.masse+p2.masse) * math.cos(p1.winkel) \
    + p2.vel**2*p2.länge*p2.masse* math.cos(p1.winkel - p2.winkel))
  p2.acc = p2.acc / (p1.länge*(2*p1.masse+p2.masse -
                               p2.masse*math.cos(2*p1.winkel-2*p2.winkel)))

  p1.vel += p1.acc
  p1.winkel += p1.vel
  p2.vel += p2.acc
  p2.winkel += p2.vel

  p1.show()
  p2.pos = p1.endPos()
  p2.show()
  newPos = p2.endPos()
  pg.draw.line(screen2, (0, 255, 0), oldPos, newPos, 2)
  oldPos = newPos

  pg.display.flip()
pg.quit()
