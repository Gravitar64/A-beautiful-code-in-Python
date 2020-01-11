from collections import Counter
import pygame as pg
import random as rnd
import time

time_start = time.perf_counter()

def nachbarn(pos):
  for x1, y1 in [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]:
    yield pos[0] + x1, pos[1] + y1

def neueGeneration(grid):
  anzNachbarn = Counter([p for pos in grid for p in nachbarn(pos)])
  grid = {pos for pos,anz in anzNachbarn.items() if anz == 3 or (anz == 2 and pos in grid)}
  return grid

def show(grid,rect):
  if not grid: return
  zell_breite, zell_höhe, offs_x, offs_y = rect
  for (x,y) in grid:
    pg.draw.rect(screen,(0,0,255), ((x+offs_x)*zell_breite+mouseOffsetX, (y+offs_y)*zell_höhe+mouseOffsetY, zell_breite,zell_höhe))

def spielfeldGröße(grid):
  Xs, Ys = zip(*grid)
  minX, maxX, minY, maxY = min(Xs), max(Xs), min(Ys), max(Ys)
  grid_breite, grid_höhe = (maxX - minX), (maxY - minY)
  zell_breite = screen_breite / (grid_breite)
  zell_höhe = screen_höhe / (grid_höhe)
  offs_x = - minX
  offs_y = - minX
  return zell_breite, zell_höhe, offs_x, offs_y

pg.init()
screen_breite, screen_höhe = 1000,1000
screen = pg.display.set_mode([screen_breite, screen_höhe])

spielfeld = {(rnd.randrange(200), rnd.randrange(200)) for _ in range(12000)}
feld_rect = spielfeldGröße(spielfeld)
mouseOffsetX = mouseOffsetY = 0
panning = False 


weitermachen = True
clock = pg.time.Clock()
generation = 0
while weitermachen:
  clock.tick(25)
  screen.fill((0,0,0))
  generation += 1
  show(spielfeld, feld_rect)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT or \
       (ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE):
      weitermachen = False
    if ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_SPACE:
      mouseOffsetX = mouseOffsetY = 0
      feld_rect = spielfeldGröße(spielfeld)
    if ereignis.type == pg.MOUSEBUTTONDOWN:
      if ereignis.button == 4:   
        feld_rect = list(map(lambda x : x*0.95, feld_rect))
        mouseOffsetX *= 0.95
        mouseOffsetY *= 0.95
      if ereignis.button == 5:   
        feld_rect = list(map(lambda x : x*1.05, feld_rect))
        mousePos = pg.mouse.get_pos()
        mouseOffsetX = mouseOffsetX * 1.05 
        mouseOffsetY = mouseOffsetY * 1.05 
      if ereignis.button == 1:
        panning = True
        pan_start_pos = pg.mouse.get_pos()
    if ereignis.type == pg.MOUSEBUTTONUP:
      if ereignis.button == 1 and panning:
        panning = False   
  if panning:
    mousePos = pg.mouse.get_pos()
    mouseOffsetX += (mousePos[0] - pan_start_pos[0]) 
    mouseOffsetY += (mousePos[1] - pan_start_pos[1]) 
    pan_start_pos = mousePos 
    
  spielfeld = neueGeneration(spielfeld)
  textfläche = pg.font.SysFont('impact', 28).render(f'#{len(spielfeld)}', False, (150,0,0))
  screen.blit(textfläche, (screen_breite // 2 - textfläche.get_width() // 2, 5))

  textfläche = pg.font.SysFont('impact', 24).render(f'Generation: {generation:,}', False, (150,0,0))
  screen.blit(textfläche, (5, 5))  

  pg.display.flip()

pg.quit()

