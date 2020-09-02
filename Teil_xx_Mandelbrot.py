import pygame
import sys

SCREENWIDTH = 800
SCREENHEIGHT = 600
max_iteration = 255

pygame.init()

screen = pygame.display.set_mode(
    (SCREENWIDTH, SCREENHEIGHT), pygame.DOUBLEBUF | pygame.HWSURFACE)
pygame.display.set_caption("Mandelbrot Fractal")

fractal = screen.copy()

pygame.mixer.init()


fractal.fill((0, 0, 0))
for i in range(SCREENWIDTH):
  print(i)
  for j in range(SCREENHEIGHT):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          sys.exit()

    x0 = (float(i)/SCREENWIDTH)*3.5 - 2.5
    y0 = (float(j)/SCREENHEIGHT)*2 - 1

    x = 0
    y = 0

    iteration = 0

    while x*x + y*y < 2*2 and iteration < max_iteration:
      xtemp = x*x - y*y + x0
      y = 2*x*y + y0

      x = xtemp

      iteration = iteration + 1

    fractal.set_at((i, j), (iteration, iteration, iteration))

    screen.blit(fractal, (0, 0))
    pygame.display.flip()

running = True

while running:
	# Events
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        sys.exit()
