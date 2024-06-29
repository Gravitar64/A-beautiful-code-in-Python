import tcod as tc

WIDTH, HEIGHT = 720,480
FLAGS = tc.context.SDL_WINDOW_RESIZABLE | tc.context.SDL_WINDOW_MAXIMIZED

tileset = tc.tileset.load_tilesheet("dejavu10x10_gs_tc.png", 32, 8, tc.tileset.CHARMAP_TCOD)

console = tc.Console(WIDTH, HEIGHT, order="F")
context = tc.context.new(width=WIDTH, height=HEIGHT, sdl_window_flags=FLAGS)

bsp = tc.bsp.BSP(x=0, y=0, width=80, height=60)
bsp.split_recursive(
    depth=5,
    min_width=3,
    min_height=3,
    max_horizontal_ratio=1.5,
    max_vertical_ratio=1.5,
)

# In pre order, leaf nodes are visited before the nodes that connect them.
for node in bsp.pre_order():
    if node.children:
        node1, node2 = node.children
        print('Connect the rooms:\n%s\n%s' % (node1, node2))
    else:
        print('Dig a room for %s.' % node)
  
while True:  
  console.clear()
  console.print(0, 0, "Hello World!")
  context.present(console, integer_scaling=True)  

  for event in tc.event.wait():
    context.convert_event(event)
    print(event)
    if isinstance(event, tc.event.Quit):
      raise SystemExit()
    elif isinstance(event, tc.event.WindowResized) and event.type == "WINDOWRESIZED":
      pass  