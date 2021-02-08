from ursina import *
from itertools import product


rot_dict = {'u': ['y', 1, 90],    'e': ['y',0, -90],    'd': ['y', -1, -90], 
            'l': ['x', -1, -90],  'm': ['x', 0, -90],   'r': ['x', 1, 90],  
            'f': ['z', -1, 90],   's': ['z',0,90],      'b': ['z', 1, -90]}

app = Ursina()
window.borderless = False
window.size = (800, 800)

Light(type='ambient', color=(0.5, 0.5, 0.5, 0.5))  # dim full spectrum
Light(type='directional', color=(0.5, 0.5, 0.5, 1),direction=(0.8,0.8,0.8))  # dim full spectrum
PARENT = Entity()
cubes = []

for pos in product(range(-1,2), repeat=3):
  cubes.append(Entity(position=pos, model='textures/cube', scale=0.5, texture="textures/cube", ))


def parent_scheibe(d, p):
  for c in cubes:
    if c.parent != PARENT: continue
    wpos, wrot = c.world_position, c.world_rotation
    c.parent = scene
    c.position, c.rotation = round(wpos, 1), wrot
  PARENT.rotation = 0

  for c in cubes:
    if eval(f'c.position.{d} != {p}'): continue
    c.parent = PARENT

def input(key):
  if key not in rot_dict: return
  d, p, r = rot_dict[key]
  parent_scheibe(d, p)
  if held_keys['shift']:
    eval(f'PARENT.animate_rotation_{d}( {-r}, duration=0.5)')
  else:
    eval(f'PARENT.animate_rotation_{d}( {r}, duration=0.5)')

EditorCamera()
app.run()
