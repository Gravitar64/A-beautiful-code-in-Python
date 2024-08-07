import pygame as pg, random as rnd, time


def gift_wrapping(punkte):
  startpunkt = pg.Vector2(min((p.x, p.y) for p in punkte))
  hülle = [startpunkt]
  while True:
    endpunkt = rnd.choice(punkte)
    if startpunkt == endpunkt: continue
    for p in punkte:
      if (endpunkt - startpunkt).cross(p - startpunkt) < 0: endpunkt = p
    if endpunkt == hülle[0]: return hülle
    startpunkt = endpunkt
    hülle.append(startpunkt)
    punkte.remove(startpunkt)


pg.init()
größe = breite, höhe = 1920, 1080
fenster = pg.display.set_mode(größe)
clock = pg.time.Clock()
FPS = 5

start = time.perf_counter()
punkte = [pg.Vector2(rnd.randrange(breite), rnd.randrange(höhe)) for _ in range(16)]
hülle = gift_wrapping(punkte)
print(time.perf_counter() - start)

while True:
  clock.tick(FPS)

  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT or ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE: quit()

  for punkt in punkte:  pg.draw.circle(fenster, 'white', punkt, 5)
  for punkt in hülle:   pg.draw.circle(fenster, 'green', punkt, 10)

  pg.draw.polygon(fenster, 'green', hülle, 2)

  pg.display.flip()
