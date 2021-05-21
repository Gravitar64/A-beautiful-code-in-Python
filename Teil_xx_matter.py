import matter
import random as rnd


def make_boxes():
  Engine = Matter.Engine
  Render = Matter.Render
  World = Matter.World
  Bodies = Matter.Bodies

  # create an engine
  engine = Engine.create()
  for _ in range(10):
    x,y,w,h = rnd.randint(400), rnd.randint(200), rnd.randint(80), rnd.randint(80), 
    box = Bodies.rectangle(x,y,w,h)
    World.add(engine.world, box)
  ground = Bodies.rectangle(400, 610, 810, 60, {'isStatic': True})
  World.add(engine.world, ground)

  render = Render.create({
      'element': document.body,
      'engine': engine
  })
  # run the engine
  Engine.run(engine)

  # run the renderer
  Render.run(render)



if __name__ == '__main__':
  matter.show([make_boxes, drop])
