import pygame as pg


class Ball():
  def __init__(self, farbe, pos, richtung):
    self.farbe = farbe
    self.pos = pg.Vector2(pos)
    self.richtung = pg.Vector2(richtung)
    self.rect = pg.Rect(*pos, BALL_RADIUS * 2, BALL_RADIUS * 2, center=pos)
    self.rect_alt = self.rect.copy()

  def update(self):
    self.rect_alt = self.rect.copy()
    self.pos += self.richtung
    self.rect.center = self.pos

    if self.rect.left < 0 or self.rect.right > breite:
      self.richtung.x *= -1
    if self.rect.top < 0 or self.rect.bottom > höhe:
      self.richtung.y *= -1

    for block in blöcke:
      if block.farbe != self.farbe: continue
      if not self.rect.colliderect(block.rect): continue
      if self.rect_alt.right <= block.rect.left or self.rect_alt.left >= block.rect.right:
        self.richtung.x *= -1
      if self.rect_alt.top >= block.rect.bottom or self.rect_alt.bottom <= block.rect.top:
        self.richtung.y *= -1
      block.tausche_farbe()  
      break  


    pg.draw.circle(fenster, self.farbe, self.pos, BALL_RADIUS)


class Block():
  def __init__(self, farbe, pos):
    self.farbe = farbe
    self.pos = pg.Vector2(pos)
    self.rect = pg.Rect(*pos, BLOCK_GROESSE, BLOCK_GROESSE)

  def update(self):
    pg.draw.rect(fenster, self.farbe, self.rect)

  def tausche_farbe(self):
    self.farbe = 'yellow' if self.farbe == 'black' else 'black'  


pg.init()
größe = breite, höhe = 1200, 520
fenster = pg.display.set_mode(größe)


clock = pg.time.Clock()
FPS = 40

BALL_RADIUS = 20
BLOCK_GROESSE = 40
bälle = [Ball('black', (103, 87), (10, 10)), Ball('yellow', (1087, 420), (-10, -10))]

blöcke = []
for y in range(0, höhe, BLOCK_GROESSE):
  for x in range(0, breite, BLOCK_GROESSE):
    farbe = 'yellow' if x < breite / 2 else 'black'
    blöcke.append(Block(farbe, (x, y)))

while True:
  clock.tick(FPS)
  
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT or ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE: quit()

  for block in blöcke: block.update()
  for ball in bälle: ball.update()

  anz_gelbe_blöcke = sum(b.farbe == 'yellow' for b in blöcke)
  pg.display.set_caption(f'Kill-Bill PONG, SCORE = {anz_gelbe_blöcke:>3} : {len(blöcke) - anz_gelbe_blöcke:>3}')


  pg.display.flip()
