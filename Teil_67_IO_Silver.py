import pygame as pg
import random as rnd
from math import floor

class Sprite(pg.sprite.Sprite):
  def __init__(self, nr, pos):
    super().__init__()
    self.nr = nr
    self.images = bilder[nr*2:nr*2+2]
    self.selektiert = False
    self.image = self.images[self.selektiert]
    self.rect = self.image.get_rect()
    self.rect.topleft = pos
    self.vel = (0,0)
    self.fusion = 1
        
  def change_selektiert(self):
    self.selektiert = not self.selektiert
    self.image = self.images[self.selektiert]

  def change_nr(self,nr):
    self.nr = nr
    self.images = bilder[nr*2:nr*2+2]
    self.image = self.images[self.selektiert]  
  
  def collidable(self, me, other):
    if me is other:
      return False
    else:
      return me.rect.colliderect(other.rect)  
  
  def update(self):
    if self.vel == (0,0): return
    new_pos = self.rect.move(self.vel)
    new_pos.x %= BREITE
    new_pos.y %= HÖHE
    for sprite in group_sprites:
      if sprite == self: continue
      if sprite.rect.colliderect(new_pos):
        # if sprite.nr < 6 and sprite.nr == self.nr:
        #   sprite.fusion += self.fusion
        #   group_sprites.remove(self)
        #   if sprite.fusion == 5:
        #     sprite.change_nr(6)
        # elif sprite.nr > 5 and self.nr > 5:
        #   sprite.fusion += self.fusion
        #   print(sprite.fusion)
        #   group_sprites.remove(self)
        #   if sprite.fusion == 10: sprite.change_nr(7)
        #   if sprite.fusion == 15: sprite.change_nr(8)
        #   if sprite.fusion == 20: sprite.change_nr(9)
        #else:  
          self.vel = (0,0)
          self.rect.x = round(self.rect.x / TILE[0]) * TILE[0]
          self.rect.y = round(self.rect.y / TILE[1]) * TILE[1]
          return
      else:
        self.rect = new_pos    
        

def sprite_clicked(sprite):
  sprite.change_selektiert()
  for s in group_sprites:
    if s.selektiert and s!= sprite: s.change_selektiert()

def move_selected(key):
  sprite = [sprite for sprite in group_sprites if sprite.selektiert]
  if sprite and sprite[0].vel == (0,0):
    sprite[0].vel = dirs[key]


pg.init()
BREITE, HÖHE = 1157, 747
RASTER = (13,9)
TILE = (BREITE / RASTER[0], HÖHE / RASTER[1])
clock = pg.time.Clock()
FPS = 40
zentrum = (BREITE / 2, HÖHE / 2)
screen = pg.display.set_mode((BREITE, HÖHE))

pfad = 'Teil_65_Bilder/'
bilder = [pg.image.load(f'{pfad}{n}{e}') for n in range(10) for e in ('_d.png', '_s.png')]
group_sprites = pg.sprite.Group()
dirs = {pg.K_w:(0,-20), pg.K_s:(0,20), pg.K_a:(-20,0), pg.K_d:(20,0)}
game_over = False

besetzt = set()
for n in range(30):
  while True:
    col, row = rnd.randrange(RASTER[0]), rnd.randrange(RASTER[1])
    if (col,row) not in besetzt:
      besetzt.add((col,row))
      break
  pos = (col*TILE[0], row*TILE[1])
  group_sprites.add(Sprite(n//5, pos))



while True:
  clock.tick(FPS)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT:
     quit()
    if ereignis.type == pg.MOUSEBUTTONDOWN:
      point = pg.mouse.get_pos()
      for sprite in group_sprites:
        if not sprite.rect.collidepoint(point): continue
        sprite_clicked(sprite)
    if ereignis.type == pg.KEYDOWN and ereignis.key in dirs:
      move_selected(ereignis.key)


  screen.fill('#000000')
  group_sprites.update()
  group_sprites.draw(screen)
  pg.display.flip()

pg.quit()