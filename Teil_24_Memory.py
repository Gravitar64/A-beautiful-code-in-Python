import pygame as pg
import random as rnd

PFADELEMENTE = 80


class Karte:

  def __init__(self, bild, pos):
    self.bild = bild
    self.pos = pos
    self.aufgedeckt = False
    self.pfad_pos = 0
    self.animation = False

  def zeige(self):
    if self.aufgedeckt:
      pg.draw.rect(screen, (120, 200, 120),
                   (*self.pos, karte_breite - 5, karte_höhe - 5))
      text = pg.font.SysFont('impact', 54).render(f' {self.bild}', False,
                                                  (0, 0, 0))
      x = self.pos[0] + (karte_breite - 14) // 2 - text.get_width() // 2
      y = self.pos[1] + (karte_höhe - 5) // 2 - text.get_height() // 2
      screen.blit(text, (x, y))
    else:
      color = (200, 120, 120) if self.animation else (120, 120, 200)
      pg.draw.rect(screen, color, (*self.pos, karte_breite - 5, karte_höhe - 5))
    if self.animation:
      pg.draw.rect(screen, (255, 255, 255),
                   (*self.pos, karte_breite, karte_höhe), 5)

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


level = [(2, 3, 2, False), (2, 3, 3, False), (2, 3, 2, True), (2, 3, 3, True),
         (4, 3, 2, False), (4, 3, 3, False), (4, 3, 2, True), (4, 3, 3, True),
         (6, 3, 2, False), (6, 3, 3, False), (6, 3, 2, True), (6, 3, 3, True),
         (6, 4, 2, False), (6, 4, 3, False), (6, 4, 2, True), (6, 4, 3, True)]

pg.init()
BREITE, HÖHE = 800, 640
screen = pg.display.set_mode([BREITE, HÖHE])

for spalten, zeilen, anz_richtige, pos_tauschen in level:
  spiel_beenden = False
  swap_animation = False
  zellen = spalten * zeilen
  karte_breite = BREITE // spalten
  karte_höhe = HÖHE // zeilen

  karten = {}
  aufgedeckte_karten = []
  nummern = [i for i in range(zellen // anz_richtige)] * anz_richtige
  rnd.shuffle(nummern)
  for i in range(zellen):
    x = i % spalten * karte_breite
    y = i // spalten * karte_höhe
    karten[i] = Karte(nummern.pop(), (x, y))

  weitermachen = True
  clock = pg.time.Clock()

  while weitermachen:
    clock.tick(60)
    screen.fill((0, 0, 0))

    if swap_animation:
      k1.move(pos1, pos2)
      if k2.move(pos2, pos1):
        swap_animation = False
        karten[i1], karten[i2] = karten[i2], karten[i1]
    else:
      for ereignis in pg.event.get():
        if ereignis.type == pg.QUIT:
          weitermachen = False
          spiel_beenden = True
        if ereignis.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[0]:
          if len(aufgedeckte_karten) == anz_richtige:
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
            if pos_tauschen and karten:
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
              swap_animation = True
          else:  #die Anzahl der aufgedeckten Karten ist < vorgabe
            mouseX, mouseY = pg.mouse.get_pos()
            i = mouseY // karte_höhe * spalten + mouseX // karte_breite
            if i in karten and not karten[i].aufgedeckt:
              karten[i].beiKlick()
              aufgedeckte_karten.append(i)

    for karte in karten.values():
      #zuerst alle karten zeichnen, die nicht ainimiert werden
      if not karte.animation:
        karte.zeige()

    #jetzt die karten, die animiert werden zeichnen (= im Vordergrund)
    if swap_animation:
      k1.zeige()
      k2.zeige()

    #wenn alle karten gelöscht wurden (= alle Bilder gefunden), startet
    #das nächste Level
    if not (karten):
      weitermachen = False

    pg.display.flip()

  #wenn Fenster-Schließen gedrückt wurde
  if spiel_beenden:
    break

pg.quit()