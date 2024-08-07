import bpy
import random as rnd
from collections import Counter
import itertools as iter 


feld_von, feld_bis = -4, 4
spielfeld_von, spielfeld_bis = feld_von-6, feld_bis+6
anz = int((feld_bis-feld_von)**3*.3)

spielfeld = {(rnd.randint(feld_von, feld_bis), rnd.randint(
    feld_von, feld_bis), rnd.randint(feld_von, feld_bis)) for _ in range(anz)}
animate_frame = 8


def nachbarn(pos):
  for x,y,z in iter.product(range(-1,2), repeat = 3):
    if z == y == x == 0: continue
    yield pos[0]+x, pos[1]+y, pos[2]+z


def nächsteGeneration(spielfeld):
  nachb = Counter([p for pos in spielfeld for p in nachbarn(pos)])
  return {pos for pos, anz in nachb.items() if anz == 6 or (anz in (5, 6, 7, 8) and pos in spielfeld)}


def scale_rotate(ob, scale, rot, fr):
  ob.scale = (scale, scale, scale)
  ob.rotation_euler.rotate_axis("Z", rot)
  ob.keyframe_insert(data_path='rotation_euler', frame=fr)
  ob.keyframe_insert(data_path='scale', frame=fr)


bpy.ops.mesh.primitive_cube_add(size=0.001, location=(0, 0, 0))
orig_cube = bpy.context.active_object
n = "cube"
m = orig_cube.data.copy()

cubes = {}
for x,y,z in iter.product(range(spielfeld_von,spielfeld_bis), repeat = 3):
  o = bpy.data.objects.new(n, m)
  o.location = (x, y, z)
  cubes[x, y, z] = o
  bpy.context.collection.objects.link(o)
  o.select_set(False)

for i in range(200):
  print(f'Durchlauf No. {i}, Anz. Zellen = {len(spielfeld)}')
  spielfeld2 = nächsteGeneration(spielfeld)
  dead = spielfeld - spielfeld2
  new = spielfeld2 - spielfeld
  spielfeld = spielfeld2
  if not new and not dead:
    break
  for zelle in new | dead:
    if zelle not in cubes:
      continue
    ob = cubes[zelle]
    if zelle in new:
      scale_rotate(ob, 0.001, -3.141/2, (i-1)*animate_frame)
      scale_rotate(ob, 750, 3.141/2, i * animate_frame)
    else:
      scale_rotate(ob, 750, 3.141/2, (i-1) * animate_frame)
      scale_rotate(ob, 0.001, -3.141/2, i * animate_frame)
  if not spielfeld:
    break

bpy.context.scene.frame_current = 1
