import pygame as pg


def perspektive(punkt):
  return punkt.xy * 4 / (4 - punkt.z) 


def rotiere(punkte):
  for punkt in punkte:
    punkt.rotate_ip(geschwindigkeit, rot_achsen)
    pg.draw.circle(fenster, 'red', perspektive(punkt) * skalierung + zentrum, 10)


def zeichne(kanten):
  for i,j in kanten:
    a = v2(perspektive(punkte[i]) * skalierung + zentrum)
    b = v2(perspektive(punkte[j]) * skalierung + zentrum)
    pg.draw.line(fenster, 'green', a, b, 2)


pg.init()
v2, v3 = pg.Vector2, pg.Vector3
größe = v2(1920, 1080)
fenster = pg.display.set_mode(größe)
zentrum = v2(*größe / 2)


punkte = [v3(-1, -1, 1),
          v3(1, -1, 1),
          v3(1, 1, 1),
          v3(-1, 1, 1),
          v3(-1, -1, -1),
          v3(1, -1, -1),
          v3(1, 1, -1),
          v3(-1, 1, -1)]

kanten = [(0, 1), (1, 2), (2, 3), (3, 0),  # Vorne
          (4, 5), (5, 6), (6, 7), (7, 4),  # Hinten
          (0, 4), (3, 7),  # Links
          (1, 5), (2, 6)]  # Rechts

skalierung = 280
geschwindigkeit = 0.1
rot_achsen = v3(0.16, 0.35, 0.1)


while True:
  fenster.fill('black')

  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT: quit()
    if ereignis.type == pg.KEYDOWN:
      match ereignis.key:
        case pg.K_ESCAPE: quit()

  rotiere(punkte)
  zeichne(kanten)

  pg.display.flip()
