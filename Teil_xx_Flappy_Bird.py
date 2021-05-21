import pygame as pg, random as rnd
import requests, io
import arrow
import Teil_17_pygame_functions as pgf
import pickle


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
  global platz, plätze
  röhren.append(b_röhre_unten.get_rect(topleft=(700, y := rnd.randrange(400, 800))))
  röhren.append(b_röhre_oben.get_rect(topleft=(700, y-850)))
  if rang != platz:
    plätze.append([rang,740,y+50])
    platz = rang
  
def generiere_high_score_platzierungen(highscore_liste):
  platzierungen = {}
  plätze = list(set([x[0] for x in highscore_liste]))
  for p in plätze:
    platzierungen[p] = [x[0] for x in highscore_liste].index(p)+1
  return platzierungen  


def zeichne_Text(text, pos, farbe):
  screen.blit(pg.font.SysFont('impact', 40).render(text, False, farbe), pos)


pg.init()
BREITE, HÖHE = 576, 1024
screen = pgf.screenSize(BREITE, HÖHE)

scores = []
highscore_datei = 'teil_xx_flappy_highscores_new.pkl'
with open(highscore_datei,'rb') as f:
  scores = pickle.load(f)
platzierungen = generiere_high_score_platzierungen(scores)

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


inputBox = pgf.makeTextBox(190,250,200,0,'Dein Name?')
heute = arrow.now().format('DD.MM.YY')
hintergrund_x = basis_x = score = 0
vogel_anim, vogel_grav, vogel_geschw, vogel_y = 0, 1, 0, HÖHE//2
röhren = []
plätze = []
spielstatus = False
name = ''
platz, rang, platz_x = -1, -1, -900 

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
      with open(highscore_datei,'wb') as f:
          pickle.dump(scores[:10], f)
    if ereignis.type == e_anim:
      vogel_anim = (vogel_anim + 1) % 3
    if ereignis.type == e_röhre:
      generiere_röhre()
    if ereignis.type == pg.MOUSEBUTTONDOWN:
      if spielstatus and ereignis.button == 1:
        vogel_geschw = -15; s_flug.play()
      if ereignis.button == 3 and not spielstatus:
        spielstatus = True; röhren.clear(); vogel_y = HÖHE//2; score = 0; 
        vogel_geschw = -15
        platz, rang, platz_x = -1, -1, -900
        plätze.clear()
        scores = scores[:10]
  hintergrund_x = endlos_scrolling(b_hintergrund, hintergrund_x, 0, 1)
  if spielstatus:
    for röhre in reversed(röhren):
      bild = b_röhre_unten if röhre.y > 399 else b_röhre_oben
      screen.blit(bild, röhre)
      röhre.x -= 10
      if röhre.x == -10:
        score += 0.5; s_punkt.play().set_volume(0.1)
      if röhre.x < -100:
        röhren.remove(röhre)
    score = int(score)
    if score+2 in platzierungen:
      rang = platzierungen[score+2]
    for p in reversed(plätze):
      zeichne_Text(f'{p[0]}', (p[1], p[2]), '#0e6b0e')
      p[1] -= 10
      if p[1] < -100:
        plätze.remove(p)

    vogel_geschw += vogel_grav; vogel_y += vogel_geschw
    vogel_rect = b_vögel[vogel_anim].get_rect(topleft=(100, vogel_y))
    screen.blit(b_vögel[vogel_anim], vogel_rect)
    if vogel_rect.collidelist(röhren) != -1 or vogel_rect.top < 0 or vogel_rect.bottom > 900:
      spielstatus = False; s_wand.play()
      if len(scores) < 10 or int(score) > scores[-1][0]:
        if name == '':
          zeichne_Text('Super! Du bis in den TOP 10!',(50,150), (255,255,255))
          name = pgf.textBoxInput(inputBox)
        scores.append([score, name, heute])
        scores = sorted(scores, reverse=True)
        with open(highscore_datei,'wb') as f:
          pickle.dump(scores[:10], f)
        platzierungen = generiere_high_score_platzierungen(scores[:10])     
  else:
    screen.blit(b_spielende, (100, 10))
    zeichne_Text(f'HIGH-SCORES', (180, 200) ,(255,244,135))
    ty, counter = 280,0
    for s, n, d in scores[:10]:
      if s == score and n == name and d == heute and counter == 0 and score > scores[-1][0]:
        farbe = (255,244,135)
        counter += 1
      else:
         farbe = '#0e6b0e'
      zeichne_Text(f'{n}', (50,ty), farbe)
      zeichne_Text(f'{d}', (250,ty), farbe)
      zeichne_Text(f'{s}', (450,ty), farbe)
      ty += 50
  zeichne_Text(f'{score:.0f}', (BREITE//2-5, 130), (255,255,255))
  basis_x = endlos_scrolling(b_basis, basis_x, 900, 10)
  pg.display.flip()
