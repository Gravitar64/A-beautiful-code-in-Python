import pygame as pg, math, random


class Drop:
  def __init__(self):
    self.center = pg.Vector2(random.randrange(größe.x), random.randrange(größe.y))
    self.radius = random.randrange(10, 100)
    self.color = (random.randrange(256), random.randrange(256), random.randrange(256))
    self.vertices = []
    self.create_vertices()

  def create_vertices(self):
    resolution = 100
    for i in range(resolution):
      angle = math.tau / resolution * i
      self.vertices.append(pg.Vector2(math.cos(angle), math.sin(angle))
                           * self.radius + self.center)

  def marble(self, other):
    c = other.center
    r = other.radius
    new_center = pg.Vector2(0,0)
    for i, p in enumerate(self.vertices):
      p = c + (p - c) * math.sqrt(1 + r * r / pg.Vector2.magnitude_squared(p-c))
      self.vertices[i] = p
      new_center += p
    self.center = new_center / i  


pg.init()
größe = pg.Vector2(1920, 1080)
fenster = pg.display.set_mode(größe)
clock = pg.time.Clock()
FPS = 40

drops = []
while True:
  fenster.fill('black')
  clock.tick(FPS)

  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT or ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE: quit()
  
  new_drop = Drop()
  for drop in drops:
    drop.marble(new_drop)
  drops.append(new_drop)

  drops = [drop for drop in drops 
           if -300 < drop.center.x < (größe.x + 300) and 
              -300 < drop.center.y < (größe.y + 300)]

  print(len(drops))
  for drop in drops:
    pg.draw.polygon(fenster, drop.color, drop.vertices)

  pg.display.flip()
