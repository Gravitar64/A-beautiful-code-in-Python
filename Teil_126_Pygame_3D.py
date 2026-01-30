import pygame as pg

DISTANZ, PERSPEKTIVE, WINKEL_DELTA, ZOOM_DELTA = 3, 0.5, 0.3, 0.5 


class Model:
  def __init__(self, punkte, flächen):
    self.punkte = punkte
    self.flächen = flächen
    self.drehpunkt = v3(0,0,0)
    self.rot_winkel = [0,0,0]

  def zeichne(self):
    if any(w != 0 for w in self.rot_winkel):
      self.rotiere()
    if zeige_punkte: 
      for punkt in self.punkte:
        pg.draw.circle(fenster, 'red', self.projeziere(punkt),5)
    
    if not zeige_drahtgitter:
      self.flächen = sorted(self.flächen, 
                            key= lambda x: -sum(self.punkte[i].z for i in x)/len(x))

    for fläche in self.flächen:
      polygon = [self.projeziere(self.punkte[i]) for i in fläche]
      if not zeige_drahtgitter: pg.draw.polygon(fenster,'black',polygon,0)  
      pg.draw.polygon(fenster,'green',polygon,1)  

  def projeziere(self, punkt):
    x,y = punkt.xy / (punkt.z * PERSPEKTIVE + DISTANZ)
    return (x+1)/2*breite, (1-(y+1)/2)*höhe
  
  def zoom(self,delta):
    for punkt in self.punkte:
      punkt.z += delta
    self.drehpunkt.z += delta  
  
  def rotiere(self):
    for punkt in self.punkte:
      punkt -= self.drehpunkt
      for winkel, achse in zip(self.rot_winkel, ((1,0,0),(0,1,0),(0,0,1))):
        punkt.rotate_ip(winkel, achse)
      punkt += self.drehpunkt  


def lade_model(datei):
  punkte, flächen = [], []
  with open(datei) as f:
    for zeile in f.readlines():
      if zeile.startswith('v '):
        punkte.append(v3(list(map(float, zeile.split()[1:]))))
      if zeile.startswith('f '):
        flächen.append([int(p.split('/')[0])-1 for p in zeile.split()[1:]])
  return punkte, flächen      


pg.init()
größe = breite, höhe = 1000,1000
fenster = pg.display.set_mode(größe)

v2, v3 = pg.Vector2, pg.Vector3
clock = pg.time.Clock()
FPS = 60

punkte, flächen = lade_model('Teil_126_monkey.obj')
model = Model(punkte, flächen)
zeige_punkte = zeige_drahtgitter = True

while True:
  clock.tick(FPS)
  fenster.fill('black')

  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT: quit() 
    
    if ereignis.type == pg.KEYDOWN:
      match ereignis.key:
        case pg.K_ESCAPE: quit()
        case pg.K_KP4: model.rot_winkel[1] += WINKEL_DELTA
        case pg.K_KP6: model.rot_winkel[1] -= WINKEL_DELTA
        case pg.K_KP8: model.rot_winkel[0] += WINKEL_DELTA
        case pg.K_KP2: model.rot_winkel[0] -= WINKEL_DELTA
        case pg.K_KP9: model.rot_winkel[2] -= WINKEL_DELTA
        case pg.K_KP1: model.rot_winkel[2] += WINKEL_DELTA
        case pg.K_p: zeige_punkte = not zeige_punkte
        case pg.K_d: zeige_drahtgitter = not zeige_drahtgitter
    
    if ereignis.type == pg.MOUSEWHEEL:
      model.zoom(-ZOOM_DELTA) if ereignis.y > 0 else model.zoom(ZOOM_DELTA)
  
  model.zeichne()
  pg.display.flip()