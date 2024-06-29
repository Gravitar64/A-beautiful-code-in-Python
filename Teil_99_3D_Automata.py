import itertools, collections, ursina, random


def nachbarn(pos, typ):
  x, y, z = pos
  if typ == VON_NEUMANN:
    for x2, y2, z2 in [(x + 1, y, z), (x - 1, y, z),
                       (x, y + 1, z), (x, y - 1, z),
                       (x, y, z + 1), (x, y, z - 1)]:
      yield x2, y2, z2
  elif typ == MOORE:
    for dx, dy, dz in itertools.product((-1, 0, 1), repeat=3):
      if dx == dy == dz == 0: continue
      yield x + dx, y + dy, z + dz


def nächste_generation(gen1,regel):
  survive, born, lifetime, typ = regel.split('/')
  typ = MOORE if typ == 'M' else VON_NEUMANN
  nachb = collections.Counter([pos for zelle in gen1 for pos in nachbarn(zelle, typ)])
  new_gen = {pos for pos,anz in nachb.items() 
             if anz == int(born) or (anz == int(survive) and pos in gen1)}
  return {pos for pos in new_gen if max(abs(pos[0]), abs(pos[1]), abs(pos[2])) < 10}


def update():
  global gen1, counter, cam
  counter += 1
  cam.rotation_y += 1
  cam.rotation_x += 0.5
  if counter > 500:
    gen_new = nächste_generation(gen1, REGEL)
    to_delete = gen1 - gen_new
    to_create = gen_new - gen1
    
    for pos in to_delete:
      blocks[pos].visible = False
      
    for pos in to_create:
      blocks[pos].visible = True
     
    gen1 = gen_new
    counter = 0  


app = ursina.Ursina()
ursina.window.size = (1000,1000)#ursina.window.color = ursina.color.white
ursina.Entity(model='cube', color=ursina.color.black, scale=20, wireframe=True, unlit=True)
cam = ursina.EditorCamera(scale=-2.5)
ursina.PointLight(x=-15,y=15,z=15,color=ursina.color.red)
ursina.PointLight(x=15,y=-15,z=-15,color=ursina.color.green)

MOORE, VON_NEUMANN = range(2)
SCALE = [0.7]*3
SAMPLE = 200
REGEL = '3/3/5/M'

all_positions = {(x,y,z) for x,y,z in itertools.product(range(-9,10),repeat=3)}

blocks = dict()
for pos in all_positions:
  blocks[pos] = ursina.Entity(model='cube', color=ursina.color.white, position=pos, scale=SCALE, visible=False)

gen1 = set(random.sample(sorted(all_positions),SAMPLE))
for pos in gen1:
  blocks[pos].visible = True

counter = 0  

app.run()     

  
   
 


