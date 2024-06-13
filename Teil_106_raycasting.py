import pygame as pg, random as rnd


# https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection#Given_two_points_on_each_line_segment
def get_intersect(a, b, c, d):
  if not (nenner := (a.x - b.x) * (c.y - d.y) - (a.y - b.y) * (c.x - d.x)): return
  t = ((a.x - c.x) * (c.y - d.y) - (a.y - c.y) * (c.x - d.x)) / nenner
  u = -((a.x - b.x) * (a.y - c.y) - (a.y - b.y) * (a.x - c.x)) / nenner
  if 0 <= t <= 1 and 0 <= u <= 1: return a.lerp(b, t)


def ray_casting(wände):
  c = V2(pg.mouse.get_pos())
  for ray in rays:
    d = c + ray
    entfernungen = [(c.distance_to(i), i) for a, b in wände if (i := get_intersect(a, b, c, d))]
    if not entfernungen: continue
    pg.draw.line(fenster, 'green', c, min(entfernungen)[1], 1)


pg.init()
größe = breite, höhe = 1920, 1080
fenster = pg.display.set_mode(größe)

V2 = pg.Vector2
wände = [tuple(V2(rnd.randrange(breite), rnd.randrange(höhe)) for _ in range(2)) for _ in range(10)]
rays = [V2(max(größe), 0).rotate(w) for w in range(360)]

while True:
  fenster.fill('black')

  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT or ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE: quit()

  ray_casting(wände)

  for a, b in wände:
    pg.draw.line(fenster, 'white', a, b, 3)

  pg.display.flip()
