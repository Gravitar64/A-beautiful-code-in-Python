import pygame as pg, random as rnd, time


def initialisiere(pos1):
  rad1 = pg.Vector2(min(größe) / 2, 0).rotate(rnd.randrange(360))
  rad2 = rad1 * rnd.random()
  pos2 = pos1 + rad1 - rad2
  rad3 = rad2 * rnd.random()
  return rad1, rad2, pos2, rad3, False


def get_color():
  return rnd.randrange(255), rnd.randrange(255), rnd.randrange(255)


pg.init()
größe = pg.Vector2(1920, 1080)
fenster = pg.display.set_mode(größe)
hintergrund = pg.surface.Surface(größe)

color = get_color()
pos1 = größe / 2
rad1, rad2, pos2, rad3, letzte_pos = initialisiere(pos1)
geschwindigkeit = 0.1

zeichne_kreise, zeichne_linie = True, False
while True:
  fenster.fill('black')

  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT: quit()
    if ereignis.type == pg.KEYDOWN:
      match ereignis.key:
        case pg.K_ESCAPE: quit()
        case pg.K_k: zeichne_kreise = not zeichne_kreise
        case pg.K_l: zeichne_linie = not zeichne_linie
        case pg.K_KP_PLUS: geschwindigkeit *= 2
        case pg.K_KP_MINUS: geschwindigkeit /= 2
        case pg.K_f: color = get_color()
        case pg.K_RETURN: rad1, rad2, pos2, rad3, letzte_pos = initialisiere(pos1)
        case pg.K_s: pg.image.save(hintergrund, f'teil_105_Spirograph{time.time()}.png')
        case pg.K_n:
          rad1, rad2, pos2, rad3, letzte_pos = initialisiere(pos1)
          hintergrund.fill('black')

  pos2 = pos1 + (pos2 - pos1).rotate(geschwindigkeit)
  rad3 = rad3.rotate(-geschwindigkeit * rad1.length() / rad2.length())
  pos3 = pos2 + rad3

  fenster.blit(hintergrund, (0, 0))

  if zeichne_kreise:
    pg.draw.circle(fenster, 'gray65', pos1, rad1.length(), 1)
    pg.draw.circle(fenster, 'gray65', pos2, rad2.length(), 1)
    pg.draw.line(fenster, 'gray65', pos2, pos3, 1)
    pg.draw.circle(fenster, color, pos3, 10)

  if zeichne_linie and letzte_pos:
    pg.draw.line(hintergrund, color, letzte_pos, pos3, 3)
  letzte_pos = pos3

  pg.display.flip()
