import pygame as pg
import requests
import io, sys, random as rnd


def lade_bild(url):
  r = requests.get(url)
  return pg.transform.scale2x(pg.image.load(io.BytesIO(r.content)).convert())

def lade_sound(url):
  r = requests.get(url)
  return pg.mixer.Sound(io.BytesIO(r.content))  
  

def scrolling(bild,x,y,betrag,endlos):
  if endlos:
    x = x % -576
    screen.blit(bild,(x+576,y))
  screen.blit(bild,(x,y))
  return x-betrag

pg.init()
screen = pg.display.set_mode((576,1024))

#bilder laden
b_basis = lade_bild('https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/sprites/base.png')
b_hintergrund = lade_bild('https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/sprites/background-day.png')
b_pipe = lade_bild('https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/sprites/pipe-green.png')
b_pipe2 = pg.transform.flip(b_pipe, False, True)
b_gameover = pg.transform.scale2x(pg.image.load('Teil_xx_FB_game_over.png')).convert_alpha()
birds = []
birds.append(lade_bild('https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/sprites/redbird-downflap.png'))
birds.append(lade_bild('https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/sprites/redbird-midflap.png'))
birds.append(lade_bild('https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/sprites/redbird-upflap.png'))

#sounds laden
s_flap = lade_sound('https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/audio/wing.wav')
s_point = lade_sound('https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/audio/point.wav')
s_die = lade_sound('https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/audio/hit.wav')



clock = pg.time.Clock()
basis_scroll = hintergrund_scroll = bird_anim = score = highscore = 0
game_over = False
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
    if ereignis.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[0]: 
      bird_vel = -15
      s_flap.play()
      if game_over:
        game_over = False
        bird_posy = 512
        pipes = []
        score = 0
    if ereignis.type == birdflap: bird_anim = (bird_anim + 1) % 3
    if ereignis.type == pipespawn: 
      pos_y = rnd.randrange(400,800)
      pipes.append(b_pipe.get_rect(topleft =(700,pos_y)))
      pipes.append(b_pipe2.get_rect(topleft = (700,pos_y-850)))
  screen.fill((0,0,0))
  hintergrund_scroll = scrolling(b_hintergrund,hintergrund_scroll,0,1,True)
  if not game_over:
    bird_rect = birds[bird_anim].get_rect(topleft = (100,bird_posy))
    if  bird_rect.collidelist(pipes) > -1 or \
        bird_rect.bottom > 900 or \
        bird_rect.top < 0:
      s_die.play()  
      game_over = True
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
      if x == 60: 
        score += 0.5
        s_point.play()
    textsurface = pg.font.SysFont('impact', 40).render(f'{score:.0f}', False, (255, 255, 255))
    screen.blit(textsurface, (275,100))    
  else:
    screen.blit(b_gameover,(100,400))
    textsurface = pg.font.SysFont('impact', 40).render(f'HIGH-SCORE    {highscore:.0f}', False, (255, 255, 255))
    screen.blit(textsurface, (100,30))

  
  basis_scroll = scrolling(b_basis,basis_scroll,900,10,True)
  highscore = max(highscore, score)
  pg.display.flip()