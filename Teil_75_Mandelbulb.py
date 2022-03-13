import ursina as urs
import math
import itertools as it


def punkt_in_fraktal(x, y, z) -> bool:
  global hülle
  if z == 0:
    hülle = True
    return False
  x, y, z = x/BEREICH, y/BEREICH, z/BEREICH
  for _ in range(MAX_ITER):
    r = (x*x + y*y + z*z) ** 0.5
    if r > 2:
      hülle = False
      return False
    θN = math.atan2((x*x + y*y) ** 0.5, z) * N
    φN = math.atan2(y, x) * N
    rN = r**N
    x += rN * math.sin(θN) * math.cos(φN)
    y += rN * math.sin(θN) * math.sin(φN)
    z += rN * math.cos(θN)
  if not hülle:
    hülle = True
    return True


BEREICH, N, MAX_ITER = 64, 8, 16
punkte = []
for x in range(BEREICH):
  for y in range(BEREICH):
    hülle = False
    for z in range(BEREICH):
      if not punkt_in_fraktal(x, y, z):
        continue
      for m1, m2, m3 in it.product([-1, 1], repeat=3):
        punkte.append((x*m1, y*m2, z*m3))


app = urs.Ursina()
urs.window.borderless = False
urs.window.size = (1920, 1080)
urs.window.color = urs.color.black
urs.Entity(model=urs.Mesh(vertices=punkte, mode='point',
                          thickness=0.01), color=urs.color.green)
urs.EditorCamera()
app.run()
