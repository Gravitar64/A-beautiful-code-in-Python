from collections import Counter
import pygame as pg
import random as rnd 

def nachbarn(pos):
  for dx, dy in [(-1,-1), (0,-1), (1,-1),
                 (-1, 0),         (1, 0),
                 (-1, 1), (0, 1), (1, 1)]:
    yield pos[0] + dx, pos[1] + dy

def nächsteGeneration(spielfeld):
  nachb = Counter([pos for zelle in spielfeld for pos in nachbarn(zelle)]) 
  return {pos for pos,anz in nachb.items() if anz == 3 or (anz==2 and pos in spielfeld)}

def größeErmitteln(spielfeld, breite, höhe):
  Xs, Ys = zip(*spielfeld)
  minX, maxX, minY, maxY = min(Xs), max(Xs), min(Ys), max(Ys)
  spalten, zeilen = maxX - minX + 1, maxY - minY + 1
  return breite / spalten, höhe/ zeilen, -minX, -minY                   

spielfeld = {(rnd.randrange(200), rnd.randrange(200)) for i in range(6000)}

pg.init()
sc_b = sc_h = 1000
screen = pg.display.set_mode([sc_b, sc_h])
zb, zh, offsX, offsY = größeErmitteln(spielfeld, sc_b, sc_h)
fps=40
clock = pg.time.Clock()


while True:
  clock.tick(fps)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT or ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE: quit()
  screen.fill((0,0,0))
  spielfeld = nächsteGeneration(spielfeld)
  for x,y in spielfeld:
    pg.draw.rect(screen,'white', ((x+offsX)*zb,(y+offsY)*zh, zb, zh))
  pg.display.flip()

pg.quit()

