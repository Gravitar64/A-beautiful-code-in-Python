import pygame, random


def particle_update(particles):
  particles2 = dict()
  for (x,y),farbe in particles.items():
    a,b,c = [(x+dx,y+1) for dx in range(-1,2)]
    if b not in particles:
      x,y = b
    elif a not in particles and c not in particles:
      x,y = x+random.choice([-1,1]),y+1
    elif a not in particles:
      x,y = a
    elif c not in particles:
      x,y = c
    particles2[x,min(höhe//skalierung-1,y)]=farbe  
  return particles2    


pygame.init()
größe = breite, höhe = 1920, 1080
fenster = pygame.display.set_mode(größe)
clock = pygame.time.Clock()
FPS = 80
hue = 200

particles = dict()
skalierung=10

# Zeichenschleife mit FPS Bildern pro Sekunde
while True:
  for ereignis in pygame.event.get():
    if ereignis.type == pygame.QUIT or \
       ereignis.type == pygame.KEYDOWN and ereignis.key == pygame.K_ESCAPE:
      quit()

  clock.tick(FPS)
  fenster.fill('black')
        
  if pygame.mouse.get_pressed()[0]:
    farbe = pygame.Color(0)
    hue = (hue+1)%360
    farbe.hsva = hue,50,90
    x,y = pygame.mouse.get_pos()
    particles[x//skalierung, y//skalierung]=farbe
  
  particles = particle_update(particles)
  
  for (x,y), color in particles.items():
    pygame.draw.rect(fenster,color,(x*skalierung,y*skalierung,skalierung,skalierung))

  pygame.display.flip()
