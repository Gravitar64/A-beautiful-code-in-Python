import pygame as pg
import random as rnd


class Feld:

  STATES = {0: ('#ffffff', '#000000'),
            1: ('#787C7E', '#ffffff'),
            2: ('#C9B458', '#ffffff'),
            3: ('#6AAA64', '#ffffff'),
            4: ('#D3D6DA', '#000000')}

  def __init__(self, x, y, char, state):
    self.rect = pg.Rect(x, y, 45, 44)
    self.char = char
    self.state = state

  @property
  def img(self):
    bild = pg.Surface(self.rect.size)
    bild_rect = bild.get_rect()
    bg, fg = self.STATES[self.state]
    pg.draw.rect(bild, bg, bild_rect)
    if self.state == 0:
      pg.draw.rect(bild, '#D3D6DA', bild_rect, 3)
    if self.char != '':
      text = pg.font.SysFont('Arial_bold', 32).render(
          self.char, True, fg)
      text_rect = text.get_rect(center=bild_rect.center)
      bild.blit(text, text_rect)
    return bild


def generiere_felder():
  felder = []
  for i in range(26):
    x, y = i % 13 * 50 + 152, i // 13 * 50 + 500
    felder.append(Feld(x, y, chr(65+i), 4))
  for i in range(30):
    x, y = i % 5 * 50 + 352, i // 5 * 50 + 80
    felder.append(Feld(x, y, '', 0))
  return felder


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
  for feld in felder:
    screen.blit(feld.img, feld.rect.topleft)
  pg.display.flip()


def eingabe(key):
  global cursor, cursor_min, cursor_max
  if key == pg.K_BACKSPACE:
    if cursor == cursor_min: return
    cursor -= 1
    felder[cursor].char = ''
  elif key == pg.K_RETURN:
    if cursor != cursor_max: return
    versuch = ''.join(f.char for f in felder[cursor_min:cursor_max])
    if versuch not in wörter: return
    ergebnis = vergleich(list(geheim), list(versuch))
    for i in range(5):
      feld_pos = cursor_min+i
      tasten_pos = ord(felder[feld_pos].char)-65
      felder[feld_pos].state = ergebnis[i]
      felder[tasten_pos].char = ''
      felder[tasten_pos].state = 0
    cursor_min, cursor_max = cursor, cursor + 5
    if cursor_max > 56:
      print(geheim)
  elif cursor < cursor_max:
    felder[cursor].char = chr(key).upper()
    cursor += 1


pg.init()
screen = pg.display.set_mode((920, 647))
bild = pg.image.load('Teil_72_Wordle.jpg')
with open('Teil_72_wörter.txt') as f:
  wörter = [w.strip() for w in f]
geheim = rnd.choice(wörter)
felder = generiere_felder()
zeichne_felder()
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
      zeichne_felder()
