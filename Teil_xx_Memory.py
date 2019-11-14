import pygame as pg
import random as rnd

PFADELEMENTE = 80


class Spiel:

  def __init__(self, breite, höhe):
    self.level = 0
    self.levels = [(2, 3, 2, False), (2, 3, 3, False), (2, 3, 2, True),
                   (2, 3, 3, True), (4, 3, 2, False), (4, 3, 3, False),
                   (4, 3, 2, True), (4, 3, 3, True), (6, 3, 2, False),
                   (6, 3, 3, False), (6, 3, 2, True), (6, 3, 3, True),
                   (6, 4, 2, False), (6, 4, 3, False), (6, 4, 2, True),
                   (6, 4, 3, True)]
    self.status = 'Zug'
    self.spalten, self.zeilen, self.anz_richtige, self.pos_tauschen = self.levels[
        self.level]
    self.zellen = self.spalten * self.zeilen
    self.breite = breite
    self.höhe = höhe
    self.k_breite = breite // self.spalten
    self.k_höhe = höhe // self.zeilen

  def nextLevel(self):
    self.level += 1
    if self.level >= len(self.levels):
      self.status == 'Ende'
      return
    self.spalten, self.zeilen, self.anz_richtige, self.pos_tauschen = self.levels[
        self.level]
    self.k_breite = self.breite // self.spalten
    self.k_höhe = self.höhe // self.zeilen
    self.zellen = self.spalten * self.zeilen

  def animation(self, start):
    self.status = 'Animation' if start else 'Zug'

  def spielbrett_füllen(self):
    karten = {}
    nummern = [i for i in range(self.zellen // self.anz_richtige)
              ] * self.anz_richtige
    rnd.shuffle(nummern)
    for i in range(self.zellen):
      x = i % self.spalten * self.k_breite
      y = i // self.spalten * self.k_höhe
      karten[i] = Karte(nummern.pop(), (x, y), self.k_breite, self.k_höhe)
    return karten


class Karte:

  def __init__(self, bild, pos, breite, höhe):
    self.bild = bild
    self.pos = pos
    self.aufgedeckt = False
    self.pfad_pos = 0
    self.animation = False
    self.breite = breite
    self.höhe = höhe

  def zeige(self):
    if self.aufgedeckt:
      pg.draw.rect(screen, (120, 200, 120),
                   (*self.pos, self.breite - 5, self.höhe - 5))
      text = pg.font.SysFont('impact', 54).render(f' {self.bild}', False,
                                                  (0, 0, 0))
      x = self.pos[0] + (self.breite - 14) // 2 - text.get_width() // 2
      y = self.pos[1] + (self.höhe - 5) // 2 - text.get_height() // 2
      screen.blit(text, (x, y))
    else:
      color = (200, 120, 120) if self.animation else (120, 120, 200)
      pg.draw.rect(screen, color, (*self.pos, self.breite - 5, self.höhe - 5))
    if self.animation:
      pg.draw.rect(screen, (255, 255, 255), (*self.pos, self.breite, self.höhe),
                   5)

  def beiKlick(self):
    self.aufgedeckt = True

  def move(self, start, ziel):
    self.pfad_pos += 1
    x1, y1 = start
    x3, y3 = ziel
    x2, y2 = x1, y3
    t = self.pfad_pos / PFADELEMENTE
    t1 = 1 - t
    a, b, c = t1**2, 2 * t * t1, t**2
    self.pos = (a * x1 + b * x2 + c * x3, a * y1 + b * y2 + c * y3)
    if self.pfad_pos == PFADELEMENTE:
      self.pfad_pos = 0
      self.animation = False
      return True


pg.init()
BREITE, HÖHE = 4000, 3000
screen = pg.display.set_mode([BREITE, HÖHE])

spiel = Spiel(BREITE, HÖHE)
karten = spiel.spielbrett_füllen()
aufgedeckte_karten = []

weitermachen = True
clock = pg.time.Clock()

while weitermachen:
  clock.tick(60)
  screen.fill((0, 0, 0))

  if spiel.status == 'Animation':
    k1.move(pos1, pos2)
    if k2.move(pos2, pos1):
      spiel.animation(False)
      karten[i1], karten[i2] = karten[i2], karten[i1]

  if spiel.status == 'Zug':
    for ereignis in pg.event.get():
      if ereignis.type == pg.QUIT:
        weitermachen = False
      if ereignis.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[0]:
        if len(aufgedeckte_karten) == spiel.anz_richtige:
          #haben alle aufgedeckten Karten das gleiche Bild?
          if all(karten[x].bild == karten[aufgedeckte_karten[0]].bild
                 for x in aufgedeckte_karten):
            for i in aufgedeckte_karten:
              del karten[i]
          #wenn nicht, können die Karten wieder zugedeckt werden
          else:
            for i in aufgedeckte_karten:
              karten[i].aufgedeckt = False
          aufgedeckte_karten = []
          #falls tauschen angesagt ist, dann sollte man nach zudecken
          #oder entfernen der aufgedeckten Karten das Taschen vornehmen
          if spiel.pos_tauschen and karten:
            #hier holen wir uns zwei unterschiedliche indexwerte
            while True:
              i1, i2 = rnd.choice(list(karten)), rnd.choice(list(karten))
              if i1 != i2:
                break
            #dazu dann die karten
            k1, k2 = karten[i1], karten[i2]
            pos1, pos2 = k1.pos, k2.pos
            #bei diesen beiden karten wird hinterlegt, dass diese animiert werden
            k1.animation, k2.animation = True, True
            #durch swap_animation = True wird die Abfrage der Ereignisse ausgesetzt
            #bis swap_animation = False ist
            spiel.animation(True)
        else:  #die Anzahl der aufgedeckten Karten ist < vorgabe
          mouseX, mouseY = pg.mouse.get_pos()
          i = mouseY // spiel.k_höhe * spiel.spalten + mouseX // spiel.k_breite
          if i in karten and not karten[i].aufgedeckt:
            karten[i].beiKlick()
            aufgedeckte_karten.append(i)

  if spiel.status == 'Ende':
    break

  for karte in karten.values():
    #zuerst alle karten zeichnen, die nicht ainimiert werden
    if not karte.animation:
      karte.zeige()

  #jetzt die karten, die animiert werden zeichnen (= im Vordergrund)
  if spiel.status == 'Animation':
    k1.zeige()
    k2.zeige()

  #wenn alle karten gelöscht wurden (= alle Bilder gefunden), startet
  #das nächste Level
  if not (karten):
    spiel.nextLevel()
    karten = spiel.spielbrett_füllen()

  pg.display.flip()

pg.quit()