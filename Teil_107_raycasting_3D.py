import pygame as pg, random as rnd, math


def get_intersect(a, b, c, d):
  ab, cd, ac = a - b, c - d, a - c
  if not (nenner := ab.x * cd.y - ab.y * cd.x): return
  t = (ac.x * cd.y - ac.y * cd.x) / nenner
  u = -(ab.x * ac.y - ab.y * ac.x) / nenner
  if 0 <= t <= 1 and 0 <= u <= 1: return a.lerp(b, t)


def ray_casting(wände):
  c = spieler_pos
  pg.draw.circle(left,'green',c,10)
  raster = breite/2/sicht
  
  for i in range(sicht):
    _, winkel_player = spieler_richt.as_polar()
    ray = V2(3000,0).rotate(winkel_player-sicht/2+i)
    d = spieler_pos + ray
    entfernungen = [(c.distance_to(k), k) for a, b in wände if (k := get_intersect(a, b, c, d))]
    if not entfernungen: continue
    
    #diese Berechnung vermeidet den Fish-Eye-Effekt, danke an Gpopcorn
    #https://github.com/Gpopcorn/raycasting/blob/main/raycasting.py
    dist, intersect = min(entfernungen)
    dist *= math.cos(math.radians(i-sicht/2))
    color = [max(0,255-dist/1.5)]*3
    wand_höhe = (10/dist * 2500)
    
    pg.draw.line(left, 'green', c, intersect, 1)
    pg.draw.rect(right, color, (raster*i,höhe/2-wand_höhe/2,raster,wand_höhe))


V2 = pg.Vector2
pg.init()
größe = breite, höhe = V2(1920, 1080)
zentrum = größe/2

fenster = pg.display.set_mode(größe)
left = pg.surface.Surface((breite/2,höhe))
right = pg.surface.Surface((breite/2,höhe))

clock = pg.time.Clock()
pg.key.set_repeat(10)
FPS = 40

sicht = 60 #Sichtbereich in Grad
spieler_pos, spieler_richt = zentrum/2,V2(1,0)
wände = [tuple(V2(rnd.randrange(breite/2), rnd.randrange(höhe)) for _ in range(2)) for _ in range(10)]
maus_empflindlichkeit = 0.5

while True:
  clock.tick(FPS)
  left.fill('black')
  right.fill('black')
  
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT: quit()
    if ereignis.type == pg.KEYDOWN:
      match ereignis.key:
        case pg.K_ESCAPE: quit()
        case pg.K_w: spieler_pos += spieler_richt
        case pg.K_d: spieler_pos += spieler_richt.rotate(90)
        case pg.K_a: spieler_pos += spieler_richt.rotate(-90)
        case pg.K_s: spieler_pos += spieler_richt.rotate(180)
    if ereignis.type == pg.MOUSEWHEEL:
      sicht += ereignis.y

  
  rel_pos = V2(pg.mouse.get_rel())*maus_empflindlichkeit
  spieler_richt = spieler_richt.rotate(rel_pos.x)
        
  ray_casting(wände)
  for a, b in wände:
    pg.draw.line(left, 'white', a, b, 3)
  
  fenster.blit(left,(0,0))
  fenster.blit(right,(breite/2,0))
  pg.draw.line(fenster,'blue',(breite/2,0), (breite/2,höhe),5)
  pg.display.flip()
