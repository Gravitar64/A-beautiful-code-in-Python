import ursina as urs
import math
import itertools as iter


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
    thetaN = math.atan2((x*x + y*y) ** 0.5, z) * N
    phiN = math.atan2(y, x) * N
    rN = r**N
    x += rN * math.sin(thetaN) * math.cos(phiN)
    y += rN * math.sin(thetaN) * math.sin(phiN)
    z += rN * math.cos(thetaN)
  if not hülle:
    hülle = True
    return True

start = pfc()
BEREICH, N, MAX_ITER = 128, 8, 6

punkte = []
for x in range(-BEREICH,BEREICH):
  for y in range(-BEREICH,BEREICH):
    hülle = False
    for z in range(-BEREICH, BEREICH):
      if not punkt_in_fraktal(x, y, z): continue
      punkte.append((x, y, z))
export_ply_format('points.ply')
print(pfc()-start)

app = urs.Ursina()
urs.window.borderless = False
urs.window.size = (1920, 1080)
urs.window.color = urs.color.black
urs.Entity(model=urs.Mesh(vertices=punkte, mode='point',
                          thickness=0.01), color=urs.color.green)
urs.EditorCamera()
app.run()
