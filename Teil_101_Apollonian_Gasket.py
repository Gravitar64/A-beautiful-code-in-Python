import pygame as pg
import cmath, math, itertools, random


def male_kreise(kreise):
  for krümmung, pos in kreise:
    pg.draw.circle(fenster, 'green', (pos.real, pos.imag), abs(1 / krümmung), 2)


def descartes(triplets):
  krümmungen = [krümmung for krümmung, _ in triplets]
  s = sum(krümmungen)
  p = sum(a * b for a, b in itertools.combinations(krümmungen, 2))
  if p < 0: return [None]
  p = 2 * math.sqrt(p)
  positions = [pos * krümmung for krümmung, pos in triplets]
  pos_sum = sum(positions)
  root = 2 * cmath.sqrt(sum(a * b for a, b in itertools.combinations(positions, 2)))
  return ((s - p, (pos_sum - root) * (1 / (s - p))), (s + p, (pos_sum + root) * (1 / (s + p))))


def distance(a, b):
  diff = a - b
  return abs(diff.real) + abs(diff.imag)


def init_kreise():
  r1 = random.randrange(breite / 20, breite / 5)
  r2 = breite / 4 - r1

  kreise = {(-1 / (breite / 4), zentrum),
            (1 / r1, zentrum - complex(breite / 4, 0) + complex(r1, 0)),
            (1 / r2, zentrum + complex(breite / 4, 0) - complex(r2, 0))}

  queue = {tuple(k for k in kreise)}
  fenster.fill('black')
  male_kreise(kreise)
  return kreise, queue


pg.init()
größe = breite, höhe = 1920, 1080
zentrum = complex(breite / 2, höhe / 2)
fenster = pg.display.set_mode(größe)
clock = pg.time.Clock()
FPS = 1

kreise, queue = init_kreise()
while True:
  pg.display.flip()
  clock.tick(FPS)

  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT or ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE: quit()


  new_queue = set()
  while queue:
    triplets = queue.pop()
    for neuer_kreis in descartes(triplets):
      if neuer_kreis == None or neuer_kreis[0] > 0.5: break
      if not all(distance(pos, neuer_kreis[1]) > 1 for _, pos in kreise): continue
      kreise.add(neuer_kreis)
      male_kreise([neuer_kreis])
      for a, b in itertools.combinations(triplets, 2):
        new_queue.add((a, b, neuer_kreis))
  queue = new_queue
  if not queue:
    kreise, queue = init_kreise()
