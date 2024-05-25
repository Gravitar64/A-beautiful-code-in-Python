import pygame as pg, random as rnd, itertools as itt

pg.init()
größe = breite, höhe = pg.Vector2(1920, 1080)
fenster = pg.display.set_mode(größe)

bild = pg.image.load('Teil_105_gravitar.png')
schriftzug = [(x, y) for x, y in itt.product(range(1920), range(1080))
              if bild.get_at((x, y))[0]]
rnd.shuffle(schriftzug)

kreise = []
while schriftzug:
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT or ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE: quit()

  pos1 = pg.Vector2(schriftzug.pop())
  radius1 = rnd.randrange(5, 20)

  for pos2, radius2 in kreise:
    if pos1.distance_to(pos2) - radius1 - radius2 < 0: break
  else:
    kreise.append((pos1, radius1))
    pg.draw.circle(fenster, 'green', pos1, radius1, 3)
    pg.display.flip()

pg.image.save(fenster, 'Teil_105_bubbles.png')
