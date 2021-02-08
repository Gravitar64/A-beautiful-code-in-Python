import pygame as pg
import pymunk
import pymunk.pygame_util


def generate_static_pinboard():
  col, row = BREITE // ABSTx*2, BREITE // ABSTy // 6 * 5
  for r in range(4, row+2):
    for pos in range(col):
      body = space.static_body
      body.position = (
          ABSTx * pos, r*ABSTy) if r % 2 == 0 else (ABSTx * pos + ABSTx/2, r*ABSTy)
      circle = pymunk.Circle(body, radius=PS)
      circle.elasticity = 0.05
      circle.friction = 0.8
      circle.collision_type = 5
      space.add(circle)

  base = pymunk.Segment(space.static_body, (0, 0), (BREITE, 0), 5)
  base.body.position = (0, HÖHE)
  base.friction = 0.1
  space.add(base)

  for c in range(col+1):
    section = pymunk.Segment(body, (c*ABSTx, 0), (c*ABSTx, -HÖHE // 4), 2)
    space.add(section)


def generate_ball():
  ball = pymunk.Body(mass=35, moment=1, body_type=pymunk.Body.DYNAMIC)
  ball.position = pg.mouse.get_pos()
  ball_shape = pymunk.Circle(ball, radius=BS)
  ball_shape.elasticity = 0.05
  ball_shape.friction = 0.1
  ball_shape.collision_type = 1
  space.add(ball, ball_shape)


def kill_objects(space):
  for shape in space.shapes:
    if shape.body.body_type != pymunk.Body.DYNAMIC:
      continue
    space.remove(shape, shape.body)


def kill_off_screen(space):
  for shape in space.shapes:
    if shape.body.position.y > 1000:
      space.remove(shape, shape.body)


def zeichne_Text(text, pos, farbe):
  screen.blit(pg.font.SysFont('impact', 40).render(text, False, farbe), pos)


def play_sound(space, arbiter, data):
  ping.play()
  return True


pg.init()
pg.mixer.init()
pg.mixer.set_num_channels(64)
ping = pg.mixer.Sound('ping7.mp3')


BREITE, HÖHE = 1000, 1000
zentrum = BREITE / 2
screen = pg.display.set_mode((BREITE, HÖHE))

space = pymunk.Space()
space.gravity = (0, 500)
space.sleep_time_threshold = 0.5
draw_options = pymunk.pygame_util.DrawOptions(screen)
coll_handler = space.add_collision_handler(1, 5)
coll_handler.begin = play_sound

ABSTx = 50
ABSTy = int(3**0.5/2*ABSTx)
PS = 2
BS = int(ABSTy/2 - 16)

generate_static_pinboard()

weitermachen = True
clock = pg.time.Clock()
FPS = 40

while weitermachen:
  screen.fill((0, 0, 0))
  clock.tick(FPS)
  space.step(1/FPS)
  if pg.mouse.get_pressed()[0]:
    generate_ball()
  elif pg.mouse.get_pressed()[2]:
    kill_objects(space)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT:
      weitermachen = False
  pg.draw.line(screen, (130, 0, 0), (zentrum, 0), (zentrum, HÖHE), 1)
  space.debug_draw(draw_options)
  anz_balls = sum(b.body_type == pymunk.Body.DYNAMIC for b in space.bodies)
  anz_siml = sum(b.is_sleeping for b in space.bodies)
  zeichne_Text(f'Balls = {anz_balls}', (800, 10), pg.Color('grey'))
  zeichne_Text(f'sleep = {anz_siml}', (800, 65), pg.Color('grey'))
  kill_off_screen(space)
  pg.display.flip()

pg.quit()
