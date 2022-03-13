import math
from itertools import product
from ursina import *
from time import process_time as pfc


def punkt_in_mandelbrot(x,y,z) -> bool:
  global hülle
  if z == 0: 
    hülle = True
    return False
  x,y,z = x/BEREICH, y/BEREICH, z/BEREICH
  for _ in range(MAX_ITER):
    x2, y2, z2 = x*x, y*y, z*z
    r = (x2 + y2 + z2)**0.5
    if r > 2: 
      hülle = False
      return False 
    thetaN = math.atan2((x2 + y2)**0.5, z) * N
    phiN = math.atan2(y,x) * N
    r2N = r**N
    rNsinTethaN = r2N * math.sin(thetaN)
    x += rNsinTethaN * math.cos(phiN)
    y += rNsinTethaN * math.sin(phiN)
    z += r2N * math.cos(thetaN)
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
      if not punkt_in_mandelbrot(x, y, z): continue
      punkte.append((x,y,z))
      punkte.append((-x,y,z))
      punkte.append((x,-y,z))
      punkte.append((-x,-y,z))
      punkte.append((x,y,-z))
      punkte.append((-x,y,-z))
      punkte.append((x,-y,-z))
      punkte.append((-x,-y,-z))

print(f'{len(punkte):,.0f} Punkte ermittelt in {pfc()-start:.2f} Sek.')      
      
app = Ursina()
window.borderless = False
window.fps_counter.enabled = True
window.size = (1920,1080)
window.color = color.black
Entity(model=Mesh(vertices=punkte, mode='point', thickness=0.1),color=color.green)
EditorCamera()
app.run()
