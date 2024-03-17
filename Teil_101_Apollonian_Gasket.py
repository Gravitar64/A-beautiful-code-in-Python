import pygame as pg
import cmath, math, itertools, random


def male_kreise(kreise):
  img = pg.font.SysFont('arial.ttf',48).render(f'Anzahl Kreise = {len(kreise):,}',True, 'green')
  fenster.blit(img,(5,5))
  for krümmung, pos in kreise:
    pg.draw.circle(fenster, 'green', (pos.real, pos.imag), abs(1 / krümmung), 2)


def descartes(trio):
  krümmungen = [krümmung for krümmung, _ in trio]
  s = sum(krümmungen)
  p = 2 * math.sqrt(abs(sum(a * b for a, b in itertools.combinations(krümmungen, 2))))
  positions = [pos * krümmung for krümmung, pos in trio]
  pos_sum = sum(positions)
  root = 2 * cmath.sqrt(sum(a * b for a, b in itertools.combinations(positions, 2)))
  return (s - p, (pos_sum - root) * (1 / (s - p))), (s + p, (pos_sum + root) * (1 / (s + p)))


def distance(a, b):
  diff = a - b
  return abs(diff.real) + abs(diff.imag)


def init_kreise():
  r1 = höhe / 2 
  r2 = random.randrange(r1*0.1, r1*0.9)
  r3 = r1 - r2

  kreise = {(-1 / r1, zentrum),
            (1 / r2, zentrum - complex(r1,0) + complex(r2,0)),
            (1 / r3, zentrum + complex(r1,0) - complex(r3,0))}

  queue = {tuple(k for k in kreise)}
  return kreise, queue


pg.init()
größe = breite, höhe = 1920, 1080
zentrum = complex(breite / 2, höhe / 2)
fenster = pg.display.set_mode(größe)
clock = pg.time.Clock()
FPS = 10

kreise, queue = init_kreise()
while True:
  fenster.fill('black')
  male_kreise(kreise)
  pg.display.flip()
  clock.tick(FPS)

  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT or ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE: quit()


  new_queue = set()
  while queue:
    trio = queue.pop()
    for neuer_kreis in descartes(trio):
      k4,p4 = neuer_kreis
      if k4 > 0.5: continue
      if not all(distance(pos, p4) > 1 for _, pos in kreise): continue
      kreise.add(neuer_kreis)
      for a, b in itertools.combinations(trio, 2):
        new_queue.add((a, b, neuer_kreis))
  queue = new_queue
  if not queue:
    kreise, queue = init_kreise()
