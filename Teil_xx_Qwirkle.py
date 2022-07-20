import pygame as pg
from enum import Enum
import copy


Ort = Enum('Ort', 'BEUTEL SPEICHER BRETT')


class Stein:
  def __init__(self, i):
    self.i = i
    self.pos = i2pos(i)
    self.anz = 3
    self.ort = Ort.BEUTEL
    self.markiert = False

  @property
  def bild(self):
    stein_rect = pg.Rect(*i2pos(self.i), STEINGRÖSSE, STEINGRÖSSE)
    stein = pg.Surface(stein_rect.size)
    anzahl = pg.Surface((20, 20), pg.SRCALPHA, 32)
    anzahl_rect = anzahl.get_rect()
    pg.draw.circle(anzahl, '#ff0000', anzahl_rect.center, 10)
    pg.draw.circle(anzahl, '#ffffff', anzahl_rect.center, 10, 1)
    anzahl_text = pg.font.SysFont('Arial_bold', 24).render(
        str(self.anz), True, '#ffffff')
    anzahl_text_rect = anzahl_text.get_rect(center=anzahl_rect.center)
    anzahl.blit(anzahl_text, anzahl_text_rect)
    stein.blit(steineBild, (0, 0), stein_rect)
    stein.blit(anzahl, (60, 0), anzahl_rect)
    if self.markiert:
      pg.draw.rect(stein, '#00ffff', (0, 0, STEINGRÖSSE, STEINGRÖSSE), 4)
    return stein


def i2pos(i):
  return i % 6 * STEINGRÖSSE, i // 6 * STEINGRÖSSE


def pos2stein(pos):
  x, y = pos
  for stein in steine:
    x1, y1 = stein.pos
    x2, y2 = x1+STEINGRÖSSE, y1+STEINGRÖSSE
    if x1 <= x <= x2 and y1 <= y <= y2:
      return stein
  return None


def beutel2speicher(stein):
  stein.anz -= 1
  s2 = copy.copy(stein)
  s2.pos = (6-freier_speicher)*STEINGRÖSSE, 800
  s2.ort = Ort.SPEICHER
  steine.append(s2)

def speicher2beutel():
  anz = 0
  for stein in reversed(steine):
    if not stein.markiert: continue
    i = stein.i
    steine[i].anz += 1
    steine.remove(stein)
    anz += 1
  pos = 0
  for stein in steine:
    if stein.ort != Ort.SPEICHER: continue
    stein.pos = (pos*STEINGRÖSSE,800)
    pos += 1
  return anz  


def zeichneSteine():
  fenster.fill('#000000')
  for stein in steine:
    if stein.ort == Ort.BEUTEL:
      if stein.anz > 0:
        fenster.blit(stein.bild, stein.pos)
    else:
      fenster.blit(stein.bild, stein.pos)
  pg.display.flip()


STEINGRÖSSE = 80

pg.init()
fenster_b, fenster_h = 1920, 1080
fenster = pg.display.set_mode((fenster_b, fenster_h))
steineBild = pg.image.load('qwirkle.png')
steine = [Stein(i) for i in range(36)]
freier_speicher = 6


clock = pg.time.Clock()
FPS = 40
änderung, drag = True, False

# Zeichenschleife mit FPS Bildern pro Sekunde
while True:
  clock.tick(FPS)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT:
      quit()
    if ereignis.type == pg.MOUSEBUTTONDOWN and ereignis.button == 1:
      mouse_pos = pg.mouse.get_pos()
      if (stein := pos2stein(mouse_pos)):
        if stein.ort == Ort.BEUTEL and freier_speicher and stein.anz:
          beutel2speicher(stein)
          freier_speicher -= 1
          änderung = True
        if stein.ort == Ort.SPEICHER:
          stein.markiert = not stein.markiert
          änderung = True
          drag = True
    if ereignis.type == pg.MOUSEBUTTONDOWN and ereignis.button == 3:
      anz = speicher2beutel()
      freier_speicher += anz
      änderung = True
    if drag:
      stein.pos = pg.mouse.get_pos()
      änderung = True
    if ereignis.type == pg.MOUSEBUTTONUP and ereignis.button == 1:
      drag = False       

  if änderung:
    zeichneSteine()
    änderung = False
