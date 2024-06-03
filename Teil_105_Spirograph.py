import pygame as pg, random as rnd, time


def initialisiere():
  color.hsva = (rnd.randrange(360), 100, 100)
  pos1, rad1 = größe / 2, pg.Vector2(min(größe) / 2, 0)
  rad1.rotate_ip(rnd.randrange(360))
  rad2 = rad1 * rnd.random()
  rad3 = rad1 - rad2
  rad4 = rad2 * rnd.random()
  ratio = rad1.length() / rad2.length()
  pos2 = pos1 + rad3
  return None, (pos1, rad1), (pos2, rad2), rad3, rad4, ratio


pg.init()
größe = pg.Vector2(1920, 1080)
fenster = pg.display.set_mode(größe)
hintergrund = pg.surface.Surface(größe)
color = pg.Color(0)

step = 0.1
last, (pos1, rad1), (pos2, rad2), rad3, rad4, ratio = initialisiere()
kreise, linien = True, False

while True:
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT: quit()
    if ereignis.type == pg.KEYDOWN:
      match ereignis.key:
        case pg.K_ESCAPE: quit()
        case pg.K_RETURN: last, (pos1, rad1), (pos2, rad2), rad3, rad4, ratio = initialisiere()
        case pg.K_s: pg.image.save(hintergrund, f'Teil_105_spirograph_{time.time()}.png')
        case pg.K_k: kreise = not kreise
        case pg.K_l: linien = not linien
        case pg.K_c: color.hsva = (rnd.randrange(360), 100, 100)
        case pg.K_KP_PLUS: step *= 2
        case pg.K_KP_MINUS: step /= 2
        case pg.K_n:
          last, (pos1, rad1), (pos2, rad2), rad3, rad4, ratio = initialisiere()
          hintergrund.fill('black')

  rad3.rotate_ip(step)
  rad4.rotate_ip(-step*ratio)
  pos2 = pos1 + rad3
  pos3 = pos2 + rad4

  if linien and last and pos3:
    pg.draw.line(hintergrund, color, last, pos3, 2)
  last = pos3

  fenster.blit(hintergrund, (0, 0))
  if kreise:
    pg.draw.circle(fenster, 'white', pos1, rad1.length(), 1)
    pg.draw.circle(fenster, 'white', pos2, rad2.length(), 1)
    pg.draw.line(fenster, 'white', pos2, pos3, 1)
    pg.draw.circle(fenster, color, pos3, 10)
  pg.display.flip()
