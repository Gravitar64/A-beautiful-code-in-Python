import pygame as pg

# pygame ab Version 2.0 wird benötigt
# Installation im Terminal mit
#   --> pip install pygame (windows)
#   --> pip3 install pygame (mac)
#   --> sudo apt-get install python3-pygame (Linux Debian/Ubuntu/Mint)

pg.init()
größe = breite, höhe = 1920, 1080
fenster = pg.display.set_mode(größe)


clock = pg.time.Clock()
FPS = 40

# Zeichenschleife mit FPS Bildern pro Sekunde
while True:
  clock.tick(FPS)
  fenster.fill('black')

  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT or ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE: quit()

  pg.display.flip()
