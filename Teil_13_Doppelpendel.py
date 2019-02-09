from dataclasses import dataclass
import math
import pygame as pg

PI = math.pi
g = 1
BREITE = 900
HÖHE = 600


@dataclass
class Pendel():
  anfPos: tuple
  θ: float
  L: int
  m: int
  θ1 : float = 0
  θ2 : float = 0
  endPos : tuple = (0,0)

  def endPosBerechnen(self):
    x = int(self.anfPos[0] + self.L*math.sin(self.θ))
    y = int(self.anfPos[1] + self.L*math.cos(self.θ))
    self.endPos = (x,y)

  def show(self):
    pg.draw.line(screen, (255, 255, 255), self.anfPos, self.endPos, 3)
    pg.draw.circle(screen, (255, 0, 0), self.endPos, self.m)

  def updateWinkel(self,acceleration):
    self.θ2 = acceleration
    self.θ1 += self.θ2
    self.θ += self.θ1
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
    if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
      weitermachen = False
  
  #Quelle der Formeln = https://myphysicslab.com/pendulum/double-pendulum-en.html
  acc1 = (-g*(2*p1.m+p2.m)*math.sin(p1.θ)-p2.m \
    * g * math.sin(p1.θ - 2*p2.θ) \
    - 2 * math.sin(p1.θ - p2.θ) * p2.m \
    * (p2.θ1**2*p2.L + p1.θ1**2*p1.L*math.cos(p1.θ-p2.θ))) \
    / (p1.L*(2*p1.m+p2.m - p2.m*math.cos(2*p1.θ-2*p2.θ)))

  acc2 = (2*math.sin(p1.θ-p2.θ)*(p1.θ1**2*p1.L*(p1.m+p2.m) \
    + g * (p1.m+p2.m) * math.cos(p1.θ) \
    + p2.θ1**2*p2.L*p2.m* math.cos(p1.θ - p2.θ))) \
    / (p1.L*(2*p1.m+p2.m - p2.m*math.cos(2*p1.θ-2*p2.θ)))

  p1.updateWinkel(acc1)
  p2.updateWinkel(acc2)
  p2.anfPos = p1.endPos

  p1.show()
  p2.show()
  pg.draw.line(screen2, (0, 150, 255), oldPos, p2.endPos, 2)
  oldPos = p2.endPos

  pg.display.flip()
pg.quit()
