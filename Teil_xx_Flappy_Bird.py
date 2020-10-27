import pygame as pg
import requests, io
import random as rnd


def lade_bild(url):
  r = requests.get(url)
  bild = pg.image.load(io.BytesIO(r.content))
  return pg.transform.scale2x(bild)


def lade_sound(url):
  r = requests.get(url)
  return pg.mixer.Sound(io.BytesIO(r.content))


def scrolling(bild, x, y, delta, endlos):
  if endlos:
    if x < -BREITE:
      x = 0
    screen.blit(bild, (x+BREITE, y))
  screen.blit(bild, (x, y))
  return x - delta

def generiere_röhre():
  pos_y = rnd.randrange(400,800)
  röhren.append(b_röhre.get_rect(topleft=(700,pos_y)))
  röhren.append(b_röhre2.get_rect(topleft=(700,pos_y-850)))
  

class Vogel():
  def __init__(self):
    self.x = 100
    self.y = BREITE // 2
    self.grav = 1
    self.geschw = 0
    self.anim = 0

  def update(self):
    self.geschw += self.grav
    self.y += self.geschw  





pg.init()
BREITE, HÖHE = 576, 1024
screen = pg.display.set_mode((BREITE, HÖHE))
URL = 'https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/'
b_basis = lade_bild(URL+'sprites/base.png')
b_hintergrund = lade_bild(URL+'sprites/background-day.png')
b_röhre = lade_bild(URL+'sprites/pipe-green.png')
b_röhre2 = pg.transform.flip(b_röhre, False, True)
b_ende = lade_bild(URL+'sprites/gameover.png')
vögel = []
vögel.append(lade_bild(URL+'sprites/redbird-downflap.png'))
vögel.append(lade_bild(URL+'sprites/redbird-midflap.png'))
vögel.append(lade_bild(URL+'sprites/redbird-upflap.png'))
s_flug = lade_sound(URL+'audio/wing.wav')
s_punkt = lade_sound(URL+'audio/point.wav')
s_wand = lade_sound(URL+'audio/hit.wav')

hintergrund_x = basis_x = score = highscore = 0
weitermachen = True
clock = pg.time.Clock()
röhren = []
e_röhre = pg.USEREVENT
pg.time.set_timer(e_röhre, 1400)
e_anim = e_röhre+1
pg.time.set_timer(e_anim, 100)
spielende = False

vogel = Vogel()

while weitermachen:
  clock.tick(40)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT:
      weitermachen = False
    if ereignis.type == e_röhre:
      generiere_röhre()
    if ereignis.type == e_anim:
      vogel.anim = (vogel.anim + 1) % 3
    if ereignis.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[0]:
      vogel.geschw = -15
      s_flug.play()
      if spielende:
        spielende = False
        vogel = Vogel()
        röhren.clear()
        score = 0

  screen.fill((0, 0, 0))
  hintergrund_x = scrolling(b_hintergrund, hintergrund_x, 0, 1, True)
  if not spielende:
    for röhre in röhren:
      x,y = röhre.topleft
      bild = b_röhre if röhre[1] > 399 else b_röhre2
      röhre.left = scrolling(bild,x,y, 10, False)
      if x == -10:
        score += 0.5
        s_punkt.play()
    vogel.update()
    screen.blit(vögel[vogel.anim],(vogel.x, vogel.y))
    vogel_rect = vögel[vogel.anim].get_rect(topleft = (vogel.x, vogel.y))
    if vogel_rect.collidelist(röhren) > -1 or \
       vogel_rect.bottom > 900 or \
       vogel_rect.top < 0:  
      s_wand.play()
      spielende = True
  else:
    screen.blit(b_ende,(100,400))
    textsurface = pg.font.SysFont('impact',40).render(f'HIGH-SCORE      {highscore:.0f}', False, (255,255,255))
    screen.blit(textsurface,(160,10))

  basis_x = scrolling(b_basis, basis_x, 900, 10, True)
  textsurface = pg.font.SysFont('impact',40).render(f'{score:.0f}', False, (255,255,255))
  screen.blit(textsurface,(275,100))
  highscore = max(score, highscore)

  pg.display.flip()

pg.quit()
