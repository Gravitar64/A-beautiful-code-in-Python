import pygame as pg, random as rnd, time


def initialisiere(größe, pos1):
  rad1 = pg.Vector2(min(größe) / 2, 0).rotate(rnd.randrange(360))

  rad2 = rad1 * rnd.random()
  pos2 = pos1 + rad1 - rad2

  rad3 = rad2 * rnd.random()
  return rad1, rad2, pos2, rad3, False


pg.init()
größe = pg.Vector2(1920, 1080)
fenster = pg.display.set_mode(größe)
hintergrund = pg.surface.Surface(größe)
color = pg.Color(0)

color.hsva = rnd.randrange(360), 100, 100
step = 0.1
pos1 = größe / 2
rad1, rad2, pos2, rad3, letzte_pos = initialisiere(größe, pos1)

kreise, linie = True, False
while True:

  fenster.blit(hintergrund, (0, 0))

  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT: quit()
    if ereignis.type == pg.KEYDOWN:
      match ereignis.key:
        case pg.K_ESCAPE: quit()
        case pg.K_k: kreise = not kreise
        case pg.K_l: linie = not linie
        case pg.K_f: color.hsva = rnd.randrange(360), 100, 100
        case pg.K_RETURN: rad1, rad2, pos2, rad3, letzte_pos = initialisiere(größe, pos1)
        case pg.K_KP_PLUS: step *= 2
        case pg.K_KP_MINUS: step /= 2
        case pg.K_s: pg.image.save(hintergrund, f'Teil_105_Spirograph{time.time()}.png')
        case pg.K_n:
          rad1, rad2, pos2, rad3, letzte_pos = initialisiere(größe, pos1)
          hintergrund.fill('black')

  pos2 = pos1 + (pos2 - pos1).rotate(step)
  rad3 = rad3.rotate(-step * rad1.length() / rad2.length())
  pos3 = pos2 + rad3

  if kreise:
    pg.draw.circle(fenster, 'white', pos1, rad1.length(), 2)
    pg.draw.circle(fenster, 'red', pos1, 5)
    pg.draw.circle(fenster, 'white', pos2, rad2.length(), 2)
    pg.draw.circle(fenster, 'blue', pos2, 5)
    pg.draw.line(fenster, 'blue', pos2, pos3, 2)
    pg.draw.circle(fenster, color, pos3, 5)

  if linie and letzte_pos:
    pg.draw.line(hintergrund, color, letzte_pos, pos3, 2)

  letzte_pos = pos3

  pg.display.flip()
