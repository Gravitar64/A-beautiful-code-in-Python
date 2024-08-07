import pygame as pg
import pymunk
import pymunk.pygame_util


def generiere_ball():
  body = pymunk.Body(35, 1)
  body.position = pg.mouse.get_pos()
  shape = pymunk.Circle(body, radius=5)
  shape.elasticity = 0.05
  shape.friction = 0.1
  shape.collision_type = 1
  space.add(body, shape)


def generiere_galtonbrett():
  dx, dy = 50, 43
  for ze in range(3, 15):
    for sp in range(40):
      body = space.static_body
      body.position = (dx * sp, dy * ze) if ze % 2 else (dx * sp + dx / 2, dy * ze)
      shape = pymunk.Circle(body, radius=2)
      shape.elasticity = 0.05
      shape.friction = 0.8
      shape.collision_type = 2
      space.add(shape)

  boden = pymunk.Segment(space.static_body, (0, 0), (1000, 0), 5)
  boden.body.position = (0, 1000)
  space.add(boden)

  for sp in range(40):
    tasche = pymunk.Segment(space.static_body, (dx * sp, 0), (dx * sp, -300), 2)
    space.add(tasche)


def play_ping(space, arbiter, data):
  ping.play()
  return True


def zeichne_text(text, pos, farbe):
  screen.blit(pg.font.SysFont('impact', 40).render(text, False, farbe), pos)


pg.init()
pg.mixer.init()
pg.mixer.set_num_channels(64)
ping = pg.mixer.Sound('Teil_045_ping.mp3')

auflösung = (1000, 1000)
screen = pg.display.set_mode(auflösung)
zentrum = 1000 / 2

space = pymunk.Space()
space.gravity = (0, 500)
space.sleep_time_threshold = 0.5
draw_options = pymunk.pygame_util.DrawOptions(screen)
kollision = space.add_collision_handler(1, 2)
kollision.begin = play_ping

generiere_galtonbrett()

weitermachen = True
clock = pg.time.Clock()

while weitermachen:
  clock.tick(40)
  space.step(1 / 40)
  if pg.mouse.get_pressed()[0]:
    generiere_ball()
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT:
      weitermachen = False
  screen.fill((0, 0, 0))
  space.debug_draw(draw_options)
  anz_bälle = sum(b.body_type == pymunk.Body.DYNAMIC for b in space.bodies)
  anz_sleep = sum(b.is_sleeping for b in space.bodies)
  zeichne_text(f'Bälle = {anz_bälle}', (800, 10), pg.Color('grey'))
  zeichne_text(f'sleep = {anz_sleep}', (800, 65), pg.Color('grey'))

  pg.display.flip()

pg.quit()
