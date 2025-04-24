import pygame as pg, random as rnd


def collatz_seq(n):
  seq = [n]
  while n != 1:
    n = n * 3 + 1 if n % 2 else n // 2
    seq.append(n)
  return seq


def plot_seq(seq):
  farbe.hsva = (0, rnd.randint(20, 100), 100)
  p1 = pg.Vector2(100, höhe - 30)
  segment = pg.Vector2(0, -10)
  winkel = 0
  for n in reversed(seq):
    winkel += -30 if n % 2 else 16.3
    p2 = p1 + segment.rotate(winkel)
    pg.draw.line(fenster, farbe, p1, p2, 10)
    p1 = p2


pg.init()
größe = breite, höhe = 1200, 1080
fenster = pg.display.set_mode(größe)
farbe = pg.Color(0)

for n in range(1, 2_000):
  plot_seq(collatz_seq(n))
pg.display.flip()

while True:
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT or ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE: quit()
