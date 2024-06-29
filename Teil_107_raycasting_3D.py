import pygame as pg, random as rnd, math


def get_intersect(a, b, c, d):
  ab, cd, ac = a - b, c - d, a - c
  if not (nenner := ab.x * cd.y - ab.y * cd.x): return
  t = (ac.x * cd.y - ac.y * cd.x) / nenner
  u = -(ab.x * ac.y - ab.y * ac.x) / nenner
  if 0 <= t <= 1 and 0 <= u <= 1: return a.lerp(b, t)


def ray_casting(wände):
  c = V2(pg.mouse.get_pos())
  breite_rechteck = breite/2/sichtbereich
  for i in range(sichtbereich):
    ray = V2(3000,0).rotate(spieler_richtung-sichtbereich/2+i)
    d = c + ray
    entfernungen = [(c.distance_to(k), k) for a, b in wände if (k := get_intersect(a, b, c, d))]
    if not entfernungen: continue
    
    dist, kreuzungspunkt = min(entfernungen)
    dist *= math.cos(math.radians(i-sichtbereich/2))
    wand_höhe = (10/dist * 2500)
    farbe = [max(10,255-dist/1.5)]*3
    pg.draw.line(fenster_links, 'green', c, kreuzungspunkt, 1)
    pg.draw.rect(fenster_rechts, farbe, (breite_rechteck*i,höhe/2-wand_höhe/2,breite_rechteck,wand_höhe))
    


V2 = pg.Vector2
pg.init()
größe = breite, höhe = 1920, 1080
fenster = pg.display.set_mode(größe)
pg.key.set_repeat(10)

fenster_links, fenster_rechts = pg.surface.Surface((breite/2, höhe)), pg.surface.Surface((breite/2, höhe))

clock = pg.time.Clock()
FPS = 40

wände = [tuple(V2(rnd.randrange(breite//2), rnd.randrange(höhe)) for _ in range(2)) for _ in range(10)]
sichtbereich = 60
spieler_richtung = 0

while True:
  clock.tick(FPS)
  fenster_links.fill('black')
  pg.draw.rect(fenster_rechts,'blue',(0,0,breite/2,höhe/2))
  pg.draw.rect(fenster_rechts,'brown',(0,höhe/2,breite/2,höhe/2))

  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT or ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE: quit()
    if ereignis.type == pg.KEYDOWN:
      match ereignis.key:
        case pg.K_a: spieler_richtung -= 1
        case pg.K_d: spieler_richtung += 1 

  ray_casting(wände)

  for a, b in wände:
    pg.draw.line(fenster_links, 'white', a, b, 3)

  
  fenster.blit(fenster_links,(0,0))  
  fenster.blit(fenster_rechts,(breite/2,0))  
  pg.draw.line(fenster,'blue',(breite/2,0),(breite/2,höhe),5)

  pg.display.flip()