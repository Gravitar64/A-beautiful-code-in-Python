import pygame as pg
import random as rnd


def zeichne_kachel(pos):
  x, y = pos[0]*kachel, pos[1]*kachel
  pg.draw.rect(screen, farben[brett[pos]], (x, y, kachel, kachel))
  pg.draw.rect(screen, f'#BBADA0', (x, y, kachel, kachel), 25)
  if brett[pos] == 0:
    return
  text_surface = pg.font.SysFont('Arial', 120).render(
      str(brett[pos]), False, (255, 255, 255))
  text_rect = text_surface.get_rect(center=(x+kachel//2, y+kachel//2))
  screen.blit(text_surface, text_rect)


def verschiebe(key):
  x1, y1 = richtungen[key]
  while True:
    change = False
    for pos, value in brett.items():
      pos2 = (pos[0]+x1, pos[1]+y1)
      if pos2 not in brett or brett[pos] == 0:
        continue
      if brett[pos2] == 0 or brett[pos2] == value:
        change = True
        brett[pos] = 0
        brett[pos2] = value if brett[pos2] == 0 else value*2
    if not change:
      return


def setze_neue_2():
  freie_felder = [pos for pos, value in brett.items() if value == 0]
  if not freie_felder: return False
  brett[rnd.choice(freie_felder)] = 2
  return True
  


farben = {0: '#CDC0B4', 2: '#EEE4DA', 4: '#EDE0C8', 8: '#EDE0C8', 16: '#F59563',
          32: '#F67C60', 64: '#F65E3B', 128: '#EDCF73', 256: '#EDCC62',
          512: '#EDC850', 1024: '#EDC850', 2048: '#EDC22D'}
richtungen = {pg.K_LEFT: (-1, 0), pg.K_RIGHT: (1, 0),
              pg.K_UP: (0, -1), pg.K_DOWN: (0, 1)}

pg.init()
kachel = 200
screen = pg.display.set_mode((kachel*4, kachel*4))
brett = {(x, y): 0 for x in range(4) for y in range(4)}
setze_neue_2()


weitermachen = True
clock = pg.time.Clock()

while weitermachen:
  clock.tick(40)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT:
      weitermachen = False
    if ereignis.type == pg.KEYDOWN and ereignis.key in richtungen:
      verschiebe(ereignis.key)
      if not setze_neue_2():
        print('Game Over')
        weitermachen = False
  for pos in brett:
    zeichne_kachel(pos)
  pg.display.flip()
pg.quit()
