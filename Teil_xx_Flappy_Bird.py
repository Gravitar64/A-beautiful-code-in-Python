import pygame as pg, random as rnd
import requests, io


def lade_bild(url):
  r = requests.get(url)
  bild = pg.image.load(io.BytesIO(r.content))
  return pg.transform.scale2x(bild).convert_alpha()


def lade_sound(url):
  r = requests.get(url)
  return pg.mixer.Sound(io.BytesIO(r.content))


def scrolling(bild, x, y, delta_x, endlos):
  if endlos:
    x = x % - BREITE
    screen.blit(bild, (x+BREITE, y))
  screen.blit(bild, (x, y))
  return x - delta_x


def generiere_röhre():
  pos_y = rnd.randrange(400, 800)
  röhren.append(b_röhre_unten.get_rect(topleft=(700, pos_y)))
  röhren.append(b_röhre_oben.get_rect(topleft=(700, pos_y-850)))


def zeichne_Text(text, pos):
  textsurface = pg.font.SysFont('impact', 40).render(text, False, (255, 255, 255))
  screen.blit(textsurface, pos)

pg.init()
BREITE, HÖHE = 576, 1024
screen = pg.display.set_mode((BREITE, HÖHE))

URL           = 'https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/'
b_basis       = lade_bild(URL+'sprites/base.png')
b_hintergrund = lade_bild(URL+'sprites/background-day.png')
b_röhre_unten = lade_bild(URL+'sprites/pipe-green.png')
b_röhre_oben  = pg.transform.flip(b_röhre_unten, False, True)
b_ende        = lade_bild(URL+'sprites/gameover.png')
b_vögel       = [lade_bild(URL+'sprites/redbird-downflap.png'), 
                 lade_bild(URL+'sprites/redbird-midflap.png'), 
                 lade_bild(URL+'sprites/redbird-upflap.png')]
s_flug        = lade_sound(URL+'audio/wing.wav')
s_punkt       = lade_sound(URL+'audio/point.wav')
s_wand        = lade_sound(URL+'audio/hit.wav')

score = highscore = basis_x = hintergrund_x = 0
vogel_y, vogel_grav, vogel_geschw, vogel_anim = HÖHE//2, 1, 0, 0
röhren = []
spielende = False
weitermachen = True

e_röhre = pg.USEREVENT
pg.time.set_timer(e_röhre, 1400)
e_anim = e_röhre+1
pg.time.set_timer(e_anim, 100)

clock = pg.time.Clock()
while weitermachen:
  clock.tick(40)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT:
      weitermachen = False
    if ereignis.type == e_röhre:
      generiere_röhre()
    if ereignis.type == e_anim:
      vogel_anim = (vogel_anim + 1) % 3
    if ereignis.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[0]:
      vogel_geschw = -15
      s_flug.play()
      if spielende:
        spielende = False
        vogel_y = HÖHE//2
        röhren.clear()
        score = 0
  
  screen.fill((0, 0, 0))
  hintergrund_x = scrolling(b_hintergrund, hintergrund_x, 0, 1, True)
  if not spielende:
    for rect in reversed(röhren):
      bild = b_röhre_unten if rect.top > 399 else b_röhre_oben
      rect.x = scrolling(bild, rect.x, rect.y, 10, False)
      if rect.x == -10:
        score += 0.5
        s_punkt.play()
      if rect.x < -100:
        röhren.remove(rect)
    
    vogel_geschw += vogel_grav
    vogel_y += vogel_geschw
    screen.blit(b_vögel[vogel_anim], (100, vogel_y))
    vogel_rect = b_vögel[vogel_anim].get_rect(topleft=(100, vogel_y))
    
    if vogel_rect.collidelist(röhren) > -1 or \
        vogel_rect.bottom > 900 or \
        vogel_rect.top < 0:
      s_wand.play()
      spielende = True
  else:
    screen.blit(b_ende, (100, 400))
    zeichne_Text(f'HIGH-SCORE      {highscore:.0f}', (160, 10))

  basis_x = scrolling(b_basis, basis_x, 900, 10, True)
  zeichne_Text(f'{score:.0f}', (275, 100))
  highscore = max(score, highscore)
  pg.display.flip()
pg.quit()
