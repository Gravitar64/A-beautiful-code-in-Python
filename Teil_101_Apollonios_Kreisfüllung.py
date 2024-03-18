import pygame as pg
import random, math, cmath, itertools


def init_kreise():
  r1 = höhe / 2
  r2 = random.randrange(r1 * 0.1, r1 * 0.9)
  r3 = r1 - r2
  kreise = [(-1 / r1, complex(breite / 2, höhe / 2)),
            (1 / r2, complex(breite / 2 - r1 + r2, r1)),
            (1 / r3, complex(breite / 2 + r1 - r3, r1))]

  return kreise, [kreise.copy()]


def gen_nächste_2_kreise(trio):
  # Descartes Kreis Theorem für die Krümmung der neuen 2 Kreise
  k1, k2, k3 = [k for k, _ in trio]
  wurzel = 2 * math.sqrt(abs(k1 * k2 + k2 * k3 + k3 * k1))
  k4, k5 = k1 + k2 + k3 + wurzel, k1 + k2 + k3 - wurzel

  # Komplexe Descarte Kreis Theorem für die Positionen der neuen 2 Kreise
  c1, c2, c3 = [c for _, c in trio]
  wurzel = 2 * cmath.sqrt(k1 * k2 * c1 * c2 + k2 * k3 * c2 * c3 + k3 * k1 * c1 * c3)
  c4, c5 = k1 * c1 + k2 * c2 + k3 * c3 + wurzel, k1 * c1 + k2 * c2 + k3 * c3 - wurzel

  return (k4, c4 / k4), (k5, c5 / k5)


def male_kreise(kreise):
  for krümmung, pos in kreise:
    pg.draw.circle(fenster, 'green', (pos.real, pos.imag), abs(1 / krümmung), 2)


def entfernung(a, b):
  diff = a - b
  return abs(diff.real) + abs(diff.imag)


pg.init()
größe = breite, höhe = 1920, 1080
fenster = pg.display.set_mode(größe)
clock = pg.time.Clock()
FPS = 1

kreise, queue = init_kreise()
while True:
  clock.tick(FPS)
  fenster.fill('black')
  male_kreise(kreise)
  pg.display.flip()

  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT or ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE: quit()

  queue2 = []
  while queue:
    trio = queue.pop()
    for neuer_kreis in gen_nächste_2_kreise(trio):
      if neuer_kreis[0] > 0.5: continue
      if not all(entfernung(neuer_kreis[1], pos) > 1 for _, pos in kreise): continue
      kreise.append(neuer_kreis)
      for a, b in itertools.combinations(trio, 2):
        queue2.append((a, b, neuer_kreis))
  queue = queue2
  if not queue:
    kreise, queue = init_kreise()