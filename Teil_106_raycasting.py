import pygame as pg, random as rnd


def get_intersect(a, b, c, d):
  ab, cd, ac = a - b, c - d, a - c
  if not (nenner := ab.x * cd.y - ab.y * cd.x): return
  t = (ac.x * cd.y - ac.y * cd.x) / nenner
  u = -(ab.x * ac.y - ab.y * ac.x) / nenner
  if 0 <= t <= 1 and 0 <= u <= 1: return a.lerp(b, t)


def ray_casting(wände):
  c = V2(pg.mouse.get_pos())
  for ray in rays:
    d = c + ray
    entfernungen = [(c.distance_to(k), k) for a, b in wände if (k := get_intersect(a, b, c, d))]
    if not entfernungen: continue
    pg.draw.line(fenster, 'green', c, min(entfernungen)[1], 1)


pg.init()
größe = breite, höhe = 1920, 1080
fenster = pg.display.set_mode(größe)

clock = pg.time.Clock()
FPS = 40

V2 = pg.Vector2
wände = [tuple(V2(rnd.randrange(breite), rnd.randrange(höhe)) for _ in range(2)) for _ in range(10)]
rays = [V2(3000, 0).rotate(w) for w in range(360)]

while True:
  clock.tick(FPS)
  fenster.fill('black')

  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT or ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE: quit()

  ray_casting(wände)

  for a, b in wände:
    pg.draw.line(fenster, 'white', a, b, 3)

  pg.display.flip()
