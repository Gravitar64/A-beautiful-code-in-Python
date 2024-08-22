import pygame as pg, copy


def rotiere_kurve(kurve, grad):
  rotiert = copy.deepcopy(kurve)
  drehpunkt = kurve[-1]

  for punkt in rotiert:
    punkt -= drehpunkt
    punkt.rotate_ip(grad)
    punkt += drehpunkt

  return rotiert


def zeichne_kurven():
  clock.tick(40)
  fenster.fill('black')
  pg.draw.lines(fenster, 'green', False, kurve)
  if rotiert: pg.draw.lines(fenster, 'green', False, rotiert)
  pg.draw.circle(fenster, 'red', kurve[-1], 5)
  pg.display.flip()


pg.init()
größe = breite, höhe = pg.Vector2(1920, 1080)
fenster = pg.display.set_mode(größe)
start = größe / 2
kurve = [start, start + pg.Vector2(200, 0)]
rotiert = []


clock = pg.time.Clock()
FPS = 40

while True:

  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT or ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE: quit()
    if ereignis.type == pg.MOUSEBUTTONDOWN:
      for grad in range(0, 91, 3):
        rotiert = rotiere_kurve(kurve, grad)
        zeichne_kurven()
      kurve.extend(rotiert[-2::-1])
      rotiert = []

  zeichne_kurven()
