import pygame as pg, random as rnd


def gift_wrapping(punkte):
  startpunkt = pg.Vector2((min([(p.x, p.y) for p in punkte])))
  hülle = [startpunkt]

  while True:
    endpunkt = rnd.choice(punkte)
    if startpunkt == endpunkt: continue

    for punkt in punkte:
      if (endpunkt - startpunkt).cross(punkt - startpunkt) < 0: endpunkt = punkt

    if endpunkt == hülle[0]: return hülle

    hülle.append(endpunkt)
    startpunkt = endpunkt


pg.init()
größe = breite, höhe = 1920, 1080
fenster = pg.display.set_mode(größe)


clock = pg.time.Clock()
FPS = 40
ANZ_PUNKTE = 25
punkte = [pg.Vector2(rnd.randrange(breite), rnd.randrange(höhe)) for _ in range(ANZ_PUNKTE)]

while True:
  clock.tick(FPS)
  fenster.fill('black')

  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT or ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE: quit()

  for punkt in punkte:
    pg.draw.circle(fenster, 'white', punkt, 5)

  hülle = gift_wrapping(punkte)

  for punkt in hülle:
    pg.draw.circle(fenster, 'green', punkt, 10)

  pg.draw.lines(fenster, 'green', True, hülle, 3)

  pg.display.flip()
