import pygame as pg
from itertools import combinations


class Körper:
  def __init__(self, pos, geschw, masse):
    self.pos = pg.Vector2(pos)
    self.geschw = pg.Vector2(geschw)
    self.masse = masse
    self.rad = (masse / 3.141) ** (1 / 3)
    self.spur = [pos]

  def aktualisiere_pos(self):
    self.pos += self.geschw / FPS
    self.spur.append(self.pos.xy)
    if len(self.spur) > 50: self.spur.pop(0)

  def gravitation(self, other):
    entf = pg.math.Vector2.distance_to(self.pos, other.pos)
    v_richt = pg.math.Vector2.normalize(other.pos - self.pos)
    if entf > (self.rad + other.rad):
      f = G * (self.masse * other.masse) / entf**2
      self.geschw += f * v_richt / self.masse / FPS
      other.geschw += f * -v_richt / other.masse / FPS
    else:
      gm = self.masse + other.masse
      self.geschw = (self.geschw * self.masse + other.geschw * other.masse) / gm
      self.pos = (self.pos * self.masse + other.pos * other.masse) / gm
      self.masse, other.masse = gm, 0
      self.rad = (gm / 3.141) ** (1 / 3)


pg.init()
screen = pg.display.set_mode((1920, 1080))
zentrum = (screen.get_width() / 2, screen.get_height() / 2)

clock = pg.time.Clock()
FPS = 40
G = 200
körpers = [Körper(zentrum, (0, 0), 200_000)]

# Zeichenschleife mit FPS Bildern pro Sekunde
while True:
  clock.tick(FPS)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT: quit()
    if ereignis.type == pg.MOUSEBUTTONDOWN:
      pos1 = pg.Vector2(pg.mouse.get_pos())
      if ereignis.button == 3:
        m, i = max([(k.masse, i) for i, k in enumerate(körpers)])
        körpers[i].pos = pos1
        körpers[i].geschw = pg.Vector2(0, 0)
    if ereignis.type == pg.MOUSEBUTTONUP and ereignis.button == 1:
      pos2 = pg.Vector2(pg.mouse.get_pos())
      geschw = pos1 - pos2
      körpers.append(Körper(pos2, geschw, 10_000))

  for k1, k2 in combinations(körpers, 2):
    if k1.masse == 0 or k2.masse == 0: continue
    k1.gravitation(k2)

  körpers = [k for k in körpers if k.masse > 0]

  screen.fill('#000000')
  for körper in körpers:
    körper.aktualisiere_pos()
    pg.draw.circle(screen, '#F2cb05', körper.pos, körper.rad)
    if len(körper.spur) > 2:
      pg.draw.lines(screen, '#303AF2', False, körper.spur, 2)

  if pg.mouse.get_pressed()[0]:
    pos2 = pg.Vector2(pg.mouse.get_pos())
    pg.draw.line(screen, '#419fd9', pos1, pos2, 1)

  pg.display.flip()
