import pygame as pg, copy


def rotiere_kurve(kurve):
  rotiert = copy.deepcopy(kurve)
  drehpunkt = kurve[-1]

  for _ in range(30):
    for punkt in rotiert:
      punkt -= drehpunkt
      punkt.rotate_ip(-3)
      punkt += drehpunkt

    clock.tick(FPS)
    fenster.fill('black')
    pg.draw.lines(fenster, 'green', False, kurve)
    pg.draw.lines(fenster, 'green', False, rotiert)
    pg.draw.circle(fenster, 'red', drehpunkt, 5)
    pg.display.flip()

  kurve.extend(rotiert[-2::-1])
  return kurve


pg.init()
größe = breite, höhe = pg.Vector2(1920, 1080)
fenster = pg.display.set_mode(größe)
clock = pg.time.Clock()
FPS = 40
start = pg.Vector2(größe / 2)

curve = [start, start + pg.Vector2(200, 0)]


while True:
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT or ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE: quit()
    if ereignis.type == pg.MOUSEBUTTONDOWN:
      curve = rotiere_kurve(curve)
