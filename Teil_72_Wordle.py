import pygame as pg
import random as rnd


class Feld:

  STATI =  {0: ('#ffffff', '#000000'),
            1: ('#787C7E', '#ffffff'),
            2: ('#C9B458', '#ffffff'),
            3: ('#6AAA64', '#ffffff'),
            4: ('#D3D6DA', '#000000')}

  def __init__(self, x, y, buchst, status):
    self.rect = pg.Rect(x, y, 45, 44)
    self.buchst = buchst
    self.status = status

  @property
  def bild(self):
    b_hg = pg.Surface(self.rect.size)
    b_hg_rect = b_hg.get_rect()
    hg, vg = self.STATI[self.status]
    pg.draw.rect(b_hg, hg, b_hg_rect)
    
    if self.status == 0:
      pg.draw.rect(b_hg, '#D3D6DA', b_hg_rect, 3)
    
    if self.buchst != '':
      b_vg = pg.font.SysFont('Arial_bold', 32).render(self.buchst, True, vg)
      b_vg_rect = b_vg.get_rect(center=b_hg_rect.center)
      b_hg.blit(b_vg, b_vg_rect)
    return b_hg


def generiere_felder():
  eingaben, buchstaben = [], {}
  for i in range(30):
    x, y = i % 5 * 50 + 352, i // 5 * 50 + 80
    eingaben.append(Feld(x, y, '', 0))
  for i in range(26):
    x, y = i % 13 * 50 + 152, i // 13 * 50 + 500
    buchstaben[chr(65+i)] = Feld(x, y, chr(65+i), 4)
  return eingaben, buchstaben


def vergleich(geheim, versuch):
  for i in range(5):
    if versuch[i] == geheim[i]:
      versuch[i] = geheim[i] = 3
  
  for i, b in enumerate(versuch):
    if b == 3: continue
    if b in geheim:
      versuch[i] = 2
      geheim[geheim.index(b)] = 2
    else:
      versuch[i] = 1
  return versuch


def zeichne_felder():
  screen.blit(bild, (0, 0))
  for feld in eingaben:
    screen.blit(feld.bild, feld.rect.topleft)
  for feld in buchstaben.values():
    screen.blit(feld.bild, feld.rect.topleft)
  pg.display.flip()


def eingabe(key):
  global cursor, cursor_min, cursor_max
  if key == pg.K_BACKSPACE:
    if cursor == cursor_min: return
    cursor -= 1
    eingaben[cursor].buchst = ''
  
  elif key == pg.K_RETURN:
    if cursor != cursor_max: return
    versuch = ''.join(f.buchst for f in eingaben[cursor_min:cursor_max])
    if versuch not in wörter: return
    stati = vergleich(list(geheim), list(versuch))
    for i,status in enumerate(stati):
      eingaben[cursor_min+i].status = status
      buchstaben[versuch[i]].buchst = ''
      buchstaben[versuch[i]].status = 0
    cursor_min, cursor_max = cursor, cursor + 5
    if cursor_max > 30:
      print(geheim)
  
  elif cursor < cursor_max:
    eingaben[cursor].buchst = chr(key).upper()
    cursor += 1


pg.init()
screen = pg.display.set_mode((920, 647))
bild = pg.image.load('Teil_72_Wordle.jpg')
with open('Teil_72_wörter.txt') as f:
  wörter = [w.strip() for w in f]
geheim = rnd.choice(wörter)
eingaben, buchstaben = generiere_felder()
zeichne_felder()
cursor, cursor_min, cursor_max = 0,0,5

clock = pg.time.Clock()
FPS = 20

while True:
  clock.tick(FPS)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT: quit()
    if ereignis.type == pg.KEYDOWN:
      eingabe(ereignis.key)
      zeichne_felder()