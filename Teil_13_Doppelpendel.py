from dataclasses import dataclass
import math
import pygame as pg

PI = math.pi
G = 1
BREITE = 900
HÖHE = 600


@dataclass
class Pendel():
  anfPos: tuple
  winkel: float
  länge: int
  masse: int
  acc: float = 0
  vel: float = 0
  endPos : tuple = (0,0)

  def endPosBerechnen(self):
    x = int(self.anfPos[0] + self.länge*math.sin(self.winkel))
    y = int(self.anfPos[1] + self.länge*math.cos(self.winkel))
    self.endPos = (x,y)

  def show(self):
    pg.draw.line(screen, (255, 255, 255), self.anfPos, self.endPos, 3)
    pg.draw.circle(screen, (255, 0, 0), self.endPos, self.masse)

  def updateWinkel(self,acceleration):
    self.acc = acceleration
    self.vel += self.acc
    self.winkel += self.vel
    self.endPosBerechnen()  


pg.init()
#für das Pendel, wird nach jedem Frame wieder gelöscht
screen = pg.display.set_mode([BREITE, HÖHE])
#für die Linie, die der Position des 2ten Pendels folgt
screen2 = pg.Surface([BREITE, HÖHE])

p1 = Pendel((BREITE//2, HÖHE//3), PI/2, HÖHE//3, 10)
p1.endPosBerechnen()
p2 = Pendel(p1.endPos, PI/2, HÖHE//3, 10)
p2.endPosBerechnen()
oldPos = p2.endPos

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
  
  #Quelle der Formeln = https://myphysicslab.com/pendulum/double-pendulum-en.html
  acc1 = -G*(2*p1.masse+p2.masse)*math.sin(p1.winkel)-p2.masse \
    * G * math.sin(p1.winkel - 2*p2.winkel) \
    - 2 * math.sin(p1.winkel - p2.winkel) * p2.masse \
    * (p2.vel**2*p2.länge + p1.vel**2*p1.länge*math.cos(p1.winkel-p2.winkel))
  acc1 = acc1 / (p1.länge*(2*p1.masse+p2.masse -
                               p2.masse*math.cos(2*p1.winkel-2*p2.winkel)))

  acc2 = 2*math.sin(p1.winkel-p2.winkel)*(p1.vel**2*p1.länge*(p1.masse+p2.masse) \
    + G * (p1.masse+p2.masse) * math.cos(p1.winkel) \
    + p2.vel**2*p2.länge*p2.masse* math.cos(p1.winkel - p2.winkel))
  acc2 = acc2 / (p1.länge*(2*p1.masse+p2.masse -
                               p2.masse*math.cos(2*p1.winkel-2*p2.winkel)))

  p1.updateWinkel(acc1)
  p2.updateWinkel(acc2)
  p2.anfPos = p1.endPos

  p1.show()
  p2.show()
  pg.draw.line(screen2, (0, 255, 0), oldPos, p2.endPos, 2)
  oldPos = p2.endPos

  pg.display.flip()
pg.quit()
