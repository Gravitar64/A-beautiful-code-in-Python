import pygame as pg


class Ball():
  def __init__(self, farbe, pos, richtung):
    self.farbe = farbe
    self.pos = pg.Vector2(pos)
    self.richtung = pg.Vector2(richtung)
    self.rect = pg.Rect(*pos, BALL_RADIUS * 2, BALL_RADIUS * 2, center=pos)
    self.aktiv = False

  def update(self):
    if not self.aktiv:
      self.rect.midbottom = schläger.rect.midtop
      self.pos = pg.Vector2(self.rect.center)
      self.richtung = pg.Vector2(10, -10)
    else:
      self.pos += self.richtung
      self.rect.center = self.pos

      if self.rect.left < 0 or self.rect.right > breite:
        self.richtung.x *= -1
      if self.rect.top < 0:
        self.richtung.y *= -1
      if self.rect.top > höhe:
        return True

      for block in blöcke:
        if not self.rect.colliderect(block.rect): continue
        self.pos -= self.richtung
        self.rect.center = self.pos
        if self.rect.right <= block.rect.left or self.rect.left >= block.rect.right:
          self.richtung.x *= -1
        if self.rect.top >= block.rect.bottom or self.rect.bottom <= block.rect.top:
          self.richtung.y *= -1
        if block.treffer():
          blöcke.remove(block)
        break

      if self.rect.colliderect(schläger.rect):
        self.pos -= self.richtung
        normal_vektor = self.pos - pg.Vector2(schläger.rect.centerx, 700)
        self.richtung.reflect_ip(normal_vektor)
        self.richtung *= 1.01

    pg.draw.circle(fenster, self.farbe, self.pos, BALL_RADIUS)


class Schläger():
  def __init__(self, farbe):
    self.farbe = farbe
    self.pos = pg.Vector2(0, 0)
    self.rect = pg.Rect(*self.pos, 100, 20, center=self.pos)

  def update(self):
    x, y = pg.mouse.get_pos()
    self.rect.center = x, höhe - 40
    pg.draw.rect(fenster, self.farbe, self.rect)


class Block():
  def __init__(self, farbe, pos, leben):
    self.farbe = farbe
    self.pos = pg.Vector2(pos)
    self.rect = pg.Rect(*pos, BLOCK_BR, BLOCK_HÖ)
    self.leben = leben

  def update(self):
    pg.draw.rect(fenster, self.farbe, self.rect)
    pg.draw.rect(fenster, 'black', self.rect, 3)

  def treffer(self):
    self.leben -= 1
    return self.leben <= 0


pg.init()
pg.display.set_caption(f'BREAK-OUT')
größe = breite, höhe = 800, 600
fenster = pg.display.set_mode(größe)
clock = pg.time.Clock()
FPS = 40
pg.mouse.set_visible(False)

BALL_RADIUS = 10
BLOCK_BR, BLOCK_HÖ = 60, 30
ball = Ball('dodgerblue', (103, 87), (10, -10))
schläger = Schläger('lightblue')

blöcke, farben = [], ['red', 'orange', 'yellow', 'green']
for ze in range(8):
  for sp in range(11):
    farbe = farben[ze // 2]
    x, y = 70 + sp * BLOCK_BR, 70 + ze * BLOCK_HÖ
    blöcke.append(Block(farbe, (x, y), 4 - ze // 2))

anz_bälle = 3
while anz_bälle > 0:
  clock.tick(FPS)
  fenster.fill('black')

  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT or ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE: quit()
    if ereignis.type == pg.MOUSEBUTTONDOWN: ball.aktiv = True

  for block in blöcke: block.update()
  if ball.update():
    anz_bälle -= 1
    ball.aktiv = False
  schläger.update()


  pg.display.flip()
