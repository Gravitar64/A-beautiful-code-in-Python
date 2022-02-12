import pygame as pg
import random as rnd
from itertools import combinations
import copy
import arrow

class Element(pg.sprite.Sprite):
  def __init__(self, id, typ, image, pos, enabled):
    super().__init__()
    self.id = id
    self.typ = typ
    self.image_e = pg.image.load(image+'_e.png')
    self.image_d = pg.image.load(image+'_d.png')
    self.enabled = enabled
    self.image = self.image_e if enabled else self.image_d
    self.rect = self.image.get_rect()
    self.rect.topleft = pos
    self.selektiert = False
    self.sel_sim = False
    self.mögl_punkte = 0
    self.punkte = 0
    
  def change_enabled(self, t):
    self.enabled = t
    self.image = self.image_e if self.enabled else self.image_d

def clicked_button(e):
  global würfel_zähler, game_over, durchlauf, file, durchlauf_gesamt
  if e.id == 0:
    start_würfeln(e)
  elif e.id == 1:
    for e2 in group_elemente:
      if e2.typ == 'Feld' and e2.selektiert:
        e2.punkte += e2.mögl_punkte
        e2.selektiert = False
        e2.change_enabled(False)
        #Freischalten extra 5er nach Einbuchen 5er
        if e2.id == 14 and e2.punkte:
          group_elemente.sprites()[16].change_enabled(True)
        #Extra 5er bleiben nach Buchung von Punkten weiterhin freigeschaltet
        if e2.id == 16 and e2.mögl_punkte:
          e2.change_enabled(True)
      if e2.typ == 'Würfel' and e2.selektiert:
        e2.selektiert = False
        e2.image = e2.image_e  
    e.change_enabled(False)
    game_over = sum([el.enabled for el in group_elemente if el.typ == 'Feld']) == 0 
    group_elemente.sprites()[-3].change_enabled(True)      
    if game_over:
      if durchlauf < durchläufe:
        durchlauf_gesamt += gesamt
        file.write(f'{arrow.now().format("DD.MM.YYYY HH:mm:ss")} {durchlauf:>4}. {gesamt}\n')
        clicked_button(group_elemente.sprites()[-1])
      else:
        file.write(f'KI Best-Summe, {simulationsläufe} Simulationen\n')
        file.write(f'Summe = {durchlauf_gesamt}, Durchschnitt = {durchlauf_gesamt / durchlauf:.2f}\n')
        file.close()
        group_elemente.sprites()[-1].change_enabled(True)
        group_elemente.sprites()[-3].change_enabled(False)
      durchlauf += 1
      print(durchlauf)
    else:    
      würfel_zähler = 0
      start_würfeln(e)
  elif e.id == 2:
    e.change_enabled(False)
    group_elemente.sprites()[-3].change_enabled(True)
    for e in group_elemente:
      e.punkte = 0
      e.selected = False
      if e.typ == 'Feld':
        e.change_enabled(e.id not in (6,7,8,16,17))
    würfel_zähler = 0        
    game_over = False
    start_würfeln(e)

def clicked_würfel(e):
  e.selektiert = not e.selektiert
  e.image = e.image_d if e.selektiert else e.image_e

def clicked_feld(e):
  e.selektiert = not e.selektiert
  group_elemente.sprites()[-2].change_enabled(e.selektiert)
  if not e.selektiert: return
  e.mögl_punkte = punkte_ermitteln(e.id)
  for e2 in group_elemente:     
    if e2.typ == 'Feld' and e2.selektiert and e2 != e:
      e2.selektiert = False
     
def render_punkte(l):
  l.sprites()[6].punkte = sum([e.punkte for e in l.sprites()[:6]])
  l.sprites()[7].punkte = 35 if l.sprites()[6].punkte > 62 else 0
  l.sprites()[8].punkte = l.sprites()[6].punkte + l.sprites()[7].punkte
  l.sprites()[17].punkte = sum([e.punkte for e in l.sprites()[9:17]])
  gesamt = l.sprites()[8].punkte + l.sprites()[17].punkte
  
  for e in l:
    if e.typ != 'Feld': continue
    if e.selektiert:
      pg.draw.rect(screen,'#B7FF7A',e.rect,5)
      text = pg.font.SysFont('arial',40).render(str(e.mögl_punkte), True, '#B7FF7A')
    elif e.punkte > 0:
      text = pg.font.SysFont('arial',40).render(str(e.punkte), True, '#B7FF7A')  
    else:
      continue
    rect = text.get_rect(center=e.rect.center)
    screen.blit(text, rect)
  render_text(str(gesamt),40,60)
  return gesamt

def render_text(t,y,size):
  text = pg.font.SysFont('impact',size).render(t, True, '#B7FF7A')
  cx = zentrum[0]
  rect = text.get_rect(center=(cx,y))
  screen.blit(text,rect)  

def start_würfeln(e):
  global anim_würfeln, würfel_zähler
  pg.time.set_timer(pg.USEREVENT, 10, True)
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

def würfeln_sim():
  for e in group_elemente:
    if e.typ != 'Würfel' or e.sel_sim: continue
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

def ki():
  würfel_save = [e.id for e in group_elemente if e.typ == 'Würfel']
  best_score, best_selektion = 0, []
  #print("Ausgangswurf: ",würfel_save)
  for n in range(6):
    for sel in combinations(range(5),n):
      #print("Auswahl", list(sel))
      for i in range(5):
        group_elemente.sprites()[18+i].sel_sim = True if i in sel else False
      summe = 0
      for z in range(simulationsläufe):
        würfeln_sim()
        #print("Gewürfelt: ", [e.id for e in group_elemente if e.typ == 'Würfel'], end = ' ')
        max_p = 0
        for f in felder:
          if not group_elemente.sprites()[f].enabled: continue
          p = punkte_ermitteln(f)
          if p == 0: continue
          if (f < 6 and p > 2*(f+1)) or f > 8:
            summe += p
            #max_p = max(p, max_p)
        #summe += max_p
        #print("Beste Punktzahl = ",max_p)
        for i in range(18,23):
          group_elemente.sprites()[i].id = würfel_save[i-18]
      if summe > best_score:
        best_score = summe
        best_selektion = list(sel)
  for i in range(18,23):
    old_id = würfel_save[i-18]
    e = group_elemente.sprites()[i]
    e.id = old_id
    e.image_e = bild_würfel_e[old_id-1]    
    e.image_d = bild_würfel_d[old_id-1]
    e.image = e.image_d if e.selektiert else e.image_e
  return best_selektion

pg.init()
BREITE, HÖHE = 1280, 720
clock = pg.time.Clock()
FPS = 40
zentrum = (BREITE / 2, HÖHE / 2)
screen = pg.display.set_mode((BREITE, HÖHE))
pg.time.set_timer(pg.USEREVENT, 10, True)
anim_würfeln, game_over = True, False
würfel_zähler = 1
simulationsläufe = 100
durchläufe = 100
durchlauf = durchlauf_gesamt = 0

pfad = 'Teil_63_Bilder/'
bild_gui = pg.image.load(f'{pfad}gui.png')
bild_würfel_e = [pg.image.load(f'{pfad}{n+1}_e.png') for n in range(6)]
bild_würfel_d = [pg.image.load(f'{pfad}{n+1}_d.png') for n in range(6)]
group_elemente = pg.sprite.Group()
felder = list(range(6)) + list(range(9,17))
file = open('Teil_63_Log.txt','a')

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


while True:
  clock.tick(FPS)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT:
      quit()
    
    if ereignis.type == pg.USEREVENT:
      anim_würfeln = False
      if würfel_zähler < 3:
        sel = ki()
        i = 0
        for e in group_elemente:
          if e.typ != 'Würfel': continue
          e.selektiert = True if i in sel else False
          e.image = e.image_d if e.selektiert else e.image_e
          i += 1
        clicked_button(group_elemente.sprites()[-3])  
      else:
        max_p = best_feld = -1
        for f in felder:
          if not group_elemente.sprites()[f].enabled: continue
          p = punkte_ermitteln(f)
          if p > max_p:
            max_p = p
            best_feld = f
        e = group_elemente.sprites()[best_feld]
        e.mögl_punkte = max_p
        e.selektiert = True
        clicked_button(group_elemente.sprites()[-2])
        
        
    if ereignis.type == pg.MOUSEBUTTONDOWN:
      point = pg.mouse.get_pos()
      for e in group_elemente:
        if not e.enabled or not e.rect.collidepoint(point): continue
        if e.typ == "Button": clicked_button(e)
        if game_over: continue
        if e.typ == "Würfel": clicked_würfel(e)
        if e.typ == "Feld": clicked_feld(e)

  screen.blit(bild_gui, (0,0))
  if anim_würfeln:
    würfeln()
  group_elemente.draw(screen)
  gesamt = render_punkte(group_elemente)
  if game_over:
    render_text('GAME OVER', zentrum[1], 180)
      
  pg.display.flip()

pg.quit()