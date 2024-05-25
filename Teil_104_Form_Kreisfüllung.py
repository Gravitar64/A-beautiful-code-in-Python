import pygame as pg, random as rnd

pg.init()
größe = breite, höhe = 1920, 1080
fenster = pg.display.set_mode(größe)
bild = pg.image.load('Teil_105_Gravitar.png')
maske = [(x, y) for x in range(breite) for y in range(höhe) if bild.get_at((x, y))[0]]
rnd.shuffle(maske)

kreise = []
while maske:
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT or ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE: quit()

  pos = pg.Vector2(maske.pop())
  rad = rnd.randrange(5, 20)

  for pos2, rad2 in kreise:
    if pos.distance_to(pos2) - rad - rad2 < 0: break
  else:
    kreise.append((pos, rad))
    pg.draw.circle(fenster, 'green', pos, rad, 3)
    pg.display.flip()

pg.image.save(fenster, 'Teil_105_kreise.png')
