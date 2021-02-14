from ursina import *
from itertools import product

rot_dict = {'u': ['y', 1, 90],    'e': ['y', 0, -90],    'd': ['y', -1, -90],
            'l': ['x', -1, -90],  'm': ['x', 0, -90],    'r': ['x', 1, 90],
            'f': ['z', -1, 90],   's': ['z', 0, 90],     'b': ['z', 1, -90]}

def input(key):
  if key not in rot_dict: return
  rot_achse, schicht, winkel = rot_dict[key]
  childs_scheibe(rot_achse, schicht)
  if held_keys['shift']:
    eval(f'PARENT.animate_rotation_{rot_achse} ({-winkel}, duration=0.5)')
  else:
    eval(f'PARENT.animate_rotation_{rot_achse} ({winkel}, duration=0.5)')

def childs_scheibe(rot_achse, schicht):
  for w in würfel:
    if w.parent != PARENT: continue
    wpos, wrot = w.world_position, w.world_rotation
    w.parent = scene
    w.position, w.rotation = round(wpos,1), wrot
  
  PARENT.rotation = 0 
  
  for w in würfel:
    if eval(f'w.position.{rot_achse} != {schicht}'): continue
    w.parent = PARENT


app = Ursina()
window.borderless = False
PARENT = Entity(model='cube', size = 0.2)

würfel = []
for pos in product(range(-1,2), repeat=3):
  würfel.append(Entity(position=pos, model='Teil_46_model.obj', texture='Teil_46_texture.png', scale=0.5))

EditorCamera()
app.run()