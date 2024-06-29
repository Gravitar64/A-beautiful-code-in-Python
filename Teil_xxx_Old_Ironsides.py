import pygame as pg
import math

def ermittel_beschleunigung(vel,richtung):
  acc = wind_wahr*0.01 #Windkraft auf den Bootskörper
  acc -= vel*0.1  #Wasserwiderstand
  wind_scheinbar = wind_wahr - vel
  wind_scheinbar_länge, wind_scheinbar_winkel = wind_scheinbar.as_polar()
  segel_anstellwinkel = vel.as_polar()[1]-wind_scheinbar_winkel
  kraft_faktor = math.cos(math.radians(segel_anstellwinkel))
  kraft = wind_scheinbar_länge * kraft_faktor
  kraft_vektor = pg.Vector2(kraft, vel.as_polar()[1])
  pg.draw.line(fenster, 'gray', pos_wind_scheinbar, pos_wind_scheinbar+wind_scheinbar,3)
  pg.draw.line(fenster, 'green', pos_antrieb, pos_antrieb+kraft_vektor,3)
  print(segel_anstellwinkel, kraft_vektor)
  acc += pg.Vector2.from_polar(kraft_vektor)
  return acc/FPS
  a *= wind_scheinbar.magnitude()
  return 
  print(a)
  return 0
#   wind_scheinbar = wind_wahr - vel
#   beta = richtung + 90
#   alpha = wind_scheinbar.as_polar()[1] - richtung
#   alpha_vec = pg.Vector2.from_polar((100,alpha))
#   pg.draw.line(fenster, 'red', pos_winkel, pos_winkel+alpha_vec,3)

#   Fa = wind_scheinbar.rotate(90) * math.sin(alpha) #- wind_scheinbar * math.cos(alpha) 
#   acc = wind_scheinbar / FPS
#   # windrichtung = wind.as_polar()[1]
#   # segelkraft = wind.copy()
#   # winkeldifferenz = windrichtung - richtung
#   # print(windrichtung, richtung, winkeldifferenz)
  
#   # for low in range(-360,361,90):
#   #   if low <= winkeldifferenz < low+90:
#   #     segelkraft *= ((low+90-winkeldifferenz) - winkeldifferenz)/90
#   #     #if low < 0: segelkraft *= -1
#   # segelkraft.rotate_ip(winkeldifferenz)
#   # pg.draw.line(fenster,'green',pos_segelkraft,pos_segelkraft+segelkraft)
#   # acc += segelkraft/FPS
#   return acc  

# # s = pg.Vector2(12*(math.cos(90)), 12*(math.sin(90)))
# # c = pg.Vector2(4*(math.cos(225)), 4*(math.sin(225)))
# # r = s+c
# # print(r)
# # quit()


pg.init()
größe = pg.Vector2(1920, 1080)
fenster = pg.display.set_mode(größe)
clock = pg.time.Clock()
FPS = 40
pg.key.set_repeat(10)

pos = größe / 2
acc = vel = pg.Vector2(0,0)
wind_wahr = pg.Vector2(100, 0)
pos_wind_wahr = pg.Vector2(100,100)
pos_wind_scheinbar = pg.Vector2(100,250)
pos_antrieb = pg.Vector2(100,400)
pos_winkel = pg.Vector2(100,550)
bild = pg.image.load("Teil_104_Boot.png")
bild = pg.transform.scale_by(bild,0.2)
rect = bild.get_rect()
richtung = 0




while True:
  clock.tick(FPS)
  fenster.fill('blue')

  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT or ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE: quit()
    if ereignis.type == pg.KEYDOWN:
      if ereignis.key == pg.K_LEFT:   vel.rotate_ip(-10/FPS);richtung = (richtung + 10/FPS) % 360
      if ereignis.key == pg.K_RIGHT:  vel.rotate_ip(10/FPS);richtung =  (richtung - 10/FPS) % 360
      if ereignis.key == pg.K_a:      wind_wahr.rotate_ip(-10 / FPS)
      if ereignis.key == pg.K_s:      wind_wahr.rotate_ip(10 / FPS)

  
    
  acc = ermittel_beschleunigung(vel, richtung)
  vel += acc / FPS
  pos += vel / FPS
  pg.draw.line(fenster,'white',pos_wind_wahr, pos_wind_wahr+wind_wahr,3)
  rot_bild = pg.transform.rotate(bild, richtung)
  new_rect = rot_bild.get_rect(center = rect.center + pos)
  fenster.blit(rot_bild, new_rect)


  pg.display.flip()
