import pygame as pg, random as rnd, time


def initialisiere():
  color.hsva = (rnd.randrange(360), 100, 100)
  pos1, radius1 = größe / 2, pg.Vector2(min(größe) / 2, 0)
  radius2 = pg.Vector2(rnd.random() * radius1.x, 0)
  pos2 = pos1 + radius1 - radius2
  return None, (pos1, radius1, radius1.x), (pos2, radius2, rnd.random(), radius2.x)


pg.init()
größe = pg.Vector2(1920, 1080)
fenster = pg.display.set_mode(größe)
hintergrund = pg.surface.Surface(größe)
color = pg.Color(0)

step = 0.1
last, (pos1, radius1, l1), (pos2, radius2, skalar, l2) = initialisiere()
kreise, linien = True, False

while True:
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT: quit()
    if ereignis.type == pg.KEYDOWN:
      match ereignis.key:
        case pg.K_ESCAPE: quit()
        case pg.K_RETURN: last, (pos1, radius1, l1), (pos2, radius2, skalar, l2) = initialisiere()
        case pg.K_s: pg.image.save(hintergrund, f'Teil_105_spirograph_{time.time()}.png')
        case pg.K_k: kreise = not kreise
        case pg.K_l: linien = not linien
        case pg.K_c: color.hsva = (rnd.randrange(360), 100, 100)
        case pg.K_KP_PLUS: step *= 2
        case pg.K_KP_MINUS: step /= 2
        case pg.K_n:
          last, (pos1, radius1, l1), (pos2, radius2, skalar, l2) = initialisiere()
          hintergrund.fill('black')

  pos2 = pos1 + ((pos2 - pos1).rotate(step))
  radius2.rotate_ip(-step * l1 / l2)
  pos3 = pos2 + radius2 * skalar

  if linien and last and pos3:
    pg.draw.line(hintergrund, color, last, pos3, 2)
  last = pos3

  fenster.blit(hintergrund, (0, 0))
  if kreise:
    pg.draw.circle(fenster, 'green', pos1, radius1.length(), 1)
    pg.draw.circle(fenster, 'white', pos2, radius2.length(), 1)
    pg.draw.line(fenster, 'white', pos2, pos3, 1)
    pg.draw.circle(fenster, color, pos3, 10)
  pg.display.flip()
