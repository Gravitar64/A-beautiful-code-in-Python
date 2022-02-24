import pygame as pg
from itertools import permutations


class Body:
  def __init__(self, pos, geschw, masse):
    self.pos = pg.Vector2(pos)
    self.geschw = pg.Vector2(geschw)
    self.masse = masse
    self.rad = (masse / 3.141) ** (1/3)

  def wird_angezogen_von(self, other):
    entf = pg.math.Vector2.distance_to(self.pos, other.pos)
    v_richt = pg.math.Vector2.normalize(other.pos - self.pos)
    if entf > (self.rad + other.rad):
      self.geschw += G * (self.masse * other.masse) / entf**2 * v_richt / self.masse
    else:
      gm = self.masse + other.masse
      self.geschw = (self.geschw * self.masse + other.geschw * other.masse) / gm
      self.pos = (self.pos * self.masse + other.pos * other.masse) / gm
      self.masse, other.masse = gm, 0
      self.rad = (gm / 3.141) ** (1/3)

  def aktualisiere_pos(self):
    self.pos += self.geschw / FPS


pg.init()
screen = pg.display.set_mode((1920, 1080))
zentrum = (screen.get_width() / 2, screen.get_height() / 2)
bodies = [Body(zentrum, (0, 0), 200_000)]
G = 5

clock = pg.time.Clock()
FPS = 40

# Zeichenschleife mit FPS Bildern pro Sekunde
while True:
  clock.tick(FPS)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT: quit()
    if ereignis.type == pg.MOUSEBUTTONDOWN:
      pos1 = pg.Vector2(pg.mouse.get_pos())
      if ereignis.button == 3:
        m, i = max([(b.masse, i) for i, b in enumerate(bodies)])
        bodies[i].pos = pos1
        bodies[i].geschw = 0, 0

    if ereignis.type == pg.MOUSEBUTTONUP and ereignis.button == 1:
      pos2 = pg.Vector2(pg.mouse.get_pos())
      geschw = pos1 - pos2
      bodies.append(Body(pos2, geschw*2, 1000))

  screen.fill('#000000')
  for b1, b2 in permutations(bodies, 2):
    if b1.masse == 0 or b2.masse == 0: continue
    b1.wird_angezogen_von(b2)

  bodies = [b for b in bodies if b.masse > 0]

  for body in bodies:
    body.aktualisiere_pos()
    pg.draw.circle(screen, '#F2cb05', body.pos, body.rad)

  if pg.mouse.get_pressed()[0]:
    pos2 = pg.Vector2(pg.mouse.get_pos())
    pg.draw.line(screen, '#419fd9', pos1, pos2, 1)

  pg.display.flip()