import pygame as pg, random as rnd


def segment_intersection(a, b, c, d):
  bottom = (d.y - c.y) * (b.x - a.x) - (d.x - c.x) * (b.y - a.y)
  if not bottom: return
  t_top = (d.x - c.x) * (a.y - c.y) - (d.y - c.y) * (a.x - c.x)
  u_top = (c.y - a.y) * (a.x - b.x) - (c.x - a.x) * (a.y - b.y)
  t = t_top / bottom
  u = u_top / bottom
  return a.lerp(b,t) if 0 <= u <= 1 and 0 <= t <= 1 else None


def ray_casting(wände):
  a = V2(pg.mouse.get_pos())
  for ray in rays:
    b = a + ray
    entfernung, best_pos = 99999, None
    for c, d in wände:
      if not (intersect := segment_intersection(a, b, c, d)): continue
      if  (e := a.distance_to(intersect)) < entfernung:
        entfernung = e
        best_pos = intersect
    if not best_pos: continue
    pg.draw.line(fenster, 'gray40', a, best_pos, 1)


V2 = pg.Vector2

pg.init()
größe = breite, höhe = V2(1920, 1080)
fenster = pg.display.set_mode(größe)

wände = [tuple(V2(rnd.randrange(breite), rnd.randrange(höhe)) for _ in range(2))  
         for _ in range(10)]
ecken = [(0, 0), (breite, 0), (breite, höhe), (0, höhe), (0, 0)]
wände.extend([(V2(a), V2(b)) for a, b in zip(ecken,ecken[1:])])

rays = [V2(max(größe),0).rotate(a) for a in range(360)]

while True:
  fenster.fill('black')
  
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT: quit()
    if ereignis.type == pg.KEYDOWN:
      match ereignis.key:
        case pg.K_ESCAPE: quit()

  ray_casting(wände)

  for a, b in wände:
    pg.draw.line(fenster, 'white', a, b, 3)
  
  pg.display.flip()
 