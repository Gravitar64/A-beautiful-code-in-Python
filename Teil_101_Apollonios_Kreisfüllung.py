import pygame as pg
import random, itertools, math, cmath


def init_kreise():
  r1 = höhe / 2
  r2 = random.randrange(r1 * 0.1, r1 * 0.9)
  r3 = r1 - r2
  zentrum = complex(breite / 2, höhe / 2)
  kreise = [((-1 / r1, zentrum)), 
            ((1 / r2, complex(breite / 2 - r1 + r2, r1))), 
            ((1 / r3, complex(breite / 2 + r1 - r3, r1)))]
  
  return kreise, [kreise.copy()]


def male_kreise(kreise):
  for krümmung, pos in kreise:
    pg.draw.circle(fenster, 'green', (pos.real, pos.imag), abs(1 / krümmung), 2)
  pg.display.flip()


def descartes(trio):
  krümmungen = [krümmung for krümmung, _ in trio]
  krüm_sum = sum(krümmungen)
  krüm_wurzel = 2 * math.sqrt(abs(sum([k1 * k2 for k1, k2 in itertools.combinations(krümmungen, 2)])))
  k1, k2 = krüm_sum + krüm_wurzel, krüm_sum - krüm_wurzel

  positionen = [pos * krümmung for krümmung, pos in trio]
  pos_sum = sum(positionen)
  pos_wurzel = 2 * cmath.sqrt(sum([p1 * p2 for p1, p2 in itertools.combinations(positionen, 2)]))
  p1, p2 = pos_sum + pos_wurzel, pos_sum - pos_wurzel

  return (k1, p1 * (1 / k1)), (k2, p2 * (1 / k2))


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

  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT or ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE: quit()

  queue2 = []
  while queue:
    trio = queue.pop()
    for neuer_kreis in descartes(trio):
      if neuer_kreis[0] > 0.5: continue
      if not all(entfernung(neuer_kreis[1], pos) > 1 for _, pos in kreise): continue
      kreise.append(neuer_kreis)
      for a, b in itertools.combinations(trio, 2):
        queue2.append((a, b, neuer_kreis))
  queue = queue2
  if not queue:
    kreise, queue = init_kreise()