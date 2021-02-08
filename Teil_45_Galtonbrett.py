import pygame as pg
import pymunk
import pymunk.pygame_util


def generate_ball():
  ball = pymunk.Body(35, 1)
  ball.position = pg.mouse.get_pos()
  shape = pymunk.Circle(ball, radius=10)
  shape.elasticity = 0.05
  shape.friction = 0.1
  shape.collision_type = 1
  space.add(ball, shape)


def galton_brett():
  abst_x, abst_y = 50, 36
  for ze in range(20):
    for sp in range(30):
      nagel = space.static_body
      nagel.position = (
          sp*abst_x, ze*abst_y) if ze % 2 == 0 else (sp*abst_x + abst_x/2, ze*abst_y)
      shape = pymunk.Circle(nagel, radius=2)
      shape.elasticity = 0.05
      shape.friction = 0.8
      shape.collision_type = 5
      space.add(shape)

  boden = pymunk.Segment(space.static_body, (0, 0), (1000, 0), 5)
  boden.body.position = (0, 1000)
  boden.friction = 0.1
  space.add(boden)

  for sp in range(30):
    tasche = pymunk.Segment(
        space.static_body, (sp*abst_x, 0), (sp*abst_x, -300), 2)
    space.add(tasche)


def play_ping(space, arbiter, data):
  ping.play()
  return True


pg.init()
pg.mixer.init()
pg.mixer.set_num_channels(64)
ping = pg.mixer.Sound('Teil_45_ping.mp3')


auflösung = 1000
screen = pg.display.set_mode((auflösung, auflösung))
zentrum = auflösung / 2

space = pymunk.Space()
space.gravity = (0, 500)
draw_option = pymunk.pygame_util.DrawOptions(screen)
play_event = space.add_collision_handler(1, 5)
play_event.begin = play_ping
galton_brett()

weitermachen = True
clock = pg.time.Clock()

while weitermachen:
  clock.tick(40)
  space.step(1/40)
  if pg.mouse.get_pressed()[0]:
    generate_ball()
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT:
      weitermachen = False
  screen.fill((0, 0, 0))
  space.debug_draw(draw_option)
  pg.display.flip()

pg.quit()
