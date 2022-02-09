import pygame as pg
import random as rnd


class Feld:
  def __init__(self, rect):
    self.rect = pg.Rect(rect)
    self.char = ''
    self.state = -1
    self.img = generiere_bild(self.rect.size, self.char, self.state)

  def change_state(self, state):
    self.state = state
    self.img = generiere_bild(self.rect.size, self.char, self.state)

  def change_char(self, char):
    self.char = char
    self.img = generiere_bild(self.rect.size, self.char, self.state)


def generiere_felder():
  felder = []
  for i in range(30):
    x, y = i % 5 * 50 + 352, i // 5 * 50 + 80
    felder.append(Feld((x, y, 45, 44)))
  return felder


def generiere_bild(size, buchstabe, state):
  bild = pg.Surface(size)
  bild_rect = bild.get_rect()
  farbe_hg, farbe_txt = FARBEN[state]
  pg.draw.rect(bild, farbe_hg, bild_rect)

  if state == -1:
    pg.draw.rect(bild, '#D3D6DA', (0, 0, *size), 3)

  if buchstabe != '':
    text = pg.font.SysFont('Arial_bold', 32).render(buchstabe, True, farbe_txt)
    text_rect = text.get_rect(center=bild_rect.center)
    bild.blit(text, text_rect)

  return bild


def prüfe(versuch):
  pos = [0]*5
  bv, bg = list(versuch), list(geheim)
  for i in range(5):
    if bv[i] != bg[i]:
      continue
    pos[i] = 2
    bv[i] = bg[i] = '*'
  for i, b in enumerate(bv):
    if b == '*':
      continue
    if b in bg:
      pos[i] = 1
      bg[bg.index(b)] = '*'
  return pos


def eingabe(key):
  global cursor, cursor_min, cursor_max
  if key == pg.K_BACKSPACE:
    if cursor == cursor_min:
      return
    cursor -= 1
    felder[cursor].change_char('')
  elif key == pg.K_RETURN:
    if cursor != cursor_max:
      return
    versuch = ''.join(f.char for f in felder[cursor_min:cursor_max])
    pos = prüfe(versuch)
    for i in range(5):
      feld = felder[cursor_min+i]
      feld.change_state(pos[i])
      if versuch[i] in offen:
        offen[offen.index(versuch[i])] = '*'
    cursor_min = cursor
    cursor_max = cursor_min + 5
    if cursor_max > 30:
      print(geheim)
  else:
    if cursor == cursor_max:
      return
    felder[cursor].change_char(chr(key).upper())
    cursor += 1


FARBEN = {-1: ('#ffffff', '#000000'),
          0: ('#787C7E', '#ffffff'),
          1: ('#C9B458', '#ffffff'),
          2: ('#6AAA64', '#ffffff'),
          3: ('#D3D6DA', '#000000')}


pg.init()
screen = pg.display.set_mode((920, 647))
bild = pg.image.load('Teil_72_Wordle.jpg')
with open('Teil_72_wörter.txt') as f:
  wörter = [w.strip().upper() for w in f]
geheim = rnd.choice(wörter)
felder = generiere_felder()
offen = [chr(x) for x in range(65, 91)]
cursor, cursor_min, cursor_max = 0, 0, 5


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

  for i, buchstabe in enumerate(offen):
    if buchstabe == '*':
      continue
    x, y = i % 13 * 50 + 152, i // 13 * 50 + 500
    taste = generiere_bild((45, 44), buchstabe, 3)
    screen.blit(taste, (x, y))

  pg.display.flip()