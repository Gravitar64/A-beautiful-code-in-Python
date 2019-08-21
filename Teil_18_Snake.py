import pygame as pg, random as rnd

BREITE, HÖHE, SKALIERUNG = 1000, 600, 20
score, speed = 0, 3
snake = [(BREITE // 2, HÖHE // 2)]
r_x, r_y = 0, 1 
b_x, b_y = 300, 300
richtungen = {pg.K_LEFT: (-1, 0), pg.K_RIGHT: (1, 0), pg.K_DOWN: (0, 1) , pg.K_UP: (0, -1)}

pg.init()
screen = pg.display.set_mode([BREITE, HÖHE])
weitermachen = True
clock = pg.time.Clock()

while weitermachen:
  screen.fill((0, 0, 0))
  clock.tick(speed)
  
  for event in pg.event.get():
    if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
      weitermachen = False
    if event.type == pg.KEYDOWN and event.key in richtungen:
      r_x, r_y = richtungen[event.key]
  
  x, y = snake[-1]
  x, y = x + r_x * SKALIERUNG, y + r_y * SKALIERUNG
  if (x, y) in snake or x < 0 or x+SKALIERUNG > BREITE or y < 0 or y+SKALIERUNG > HÖHE:
    weitermachen = False
  snake.append((x, y))
  
  if x == b_x and y == b_y:
    score += speed * 10
    speed += 1
    b_x = rnd.randrange(BREITE)//SKALIERUNG*SKALIERUNG
    b_y = rnd.randrange(HÖHE)//SKALIERUNG*SKALIERUNG
  else:
    del snake[0]
  
  for x, y in snake:
    pg.draw.rect(screen, (0, 255, 0), (x, y, SKALIERUNG, SKALIERUNG))
  pg.draw.rect(screen, (255, 0, 0),(b_x, b_y, SKALIERUNG, SKALIERUNG))
  
  textsurface = pg.font.SysFont('impact', 28).render(
      f'Score: {score:,}', False, (255, 255, 255))
  screen.blit(textsurface, (BREITE - textsurface.get_width(), 5))
  pg.display.flip()

pg.quit()