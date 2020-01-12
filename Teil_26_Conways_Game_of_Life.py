import pygame as pg 
import random as rnd
from collections import Counter 

def zellGröße(spielfeld, breite, höhe):
  Xs, Ys = zip(*spielfeld)
  minx, maxx, miny, maxy = min(Xs), max(Xs), min(Ys), max(Ys)
  spalten, zeilen = maxx-minx + 1, maxy-miny + 1
  return breite / spalten, höhe / zeilen

def nachbarn(pos):
  for x1, y1 in [(-1,-1), (0,-1), (1,-1),
                 (-1,0),          (1,0),
                 (-1,1),  (0,1),  (1,1)]:
    yield pos[0]+x1, pos[1] + y1               


def neueGeneration(spielfeld):
  anzNachbarn =  Counter([p for pos in spielfeld for p in nachbarn(pos)])
  spielfeld = {pos for pos, anz in anzNachbarn.items() if anz == 3 or (anz == 2 and pos in spielfeld)}
  return spielfeld 


spielfeld = {(rnd.randrange(200), rnd.randrange(200)) for _ in range(6000)}

pg.init()
sc_b = sc_h = 1000
screen = pg.display.set_mode([sc_b, sc_h])
zb, zh = zellGröße(spielfeld, sc_b, sc_h)


while True:
  screen.fill((0,0,0))
  spielfeld = neueGeneration(spielfeld)
  for zelle in spielfeld:
    pg.draw.rect(screen, (0,0,255), (zelle[0]*zb, zelle[1]*zh, zb, zh))
  pg.display.flip()
pg.quit()

