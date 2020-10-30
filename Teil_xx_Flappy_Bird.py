import pygame as pg, random as rnd
import requests, io


def lade_bild(url):
  return pg.transform.scale2x(pg.image.load(io.BytesIO(requests.get(url).content)).convert_alpha())
  

def lade_sound(url):
  return pg.mixer.Sound(io.BytesIO(requests.get(url).content))


def endlos_scrolling(bild, x, y, geschw):
  x = x % -BREITE
  screen.blit(bild, (x, y))
  screen.blit(bild, (x+BREITE, y))
  return x-geschw


def generiere_röhre():
  röhren.append(b_röhre_unten.get_rect(topleft=(700, y := rnd.randrange(400, 800))))
  röhren.append(b_röhre_oben.get_rect(topleft=(700, y-850)))


def zeichne_Text(text, pos):
  screen.blit(pg.font.SysFont('impact', 40).render(text, False, (255, 255, 255)), pos)


pg.init()
BREITE, HÖHE = 576, 1024
screen = pg.display.set_mode((BREITE, HÖHE))

URL1 = 'https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/sprites/'
URL2 = 'https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/audio/'
b_hintergrund = lade_bild(URL1+'background-day.png')
b_basis = lade_bild(URL1+'base.png')
b_vögel = [lade_bild(URL1+'redbird-downflap.png'),
           lade_bild(URL1+'redbird-midflap.png'),
           lade_bild(URL1+'redbird-upflap.png')]
b_röhre_unten = lade_bild(URL1+'pipe-green.png')
b_spielende = lade_bild(URL1+'gameover.png')
b_röhre_oben = pg.transform.flip(b_röhre_unten, False, True)
s_flug = lade_sound(URL2+'wing.wav')
s_punkt = lade_sound(URL2+'point.wav')
s_wand = lade_sound(URL2+'hit.wav')


hintergrund_x = basis_x = score = highscore = 0
vogel_anim, vogel_grav, vogel_geschw, vogel_y = 0, 1, 0, HÖHE//2
röhren = []
spielstatus = True

e_anim = pg.USEREVENT
pg.time.set_timer(e_anim, 100)
e_röhre = pg.USEREVENT+1
pg.time.set_timer(e_röhre, 1400)

weitermachen = True
clock = pg.time.Clock()

while weitermachen:
  clock.tick(40)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT:
      weitermachen = False
    if ereignis.type == e_anim:
      vogel_anim = (vogel_anim + 1) % 3
    if ereignis.type == e_röhre:
      generiere_röhre()
    if ereignis.type == pg.MOUSEBUTTONDOWN:
      vogel_geschw = -15; s_flug.play()
      if not spielstatus:
        spielstatus = True; röhren.clear(); vogel_y = HÖHE//2; score = 0
  screen.fill((0, 0, 0))
  hintergrund_x = endlos_scrolling(b_hintergrund, hintergrund_x, 0, 1)
  if spielstatus:
    for röhre in reversed(röhren):
      bild = b_röhre_unten if röhre.y > 399 else b_röhre_oben
      screen.blit(bild, röhre)
      röhre.x -= 10
      if röhre.x == -10:
        score += 0.5; s_punkt.play()
      if röhre.x < -100:
        röhren.remove(röhre)
    vogel_geschw += vogel_grav; vogel_y += vogel_geschw
    vogel_rect = b_vögel[vogel_anim].get_rect(topleft=(100, vogel_y))
    screen.blit(b_vögel[vogel_anim], vogel_rect)
    if vogel_rect.collidelist(röhren) != -1 or vogel_rect.top < 0 or vogel_rect.bottom > 900:
      spielstatus = False; s_wand.play() 
  else:
    screen.blit(b_spielende, (100, 400))
    zeichne_Text(f'HIGH-SCORE      {highscore:.0f}', (160, 10))

  zeichne_Text(f'{score:.0f}', (275, 100))
  basis_x = endlos_scrolling(b_basis, basis_x, 900, 10)
  highscore = max(highscore, score)
  pg.display.flip()
