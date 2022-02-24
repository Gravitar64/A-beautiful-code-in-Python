import pygame as pg
#pygame ab Version 2.0 wird benötigt
#Installation im Terminal mit 
#   --> pip install pygame (windows) 
#   --> pip3 install pygame (mac)
#   --> sudo apt-get install python3-pygame (Linux Debian/Ubuntu/Mint)

pg.init()
screen = pg.display.set_mode((1920,1080))
zentrum = (screen.get_width() / 2, screen.get_height() / 2)

clock = pg.time.Clock()
FPS = 40

#Zeichenschleife mit FPS Bildern pro Sekunde
while True:
  clock.tick(FPS)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT: quit()
  
  screen.fill('#000000')
  
  pg.display.flip()