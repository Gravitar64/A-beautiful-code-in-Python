import pygame as pg, copy


def rotate_curve(curve):
  rotated = copy.deepcopy(curve)
  pivot_point = curve[-1]

  for _ in range(45):
    for point in rotated[:-1]:
      point -= pivot_point
      point.rotate_ip(2)
      point += pivot_point

    clock.tick(FPS)
    fenster.fill('black')
    pg.draw.lines(fenster, 'green', False, curve)
    pg.draw.lines(fenster, 'green', False, rotated)
    pg.draw.circle(fenster, 'red', pivot_point, 5)
    pg.display.flip()

  curve.extend(rotated[-2::-1])
  return curve


pg.init()
größe = breite, höhe = pg.Vector2(1920, 1080)
fenster = pg.display.set_mode(größe)


clock = pg.time.Clock()
FPS = 40
start = pg.Vector2(größe / 2)

curve = [start, start + pg.Vector2(10, 0)]


while True:
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT or ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE: quit()
    if ereignis.type == pg.MOUSEBUTTONDOWN:
      curve = rotate_curve(curve)
