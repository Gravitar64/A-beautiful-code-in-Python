import pygame as pg


PERSPEKTIVE, DISTANZ, WINKEL_DELTA, ZOOM_DELTA = 0.5, 2, 0.2, 0.3

class Model:
  def __init__(self, punkte, flächen):
    self.punkte = punkte
    self.flächen = flächen
    self.drehpunkt = v3(0, 0, 0)
    self.rot_winkel = [0, 0, 0]

  def rotiere(self):
    for punkt in self.punkte:
      punkt -= self.drehpunkt
      for winkel, achse in zip(self.rot_winkel, [(1, 0, 0), (0, 1, 0), (0, 0, 1)]):
        punkt.rotate_ip(winkel, achse)
      punkt += self.drehpunkt

  def zoom(self, delta):
    for punkt in self.punkte:
      punkt.z += delta
    self.drehpunkt.z += delta

  def zeichne(self):
    if any(a != 0 for a in self.rot_winkel):
      self.rotiere()

    if zeige_punkte:
      for vertex in self.punkte:
        pg.draw.circle(fenster, 'red', screen(project(vertex)), 5)

    if not zeige_drahtgitter:
      self.flächen = sorted(self.flächen, key=lambda x: -sum(self.punkte[i].z for i in x) / len(x))

    for face in self.flächen:
      polygon = [screen(project(self.punkte[i])) for i in face]
      if not zeige_drahtgitter:
        pg.draw.polygon(fenster, 'black', polygon, 0)
      pg.draw.polygon(fenster, 'green', polygon, 1)


def load(file):
  punkte, flächen = [], []
  with open(file) as f:
    for line in f.readlines():
      if line.startswith('v '):
        punkte.append(v3(list(map(float, line.split()[1:]))))
      if line.startswith('f '):
        flächen.append([int(p.split('/')[0]) - 1 for p in line.split()[1:]])
  print(
    f'Import {file} erfolgreich. Vericies: {len(punkte):,} Edges: {len(flächen) * 4:,} Faces: {len(flächen):,} '
  )
  return punkte, flächen


def screen(p):
  return v2((p.x + 1) / 2 * breite, (1 - (p.y + 1) / 2) * höhe)


def project(p):
  return v2(p.x / (p.z * PERSPEKTIVE + DISTANZ), p.y / (p.z * PERSPEKTIVE + DISTANZ))


pg.init()
größe = breite, höhe = 1000, 1000
fenster = pg.display.set_mode(größe)

v2, v3 = pg.Vector2, pg.Vector3
clock = pg.time.Clock()
FPS = 60
zeige_punkte = zeige_drahtgitter = True
model = Model(*load('Teil_126_monkey.obj'))

while True:
  clock.tick(FPS)
  fenster.fill('black')

  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT:
      quit()
    if ereignis.type == pg.KEYDOWN:
      match ereignis.key:
        case pg.K_KP4:
          model.rot_winkel[1] += WINKEL_DELTA
        case pg.K_KP6:
          model.rot_winkel[1] -= WINKEL_DELTA
        case pg.K_KP8:
          model.rot_winkel[0] += WINKEL_DELTA
        case pg.K_KP2:
          model.rot_winkel[0] -= WINKEL_DELTA
        case pg.K_KP9:
          model.rot_winkel[2] -= WINKEL_DELTA
        case pg.K_KP1:
          model.rot_winkel[2] += WINKEL_DELTA
        case pg.K_p:
          zeige_punkte = not zeige_punkte
        case pg.K_d:
          zeige_drahtgitter = not zeige_drahtgitter
        case pg.K_ESCAPE:
          quit()
    if ereignis.type == pg.MOUSEWHEEL:
      model.zoom(-ZOOM_DELTA) if ereignis.y > 0 else model.zoom(ZOOM_DELTA)

  model.zeichne()
  pg.display.flip()
