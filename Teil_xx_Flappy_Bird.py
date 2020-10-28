import pygame as pg, random as rnd
import requests, io


def lade_bild(url):
  r = requests.get(url)
  bild = pg.image.load(io.BytesIO(r.content))
  return pg.transform.scale2x(bild).convert_alpha()


def lade_sound(url):
  r = requests.get(url)
  return pg.mixer.Sound(io.BytesIO(r.content))


def generiere_röhre():
  pos_y = rnd.randrange(400, 800)
  röhren.append(Röhre((700, pos_y), (-10,0), b_röhre_unten))
  röhren.append(Röhre((700, pos_y-850), (-10,0), b_röhre_oben))


def zeichne_Text(text, pos):
  textsurface = pg.font.SysFont('impact', 40).render(
      text, False, (255, 255, 255))
  screen.blit(textsurface, pos)


class Element():
  def __init__(self, pos, delta, bild):
    self.pos = pg.Vector2(pos)
    self.delta = pg.Vector2(delta)
    self.bild = bild
    
class Hintergrund(Element):
  def update_show(self):
    self.pos += self.delta
    self.pos.x = self.pos.x % -BREITE
    screen.blit(self.bild,self.pos)
    screen.blit(self.bild,self.pos+pg.Vector2(BREITE,0))

class Röhre(Element):
  def __init__(self, pos, delta, bild):
    Element.__init__(self, pos, delta, bild)
    self.rect = None

  def update_show(self):
    self.pos += self.delta
    self.rect = self.bild.get_rect(topleft=self.pos)
    screen.blit(self.bild,self.rect)

class Vogel(Element):
  def __init__(self, pos, delta, bild):
    Element.__init__(self, pos, delta, bild)
    self.grav = pg.Vector2(0,1)
    self.rect = None
    self.anim = 0

  def update_show(self):
    self.delta += self.grav
    self.pos += self.delta
    self.rect = self.bild[self.anim].get_rect(topleft=self.pos)
    screen.blit(self.bild[self.anim],self.rect)

  def flap(self):
    self.delta.y = -15
    s_flug.play()

  def animation(self):
    self.anim = (self.anim + 1) % 3    

pg.init()
BREITE, HÖHE = 576, 1024
screen = pg.display.set_mode((BREITE, HÖHE))
URL = 'https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/'
basis = Hintergrund((0,900), (-10,0), lade_bild(URL+'sprites/base.png'))
hintergrund = Hintergrund((0,0), (-1,0), lade_bild(URL+'sprites/background-day.png'))
b_röhre_unten = lade_bild(URL+'sprites/pipe-green.png')
b_röhre_oben = pg.transform.flip(b_röhre_unten, False, True)
b_ende = lade_bild(URL+'sprites/gameover.png')
vögel = []
vögel.append(lade_bild(URL+'sprites/redbird-downflap.png'))
vögel.append(lade_bild(URL+'sprites/redbird-midflap.png'))
vögel.append(lade_bild(URL+'sprites/redbird-upflap.png'))
s_flug = lade_sound(URL+'audio/wing.wav')
s_punkt = lade_sound(URL+'audio/point.wav')
s_wand = lade_sound(URL+'audio/hit.wav')

score = highscore = 0
weitermachen = True
clock = pg.time.Clock()
röhren = []
e_röhre = pg.USEREVENT
pg.time.set_timer(e_röhre, 1400)
e_anim = e_röhre+1
pg.time.set_timer(e_anim, 100)
spielende = False
vogel = Vogel((100,HÖHE//2), (0,0), vögel)
while weitermachen:
  clock.tick(40)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT:
      weitermachen = False
    if ereignis.type == e_röhre:
      generiere_röhre()
    if ereignis.type == e_anim:
      vogel.animation()
    if ereignis.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[0]:
      vogel.flap()
      if spielende:
        spielende = False
        vogel = Vogel((100,HÖHE//2), (0,0), vögel)
        röhren.clear()
        score = 0

  screen.fill((0, 0, 0))
  hintergrund.update_show()
  if not spielende:
    for röhre in reversed(röhren):
      röhre.update_show()
      if röhre.pos.x == -10:
        score += 0.5
        s_punkt.play()
      if röhre.pos.x < -100:
        röhren.remove(röhre)
    vogel.update_show()
    if vogel.rect.collidelist([r.rect for r in röhren]) > -1 or \
       vogel.rect.bottom > 900 or \
       vogel.rect.top < 0:
      s_wand.play()
      spielende = True
  else:
    screen.blit(b_ende, (100, 400))
    zeichne_Text(f'HIGH-SCORE      {highscore:.0f}', (160, 10))
  basis.update_show()
  zeichne_Text(f'{score:.0f}', (275, 100))
  highscore = max(score, highscore)
  pg.display.flip()
pg.quit()
