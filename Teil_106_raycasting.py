import pygame as pg, random as rnd 


#https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection#Given_two_points_on_each_line_segment
def segment_intersection(a,b,c,d):
  t_zähler = (a.x - c.x) * (c.y - d.y) - (a.y - c.y) * (c.x - d.x)
  u_zähler = (a.x - b.x) * (a.y - c.y) - (a.y - b.y) * (a.x - c.x)
  nenner   = (a.x - b.x) * (c.y - d.y) - (a.y - b.y) * (c.x - d.x)
  if not nenner: return
  
  t = t_zähler / nenner
  u = -u_zähler / nenner
  if 0<= t <= 1 and 0<= u <= 1: return a.lerp(b,t)
  

def ray_casting(wände):
  c = V2(pg.mouse.get_pos())
  for ray in rays:
    d = c + ray
    geringste_entfernung, best_pos = 99999, None
    for a,b in wände:
      intersection = segment_intersection(a,b,c,d)
      if intersection:
        entfernung = c.distance_to(intersection)
        if entfernung < geringste_entfernung:
          geringste_entfernung = entfernung
          best_pos = intersection
    if not best_pos: continue      
    pg.draw.line(fenster,'gray20',c,best_pos,1)

pg.init()
größe = breite, höhe = 1920, 1080
fenster = pg.display.set_mode(größe)

V2 = pg.Vector2
wände = [tuple(V2(rnd.randrange(breite), rnd.randrange(höhe)) for _ in range(2)) for _ in range(10)]
rays = [V2(max(größe),0).rotate(w) for w in range(360)]

while True:
  fenster.fill('black')
    
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT or ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE: quit()
  
  for a,b in wände:
    pg.draw.line(fenster, 'white', a, b, 3)

  ray_casting(wände)  
         
  pg.display.flip()