import pygame as pg
import random as rnd  

class Karte:
  def __init__(self, bild, pos):
    self.bild = bild
    self.pos = pos
    self.aufgedeckt = False
    self.pfad = []
    self.pfad_pos = 0
    self.animation = False
  
  def zeige(self):
    if self.aufgedeckt:
      pg.draw.rect(screen, (120,200,120), (*self.pos, karte_breite-5, karte_höhe-5))
      text = pg.font.SysFont('impact', 54).render(f' {self.bild}', False, (0,0,0))
      x = self.pos[0] + (karte_breite-14) //2  - text.get_width() // 2
      y = self.pos[1] + (karte_höhe-5) //2  - text.get_height() // 2
      screen.blit(text, (x,y))
    else:  
     color = (200,120,120) if self.animation else (120,120,200)
     pg.draw.rect(screen, color, (*self.pos, karte_breite-5, karte_höhe-5))
     if self.animation:
       pg.draw.rect(screen, (255,255,255), (*self.pos, karte_breite, karte_höhe), 4)

  def beiKlick(self):
    self.aufgedeckt = not self.aufgedeckt

  def move(self):
    self.pfad_pos += 1
    self.pos = self.pfad[self.pfad_pos]
    if self.pfad_pos == len(self.pfad)-1:
      self.pfad_pos = 0
      return True


  def pfad_erstellen(self, ziel):
    self.pfad = []
    x,y = self.pos
    x1, y1 = ziel
    sx, sy = (x1-x)/79, (y1-y)/79
    for i in range(80):
        self.pfad.append((x+sx*i, y+sy*i))
        


level = [(2,3,2,False), (2,3,3,False), (2,3,2,True), (2,3,3,True),
         (4,3,2,False), (4,3,3,False), (4,3,2,True), (4,3,3,True),
         (6,3,2,False), (6,3,3,False), (6,3,2,True), (6,3,3,True),
         (6,4,2,False), (6,4,3,False), (6,4,2,True), (6,4,3,True)
         ]


pg.init()
BREITE, HÖHE = 800, 640
screen = pg.display.set_mode([BREITE, HÖHE])

for spalten, zeilen, anz_richtige, pos_tauschen in level:

  nextLevel = False
  swap_animation = False
  zellen = spalten * zeilen
  karte_breite = BREITE // spalten
  karte_höhe = HÖHE // zeilen

  karten = {}
  aufgedeckte_karten = []
  nummern = [i for i in range(zellen//anz_richtige)]*anz_richtige
  rnd.shuffle(nummern)
  for i in range(zellen):
      x = i % spalten * karte_breite
      y = i // spalten * karte_höhe
      karten[i] = Karte(nummern.pop(), (x,y))
    
  weitermachen = True
  clock = pg.time.Clock()

  while weitermachen:
    clock.tick(60)
    screen.fill((0,0,0))

    if not swap_animation:
      for ereignis in pg.event.get():
        if ereignis.type == pg.QUIT:
          weitermachen = False
        if ereignis.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[0]:
          if len(aufgedeckte_karten) == anz_richtige:
            if all(karten[x].bild == karten[aufgedeckte_karten[0]].bild for x in aufgedeckte_karten):
              for i in aufgedeckte_karten:
                del karten[i]
            else:
              for i in aufgedeckte_karten:
                karten[i].aufgedeckt = False
            aufgedeckte_karten = []
            if pos_tauschen and karten:
              while True:
                k1,k2 = rnd.choice(list(karten.values())), rnd.choice(list(karten.values()))
                if k1 != k2: break
              k1.pfad_erstellen(k2.pos)
              k2.pfad_erstellen(k1.pos)
              k1.animation, k2.animation = True, True
              swap_animation = True
          else:    
            mouseX, mouseY = pg.mouse.get_pos()
            i = mouseY // karte_höhe * spalten + mouseX // karte_breite
            if i in karten and not karten[i].aufgedeckt:
              karten[i].beiKlick()
              aufgedeckte_karten.append(i)          
    else:
      k1.move()
      if k2.move():
        swap_animation = False
        k1.pos, k2.pos = k2.pos, k1.pos
        k1.bild, k2.bild = k2.bild, k1.bild
        k1.animation, k2.animation = False, False


    for karte in karten.values():
      karte.zeige()
    if swap_animation:
      k1.zeige()
      k2.zeige()  

    if not(karten):
      weitermachen = False
      nextLevel = True    

    pg.display.flip()

  if not nextLevel: break

pg.quit()