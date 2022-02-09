import pygame as pg
import random as rnd

COLORS = {-1:('#ffffff','#000000'),
          0 :('#787C7E','#ffffff'),
          1 :('#C9B458','#ffffff'),
          2 :('#6AAA64','#ffffff'),}

class Feld():
  def __init__(self,rect):
    self.rect = pg.Rect(rect)
    self.char = ''
    self.state = -1
    self.color_bg = '#ffffff'
    self.color_tx = '#000000'
    self.img = self.render()

  def change_state(self,state):
    self.state = state
    self.color_bg, self.color_tx = COLORS[state]
    self.img = self.render()

  def change_char(self,char):
    self.char = char
    self.img = self.render()

  def render(self):
    img = pg.Surface((self.rect.w, self.rect.h))
    img_rect = img.get_rect()
    pg.draw.rect(img,self.color_bg,img_rect)
    if self.state < 0:
      pg.draw.rect(img,'#D3D6DA',(0,0,self.rect.w, self.rect.h),3)
    if self.char != '':
      text = pg.font.SysFont('Arial_bold',32).render(self.char, True, self.color_tx)
      text_rect = text.get_rect(center = img_rect.center)
      img.blit(text,text_rect)
    return img


def generiere_5_buchstaben_liste(datei):
  with open(datei) as f:
    return [w.strip().upper() for w in f if len(w) == 6]

def prüfe_versuch(versuch):
  pos = [0]*5
  bv, bg = list(versuch), list(geheim)
  for i in range(len(bv)):
    if bv[i] != bg[i]: continue
    pos[i] = 2
    bv[i] = bg[i] = '*'
  for i,b in enumerate(bv):
    if b == '*': continue
    if b in bg:
      pos[i] = 1
      bg[bg.index(b)] = '*'
  return pos    

pg.init()
scr_b = 920
scr_h = 647
screen = pg.display.set_mode((scr_b, scr_h))
bild = pg.image.load('teil_72_wordle.jpg')

wörter = generiere_5_buchstaben_liste('Teil_58_Wörter.txt')
geheim = rnd.choice(wörter)
felder = []
for i in range(30):
  x,y = i % 5 * 50 + 352, i // 5 * 50 + 80 
  felder.append(Feld((x,y,45,44)))
offen = [chr(x) for x in range(65,91)]
cursor = cursor_min = 0
cursor_max = 5


clock = pg.time.Clock()
FPS = 40

while True:
  clock.tick(FPS)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT: quit()
    if ereignis.type == pg.KEYDOWN:
      if ereignis.key == pg.K_BACKSPACE:
        if cursor > cursor_min: 
          cursor -= 1
          felder[cursor].change_char('')
      elif ereignis.key == pg.K_RETURN:
        if cursor == cursor_max:
          versuch = ''.join(f.char for f in felder[cursor_min:cursor_max])
          pos = prüfe_versuch(versuch)
          for i,p in enumerate(pos):
            feld = felder[cursor_min+i]
            feld.change_state(p)
            if feld.char in offen:
              offen[offen.index(feld.char)] = '*'
          cursor_min = cursor
          cursor_max = cursor_min + 5
          if cursor_max > 30:
            print(geheim)
      else:
        if cursor < cursor_max:
          felder[cursor].change_char(chr(ereignis.key).upper())
          cursor += 1     
      
        
  screen.blit(bild,(0,0))
  pg.draw.rect(screen,'#ffffff',(0,350,920,647))
  for f in felder:
    screen.blit(f.img,(f.rect.x, f.rect.y))
  for i,o in enumerate(offen):
    if o == '*': continue
    t = pg.Surface((45,44))
    t_r = t.get_rect()
    text = pg.font.SysFont('Arial_bold',32).render(o, True, '#000000')
    text_rect = text.get_rect(center = t_r.center)
    pg.draw.rect(t,'#D3D6DA',(0,0,45,44))
    t.blit(text,text_rect)
    x,y = i % 13 * 50 + 149, i // 13 * 50 + 500
    screen.blit(t,(x,y))

    
  pg.display.flip()