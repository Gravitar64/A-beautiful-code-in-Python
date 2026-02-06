import pyray as pr

pr.init_window(1000,1000,'RayLib für Python')
pr.set_target_fps(60)
pr.

model = pr.load_model('Teil_126_monkey.obj')
SCALE = 3
pos = pr.Vector3(0,0,0)

cam = pr.Camera3D((0,0,100), pos, (0,1,0), 90, pr.CameraProjection.CAMERA_PERSPECTIVE)

zeige_drahtgitter = True

while not pr.window_should_close():
  if pr.is_key_pressed(pr.KeyboardKey.KEY_D): zeige_drahtgitter = not zeige_drahtgitter
  pr.update_camera(cam, pr.CameraMode.CAMERA_THIRD_PERSON)
  pr.begin_drawing()
  pr.clear_background(pr.BLACK)
  
  pr.begin_mode_3d(cam)
  if zeige_drahtgitter:
    pr.rl_disable_backface_culling()
    pr.draw_model_wires(model,pos,SCALE,pr.GREEN)
  else:
    pr.draw_model(model,pos,SCALE,pr.BLACK)
    pr.draw_model_wires(model,pos,SCALE,pr.GREEN)
  pr.end_mode_3d()

  pr.draw_fps(10,10)
  pr.end_drawing()

pr.close_window()  