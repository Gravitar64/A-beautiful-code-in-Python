import math
from ursina import *
from time import perf_counter as pfc


def punkt_in_mandelbrot(x, y, z) -> bool:
  global hülle
  if z == 0:
    hülle = True
    return False
  x, y, z = x/BEREICH, y/BEREICH, z/BEREICH
  for _ in range(MAX_ITER):
    r = (x*x + y*y + z*z)**0.5
    if r > 2:
      hülle = False
      return False
    θ = math.atan2((x*x + y*y)**0.5, z)
    φ = math.atan2(y, x)
    rn = r**N
    x += rn * math.sin(θ * N) * math.cos(φ * N)
    y += rn * math.sin(θ * N) * math.sin(φ * N)
    z += rn * math.cos(θ * N)
  if not hülle:
    hülle = True
    return True


start = pfc()
N, MAX_ITER, BEREICH = 8, 20, 64
punkte = []
for x in range(BEREICH):
  for y in range(BEREICH):
    hülle = False
    for z in range(BEREICH):
      if not punkt_in_mandelbrot(x, y, z):
        continue
      punkte.append((x, y, z))
      punkte.append((-x, y, z))
      punkte.append((x, -y, z))
      punkte.append((-x, -y, z))
      punkte.append((x, y, -z))
      punkte.append((-x, y, -z))
      punkte.append((x, -y, -z))
      punkte.append((-x, -y, -z))
print(pfc()-start)
app = Ursina()
window.borderless = False
window.fps_counter.enabled = True
window.size = (1920, 1080)
window.color = color.black
Entity(model=Mesh(vertices=punkte, mode='point',
                  thickness=0.01), color=color.green)
EditorCamera()
app.run()
