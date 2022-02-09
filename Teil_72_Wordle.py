import pygame as pg
import random as rnd

COLORS = {-1: ('#ffffff', '#000000'),
           0: ('#787C7E', '#ffffff'),
           1: ('#C9B458', '#ffffff'),
           2: ('#6AAA64', '#ffffff'),
           3: ('#D3D6DA', '#000000')}


class Feld():
  def __init__(self, rect):
    self.rect = pg.Rect(rect)
    self.char = ''
    self.state = -1
    self.img = generiere_bild(self.rect.w, self.rect.h, self.char, self.state)

  def change_state(self, state):
    self.state = state
    self.img = generiere_bild(self.rect.w, self.rect.h, self.char, self.state)

  def change_char(self, char):
    self.char = char
    self.img = generiere_bild(self.rect.w, self.rect.h, self.char, self.state)


def generiere_bild(breite, höhe, buchstabe, state):
  bild = pg.Surface((breite, höhe))
  bild_rect = bild.get_rect()
  farbe_hg, farbe_txt = COLORS[state]
  pg.draw.rect(bild, farbe_hg, bild_rect)
  
  if state == -1:
    pg.draw.rect(bild, '#D3D6DA', (0, 0, breite, höhe), 3)
  
  if buchstabe != '':
    text = pg.font.SysFont('Arial_bold', 32).render(buchstabe, True, farbe_txt)
    text_rect = text.get_rect(center=bild_rect.center)
    bild.blit(text, text_rect)
  
  return bild


def eingabe(key):
  global cursor, cursor_min, cursor_max
  
  if key == pg.K_BACKSPACE:
    if cursor == cursor_min: return
    cursor -= 1
    felder[cursor].change_char('')
  
  elif key == pg.K_RETURN:
    if cursor != cursor_max: return
    versuch = ''.join(f.char for f in felder[cursor_min:cursor_max])
    if versuch not in wörter: return
    pos = prüfe_versuch(versuch)
    for i, (p, c) in enumerate(zip(pos, versuch)):
      feld = felder[cursor_min+i]
      feld.change_state(p)
      if c in offen:
        offen[offen.index(c)] = '*'
    cursor_min = cursor
    cursor_max = cursor_min + 5
    if cursor_max > 30:
      print(geheim)
  
  else:
    if cursor == cursor_max: return
    felder[cursor].change_char(chr(ereignis.key).upper())
    cursor += 1


def generiere_5_buchstaben_liste(datei):
  with open(datei) as f:
    return [w.strip().upper() for w in f if len(w.strip()) == 5]


def prüfe_versuch(versuch):
  pos = [0]*5
  bv, bg = list(versuch), list(geheim)
  for i in range(len(bv)):
    if bv[i] != bg[i]: continue
    pos[i] = 2
    bv[i] = bg[i] = '*'
  for i, b in enumerate(bv):
    if b == '*': continue
    if b in bg:
      pos[i] = 1
      bg[bg.index(b)] = '*'
  return pos

def generiere_felder():
  felder = []
  for i in range(30):
    x, y = i % 5 * 50 + 352, i // 5 * 50 + 80
    felder.append(Feld((x, y, 45, 44)))
  return felder    


pg.init()
screen = pg.display.set_mode((920, 647))
bild = pg.image.load('teil_72_wordle.jpg')

wörter = generiere_5_buchstaben_liste('Teil_72_Wörter.txt')
geheim = rnd.choice(wörter)

felder = generiere_felder()
offen = [chr(x) for x in range(65, 91)]
cursor, cursor_min, cursor_max = 0, 0, 5


clock = pg.time.Clock()
FPS = 20

while True:
  clock.tick(FPS)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT: quit()
    if ereignis.type == pg.KEYDOWN:
      eingabe(ereignis.key)

  screen.blit(bild, (0, 0))
  
  for f in felder:
    screen.blit(f.img, (f.rect.x, f.rect.y))
  
  for i, o in enumerate(offen):
    if o == '*':
      continue
    x, y = i % 13 * 50 + 152, i // 13 * 50 + 500
    taste = generiere_bild(45, 44, o, 3)
    screen.blit(taste, (x, y))
  
  pg.display.flip()
