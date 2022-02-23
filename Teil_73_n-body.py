import pygame as pg

class Body:
  def __init__(self,x,y,gx,gy,masse):
    self.pos = pg.Vector2(x,y)
    self.geschw = pg.Vector2(gx,gy)
    self.masse = masse
    self.rad = (masse / 3.141) ** (1/3)

  def update(self,other):
    v_r = other.pos - self.pos
    r = pg.math.Vector2.magnitude(v_r)
    v_rn = v_r / r
    if r > (self.rad + other.rad):
      self.geschw += G * ((self.masse * other.masse) / r**2) * v_rn / self.masse
    else:
      gm = self.masse + other.masse
      self.geschw = (self.masse * self.geschw + other.masse * other.geschw) / gm    
      self.pos = (self.masse * self.pos + other.masse * other.pos) / gm
      self.masse, other.masse = gm, 0
      self.rad = (gm/3.141)**(1/3)
          

screen = pg.display.set_mode((1920,1080))
zentrum = (screen.get_width() / 2, screen.get_height() / 2)

clock = pg.time.Clock()
FPS = 40
G = 5
bodies = []
bodies.append(Body(*zentrum,0,0,200_000))

while True:
  clock.tick(FPS)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT: quit()
    if ereignis.type == pg.MOUSEBUTTONDOWN:
      if ereignis.button == 1:
        pos1 = pg.Vector2(pg.mouse.get_pos())
      if ereignis.button == 3:
        m,i = max([(b.masse,i) for i,b in enumerate(bodies)])
        bodies[i].pos = pg.mouse.get_pos()
        bodies[i].geschw = 0,0

    if ereignis.type == pg.MOUSEBUTTONUP:
      if ereignis.button == 1:
        pos2 = pg.Vector2(pg.mouse.get_pos())
        geschw = pos1 - pos2
        bodies.append(Body(*pos2,*geschw,1000))


  for i in range(len(bodies)):
    for j in range(len(bodies)):
      if i == j or bodies[i].masse == 0 or bodies[j].masse == 0: continue
      bodies[i].update(bodies[j])
  bodies = [b for b in bodies if b.masse > 0]
  screen.fill((0,0,0))
  for body in bodies:
    body.pos += body.geschw / FPS
    pg.draw.circle(screen,'#F2CB05',body.pos,body.rad)

  if pg.mouse.get_pressed()[0]:
    pos2= pg.Vector2(pg.mouse.get_pos())
    pg.draw.line(screen,'#419FD9',pos1, pos2, 1)   
  pg.display.flip()