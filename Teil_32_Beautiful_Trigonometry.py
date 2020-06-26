import pygame as pg
from Teil_25_Vektor import Vec, pol2cart
import math

def erstelle_segmentliste(anz):
  segmentliste = []
  delta_winkel = math.pi / anz
  for n in range(anz):
    start_winkel = delta_winkel * n
    end_winkel = start_winkel + math.pi
    linie_start = pol2cart(radius, start_winkel) + zentrum
    linie_end = pol2cart(radius, end_winkel) + zentrum
    segmentliste.append((linie_start,linie_end, start_winkel))
  return segmentliste

pg.init()
auflösung = Vec(1000,1000)
screen = pg.display.set_mode(auflösung)
farbe = pg.Color(0)

winkel = 0
rotationsgeschwindigkeit = 0.03
zentrum = auflösung / 2
radius = min(auflösung)*0.40
aufteilungen = 0

clock = pg.time.Clock()
weitermachen = True
show_rotating_point = False
animation = True
konnektoren = False
segmentliste = []

while weitermachen:
  clock.tick(40)

  for event in pg.event.get():
    if event.type == pg.QUIT:
      weitermachen = False
    if event.type == pg.KEYDOWN and event.key == pg.K_KP_PLUS:
      aufteilungen += 1
      segmentliste = erstelle_segmentliste(aufteilungen)
    if event.type == pg.KEYDOWN and event.key == pg.K_KP_MINUS:
      aufteilungen = max(0, aufteilungen-1)
      segmentliste = erstelle_segmentliste(aufteilungen)
    if event.type == pg.KEYDOWN and event.key == pg.K_p:
      show_rotating_point = not show_rotating_point
    if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
      animation = not animation
    if event.type == pg.KEYDOWN and event.key == pg.K_k:
      konnektoren = not konnektoren  

  if not animation:
    continue
  screen.fill((0, 0, 0))
  pg.draw.circle(screen, pg.Color("darkolivegreen1"), zentrum, radius, 1)

  winkel += rotationsgeschwindigkeit
  punkt_pos = pol2cart(radius, winkel) + zentrum

  
  for start,end,segment_winkel in segmentliste:
    pg.draw.line(screen, pg.Color("gray29"), start, end, 1)
    punkt_pos_rotiert = punkt_pos.rotate2D(zentrum, -segment_winkel)
    punkt_projektion = Vec(punkt_pos_rotiert[0], zentrum[0])
    punkt_projektion_rotiert = punkt_projektion.rotate2D(zentrum, segment_winkel)
    pg.draw.circle(screen, pg.Color("darkgoldenrod1"), punkt_projektion_rotiert, 10)

  if show_rotating_point:
    pg.draw.circle(screen, pg.Color("darkolivegreen1"), punkt_pos, 5)
  
  aufteilung = pg.font.SysFont('impact', 24).render(
      f'Aufteilungen =  {aufteilungen}', False, pg.Color("White"))
  screen.blit(aufteilung, (auflösung[0] - 50 - aufteilung.get_width(), 5))
  kommandos = pg.font.SysFont('Arial', 24).render(
      f'Kommandos = + , -, p, space', False, pg.Color("White"))
  screen.blit(kommandos, (10 , 10))


  pg.display.flip()

pg.quit()
