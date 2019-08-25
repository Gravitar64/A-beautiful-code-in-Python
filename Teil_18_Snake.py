import pygame as pg, random as rnd

BREITE, HÖHE = 1000, 600
GRÖßE = 20
score, tempo = 0, 5
snake = [(BREITE//2, HÖHE//2)]
richt_x, richt_y = 1, 0
bonus_x, bonus_y = 300, 300
richtungen = {pg.K_DOWN:(0,1), pg.K_UP: (0,-1), pg.K_LEFT: (-1,0), pg.K_RIGHT: (1,0)}
with open('Teil_18_Highscore.txt','r') as f:
  high = int(f.readline())

pg.init()
screen = pg.display.set_mode([BREITE, HÖHE])
pg.mouse.set_visible(False)

weitermachen = True
clock = pg.time.Clock()

while weitermachen:
  clock.tick(tempo)
  screen.fill((0,0,0))

  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT:
      weitermachen = False
    if ereignis.type == pg.KEYDOWN and ereignis.key in richtungen:
      richt_x, richt_y = richtungen[ereignis.key]

  x,y = snake[-1]
  x,y = x + richt_x * GRÖßE, y + richt_y * GRÖßE
  if x < 0 or x + GRÖßE > BREITE or y < 0 or y + GRÖßE > HÖHE or (x,y) in snake:
    weitermachen = False    
  snake.append((x,y))

  if x == bonus_x and y == bonus_y:
    score += tempo * 10
    tempo += 1
    bonus_x = rnd.randrange(BREITE) // GRÖßE * GRÖßE
    bonus_y = rnd.randrange(HÖHE) // GRÖßE * GRÖßE
  else:
    del snake[0]
  snake_color = pg.Color(0,255,0)
  for i, pos in enumerate(snake):
    x,y = pos
    snake_color.hsva = (120,100//len(snake)*(i+1),100//len(snake)*(i+1))
    pg.draw.rect(screen,(snake_color),(x,y,GRÖßE, GRÖßE))
  pg.draw.rect(screen,(255,0,0),(bonus_x,bonus_y,GRÖßE, GRÖßE))

  farbe = (255,255,0) if score > high else (128,128,128)
  textfläche = pg.font.SysFont('impact', 24).render(f'Score {score:,}', False, farbe)
  screen.blit(textfläche, (BREITE - textfläche.get_width(), 5))

  textfläche = pg.font.SysFont('impact', 28).render(f'High {high:,}', False, farbe)
  screen.blit(textfläche, (BREITE // 2 - textfläche.get_width() // 2, 5))

  textfläche = pg.font.SysFont('impact', 24).render(f'fps {tempo}', False, farbe)
  screen.blit(textfläche, (5, 5))  
  
  pg.display.flip()    

pg.quit()

if score > high:
  print(f'New High Score {score} (old {high})')
  with open('teil_18_highscore.txt','w') as f:
    f.write(str(score))
else:
  print(f'{score:,}')    