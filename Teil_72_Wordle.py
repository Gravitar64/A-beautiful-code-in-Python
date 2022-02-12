import pygame as pg
import random as rnd


class Feld:

  FARBEN = {-1: ('#ffffff', '#000000'),
            0: ('#787C7E', '#ffffff'),
            1: ('#C9B458', '#ffffff'),
            2: ('#6AAA64', '#ffffff'),
            3: ('#D3D6DA', '#000000')}

  def __init__(self, rect, char, state):
    self.rect = pg.Rect(rect)
    self.char = char
    self.state = state
    self.img = self.render()

  def change_char(self, char):
    self.char = char
    self.img = self.render()

  def change_state(self, state):
    self.state = state
    self.img = self.render()

  def render(self):
    bild = pg.Surface(self.rect.size)
    bild_rect = bild.get_rect()
    farbe_hg, farbe_txt = self.FARBEN[self.state]
    pg.draw.rect(bild, farbe_hg, bild_rect)
    if self.state == -1:
      pg.draw.rect(bild, '#D3D6DA', bild_rect, 3)
    if self.char != '':
      text = pg.font.SysFont('Arial_bold', 32).render(
          self.char, True, farbe_txt)
      text_rect = text.get_rect(center=bild_rect.center)
      bild.blit(text, text_rect)
    return bild


def generiere_felder():
  felder = []
  for i in range(26):
    x, y = i % 13 * 50 + 152, i // 13 * 50 + 500
    felder.append(Feld((x, y, 45, 44), chr(65+i), 3))
  for i in range(30):
    x, y = i % 5 * 50 + 352, i // 5 * 50 + 80
    felder.append(Feld((x, y, 45, 44), '', -1))
  return felder


def vergleich(geheim,versuch):
  bv, bg = list(versuch), list(geheim)
  for i in range(5):
    if bv[i] == bg[i]: 
      bv[i] = bg[i] = 2
  for i,b in enumerate(bv):
    if b == 2: continue
    if b in bg:
      bv[i] = 1
      bg[bg.index(b)] = 1
    else:
      bv[i] = 0
  return bv      
  

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
    ergebnis = vergleich(geheim,versuch)
    for i in range(5):
      feld_pos = cursor_min+i
      tasten_pos = ord(felder[feld_pos].char)-65
      felder[feld_pos].change_state(ergebnis[i])
      felder[tasten_pos].change_char('')
      felder[tasten_pos].change_state(-1)
    cursor_min, cursor_max = cursor, cursor + 5
    if cursor_max > 56:
      print(geheim)
  elif cursor < cursor_max:
    felder[cursor].change_char(chr(key).upper())
    cursor += 1


pg.init()
screen = pg.display.set_mode((920, 647))
bild = pg.image.load('Teil_72_Wordle.jpg')
with open('Teil_72_wörter.txt') as f:
  wörter = [w.strip() for w in f]
geheim = rnd.choice(wörter)
felder = generiere_felder()
cursor, cursor_min, cursor_max = 26, 26, 31


clock = pg.time.Clock()
FPS = 40

while True:
  clock.tick(FPS)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT:
      quit()
    if ereignis.type == pg.KEYDOWN:
      eingabe(ereignis.key)

  screen.blit(bild, (0, 0))
  for feld in felder:
    screen.blit(feld.img, feld.rect.topleft)
  pg.display.flip()
