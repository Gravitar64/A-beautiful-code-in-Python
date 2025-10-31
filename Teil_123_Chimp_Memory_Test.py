# Quelle: (ESL) Chimp's Memory by professorwynnie
# https://www.youtube.com/watch?v=aAIGVT3N7B0


import pygame as pg
import random as rnd
import time


def gen_zufällige_positionen():
  kachel_i = rnd.sample(range(spalten * zeilen), sequenz)
  positionen = []
  for n, i in enumerate(kachel_i, start=1):
    x, y = i % spalten * kachel, i // spalten * kachel
    kachel_rect = pg.Rect(x, y, kachel, kachel)
    bild_zahl = pg.font.SysFont('Arial_bold', 90).render(str(n), True, 'white')
    bild_rect = bild_zahl.get_rect(center=kachel_rect.center)
    positionen.append((kachel_rect, bild_zahl, bild_rect))
  return positionen


def zeige_zahlen(positionen):
  for kachel_rect, bild_zahl, bild_rect in positionen:
    pg.draw.rect(fenster, 'white', kachel_rect, 2)
    fenster.blit(bild_zahl, bild_rect)


def zeige_rechtecke(positionen):
  zeit_rect = pg.Rect(0, 0, breite, 50)
  bild_zeit = pg.font.SysFont('Arial', 48).render(f'{t2 - t1:.2f} Sek.', True, 'white')
  bild_rect = bild_zeit.get_rect(center=zeit_rect.center)
  fenster.blit(bild_zeit, bild_rect)
  for kachel_rect, *_ in positionen:
    pg.draw.rect(fenster, 'white', kachel_rect)
    pg.draw.rect(fenster, 'black', kachel_rect, 2)


pg.init()
spalten, zeilen = 9, 5
kachel = 100
größe = breite, höhe = spalten * kachel, zeilen * kachel
fenster = pg.display.set_mode(größe)


clock = pg.time.Clock()
FPS = 40

sequenz = 9
positionen = gen_zufällige_positionen()
t1 = time.perf_counter()
start = False

while True:
  clock.tick(FPS)
  fenster.fill('black')

  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT or ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE: quit()
    if ereignis.type == pg.MOUSEBUTTONDOWN:
      x, y = pg.mouse.get_pos()
      kachel_x, kachel_y = x // kachel * kachel, y // kachel * kachel
      r, *_ = positionen.pop(0)
      if r.x != kachel_x or r.y != kachel_y: quit()
      if not start: t2 = time.perf_counter()
      start = True

  if not start:
    zeige_zahlen(positionen)
  else:
    zeige_rechtecke(positionen)
  pg.display.flip()
