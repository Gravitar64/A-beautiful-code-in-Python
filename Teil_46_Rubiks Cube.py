from ursina import *
from itertools import product

def eltern_kind_beziehung(achse, schicht):
  
  for w in würfel:
    w.position, w.rotation = round(w.world_position,1), w.world_rotation
    w.parent = scene
  
  zentrum.rotation = 0
  
  for w in würfel:
    if eval(f'w.position.{achse}') == schicht:
      w.parent = zentrum


def input(key):
  if key not in rot_dict: return
  achse, schicht, winkel = rot_dict[key]
  eltern_kind_beziehung(achse, schicht)
  shift = held_keys['shift']
  eval(f'zentrum.animate_rotation_{achse} ({-winkel if shift else winkel}, duration = 0.5)')

app = Ursina()
window.borderless = False
window.size = (800,800)
window.position = (2000, 200)
EditorCamera()

zentrum = Entity()

rot_dict = {'u': ['y', 1, 90],    'e': ['y', 0, -90],    'd': ['y', -1, -90],
            'l': ['x', -1, -90],  'm': ['x', 0, -90],    'r': ['x', 1, 90],
            'f': ['z', -1, 90],   's': ['z', 0, 90],     'b': ['z', 1, -90]}

würfel = []
for pos in product((-1,0,1), repeat=3):
  würfel.append(Entity(model='Teil_46_model.obj', texture = 'Teil_46_texture.png', position=pos, scale=0.5))

app.run()