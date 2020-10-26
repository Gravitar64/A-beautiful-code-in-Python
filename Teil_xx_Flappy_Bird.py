import pygame as pg
import requests
import io, sys, random as rnd


def lade_bild(url):
  r = requests.get(url)
  return pg.transform.scale2x(pg.image.load(io.BytesIO(r.content)).convert())
  

def scrolling(bild,x,y,betrag,endlos):
  if endlos:
    x = x % -576
    screen.blit(bild,(x+576,y))
  screen.blit(bild,(x,y))
  return x-betrag

pg.init()
screen = pg.display.set_mode((576,1024))


b_basis = (lade_bild('https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/sprites/base.png'))
b_hintergrund = (lade_bild('https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/sprites/background-day.png'))
b_pipe = (lade_bild('https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/sprites/pipe-green.png'))
b_pipe2 = pg.transform.flip(b_pipe, False, True)
birds = []
birds.append(lade_bild('https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/sprites/redbird-downflap.png'))
birds.append(lade_bild('https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/sprites/redbird-midflap.png'))
birds.append(lade_bild('https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/sprites/redbird-upflap.png'))


clock = pg.time.Clock()
basis_scroll = hintergrund_scroll = bird_anim = score = 0
pipes = []
bird_posy = 512
bird_grav = 1
bird_vel = 0
birdflap = pg.USEREVENT
pipespawn = birdflap + 1
pg.time.set_timer(birdflap,100)
pg.time.set_timer(pipespawn,1400)


while True:
  clock.tick(40)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT: sys.exit()
    if ereignis.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[0]: bird_vel = -15
    if ereignis.type == birdflap: bird_anim = (bird_anim + 1) % 3
    if ereignis.type == pipespawn: 
      pos_y = rnd.randrange(400,800)
      pipes.append(b_pipe.get_rect(topleft =(700,pos_y)))
      pipes.append(b_pipe2.get_rect(topleft = (700,pos_y-850)))



  screen.fill((0,0,0))
  hintergrund_scroll = scrolling(b_hintergrund,hintergrund_scroll,0,1,True)
  bird_vel += bird_grav; bird_posy += bird_vel
  screen.blit(birds[bird_anim],(100,bird_posy))
  for pipe in reversed(pipes):
    x,y = pipe.topleft
    if y > 399:
      pipe.topleft = (scrolling(b_pipe, x, y, 10, False), y)
    else:
      pipe.topleft = (scrolling(b_pipe2, x, y, 10, False), y)  
    if x < - 100:
      pipes.remove(pipe)
    if x == 80: 
      score += 0.5
  bird_rect = birds[bird_anim].get_rect(topleft = (100,bird_posy))
  if  bird_rect.collidelist(pipes) > -1:
    sys.exit()   
        
  basis_scroll = scrolling(b_basis,basis_scroll,900,10,True)
  pg.display.flip()