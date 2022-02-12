import pygame as pg
import random as rnd


class Element(pg.sprite.Sprite):
  def __init__(self, id, typ, image, pos, enabled):
    super().__init__()
    self.id = id
    self.typ = typ
    self.image_e = pg.image.load(image+'_e.png')
    self.image_d = pg.image.load(image+'_d.png')
    self.enabled = enabled
    self.image = self.image_e.copy() if enabled else self.image_d.copy()
    self.rect = self.image.get_rect()
    self.rect.topleft = pos
    self.selektiert = False
    self.mögl_punkte = 0
    self.punkte = 0
    
  def change_enabled(self, t):
    self.enabled = t
    self.image = self.image_e.copy() if self.enabled else self.image_d.copy()


def clicked_button(e):
  global würfel_zähler
  if e.id == 0:
    start_würfeln(e)
  if e.id == 1:
    for e2 in group_elemente:
      if e2.typ == 'Feld' and e2.selektiert:
        e2.punkte += e2.mögl_punkte
        e2.selektiert = False
        e2.change_enabled(False)
        render_punkte(e2, e2.punkte)
        #Freischalten extra 5er nach Einbuchen 5er
        if e2.id == 14 and e2.punkte:
          group_elemente.sprites()[16].change_enabled(True)
        #Extra 5er bleiben nach Buchung von Punkten weiterhin freigeschaltet
        if e2.id == 16 and e2.mögl_punkte:
          e2.change_enabled(True)
          render_punkte(e2, e2.punkte)  
      if e2.typ == 'Würfel' and e2.selektiert:
        e2.selektiert = False
        e2.image = e2.image_e  
    e.change_enabled(False)
    group_elemente.sprites()[-3].change_enabled(True)
    würfel_zähler = 0
    start_würfeln(e)
    render_summen()      


def clicked_würfel(e):
  e.selektiert = not e.selektiert
  e.image = e.image_d if e.selektiert else e.image_e


def clicked_feld(e):
  e.selektiert = not e.selektiert
  e.image = e.image_e.copy()
  group_elemente.sprites()[-2].change_enabled(e.selektiert)
  if e.selektiert:
    pg.draw.rect(e.image, '#B7FF7A', (4,4,59,62),5)
    for e2 in group_elemente:     
      if e2.typ == 'Feld' and e2.selektiert and e2 != e:
        e2.selektiert = False
        e2.image = e2.image_e.copy()
    e.mögl_punkte = punkte_ermitteln(e.id)
    render_punkte(e, e.mögl_punkte)    
    

def render_punkte(e,punkte):
  text = pg.font.SysFont('arial',40).render(str(punkte), True, '#B7FF7A')
  cx, cy = e.image.get_width()//2, e.image.get_height()//2
  rect = text.get_rect(center=(cx,cy))
  e.image.blit(text, rect)


def render_summen():
  global gesamt_summe
  summen = {6:0, 7:0, 8:0, 17:0}
  for e in group_elemente:
    if e.typ != 'Feld':continue 
    if e.id < 6:
      summen[6] += e.punkte
    elif e.id in range(9,17):
      summen[17] += e.punkte
  summen[7] = 35 if summen[6] >= 63 else 0
  summen[8] = summen[6] + summen[7]
  gesamt_summe = summen[8] + summen[17]

  for i,punkte in summen.items():
    e = group_elemente.sprites()[i]
    e.punkte = punkte
    e.image = e.image_d.copy()
    render_punkte(e, e.punkte)                


def start_würfeln(e):
  global anim_würfeln, würfel_zähler
  pg.time.set_timer(pg.USEREVENT, 1000, True)
  anim_würfeln = True
  würfel_zähler += 1
  if würfel_zähler == 3:
    e.change_enabled(False)


def würfeln():
  for e in group_elemente:
    if e.typ != 'Würfel' or e.selektiert: continue
    e.id = rnd.randint(1,6)
    e.image_e = bild_würfel_e[e.id-1]    
    e.image_d = bild_würfel_d[e.id-1]
    e.image = e.image_e  


def punkte_ermitteln(i):
  wurf = [e.id for e in group_elemente if e.typ == 'Würfel']
  sw, sl = set(wurf), len(set(wurf))
  paschs = [wurf.count(w) for w in sw]
  if i <   6: return wurf.count(i+1) * (i+1)
  if i ==  9: return (max(paschs) >= 3) * sum(wurf)
  if i == 10: return (max(paschs) >= 4) * sum(wurf)
  if i == 11: return (set(paschs) == {2,3}) * 25
  if i == 12: return (any({w, w+1, w+2, w+3} <= sw for w in sw)) * 30
  if i == 13: return (max(sw) - min(sw) == 4 and sl == 5) * 40
  if i == 14: return (max(paschs) == 5) * 50
  if i == 15: return sum(wurf)
  if i == 16: return (max(paschs) == 5) * (50 + sum(wurf))
  

pg.init()
BREITE, HÖHE = 1280, 720
FPS = 40
zentrum = (BREITE / 2, HÖHE / 2)
screen = pg.display.set_mode((BREITE, HÖHE))
pg.time.set_timer(pg.USEREVENT, 1000, True)
anim_würfeln = True
würfel_zähler = 1
gesamt_summe = 0   

pfad = 'Teil_63_Bilder/'
bild_gui = pg.image.load(f'{pfad}gui.png')
bild_würfel_e = [pg.image.load(f'{pfad}{n+1}_e.png') for n in range(6)]
bild_würfel_d = [pg.image.load(f'{pfad}{n+1}_d.png') for n in range(6)]
group_elemente = pg.sprite.Group()

for n in range(18):
  pos = (292, 19+75*n) if n < 9 else (1195, 19+75*(n-9))
  enabled = n not in (6,7,8,16,17)
  group_elemente.add(Element(n, 'Feld', f'{pfad}Feld', pos, enabled))

for n in range(1,6):
  pos = (606, 130+90*(n-1))
  group_elemente.add(Element(n, 'Würfel', f'{pfad}{n}', pos, True))

for n in range(3):
  pos = [(400,615), (815,615), (506,450)]
  enabled = n == 0
  group_elemente.add(Element(n, 'Button', f'{pfad}Button{n}', pos[n], enabled)) 


weitermachen = True
clock = pg.time.Clock()

while weitermachen:
  clock.tick(FPS)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT:
      weitermachen = False
    if ereignis.type == pg.USEREVENT:
      anim_würfeln = False
    if ereignis.type == pg.MOUSEBUTTONDOWN:
      point = pg.mouse.get_pos()
      for e in group_elemente:
        if not e.enabled or not e.rect.collidepoint(point): continue
        if e.typ == "Button": clicked_button(e)
        if e.typ == "Würfel": clicked_würfel(e)
        if e.typ == "Feld": clicked_feld(e)

  screen.blit(bild_gui, (0,0))
  group_elemente.draw(screen)
  if anim_würfeln:
    würfeln()

  text = pg.font.SysFont('impact', 60).render(str(gesamt_summe), True, '#B7FF7A')
  rect = text.get_rect(center = zentrum)
  rect[1] = 5
  screen.blit(text, rect)  
  
  pg.display.flip()

pg.quit()