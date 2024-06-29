import itertools as itt
import time
import pygame as pg


fenster = pg.display.set_mode((200,400))
fenster_rect = fenster.get_rect()
bilder = [pg.image.load('Ampel'+str(i)+'.png').convert_alpha() for i in range(4)]

for i, t in itt.cycle(enumerate([20, 3, 30, 2])):
  bild_rect = bilder[i].get_rect(center=fenster_rect.center)
  fenster.blit(bilder[i],bild_rect)
  pg.display.flip()
  time.sleep(t)
