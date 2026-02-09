import pyray as pr

class Player():
  def __init__(self, file, pos, tiles, animation):
    self.img = pr.load_texture(file)
    self.pos = pr.Vector2(*pos)
    self.tiles = tiles
    self.w, self.h = self.img.width/tiles, self.img.height
    self.animation = animation
    self.frame = self.timer = 0

  def show(self):
    self.timer += pr.get_frame_time()
    if self.timer > self.animation:
      self.timer = 0
      self.frame = (self.frame+1) % self.tiles
    pr.draw_texture_rec(self.img, (self.w*self.frame,0,self.w,self.h),self.pos,pr.RAYWHITE)  


pr.init_window(1000,1000,'RayLib für Python')
pr.set_target_fps(40)
player = Player('RayLib_scarfy.png',(20,100),6,0.1)

while not pr.window_should_close():
  
  pr.begin_drawing()
  pr.clear_background(pr.GRAY)
  player.show()
  pr.draw_fps(10,10)
  pr.end_drawing()

pr.close_window()  