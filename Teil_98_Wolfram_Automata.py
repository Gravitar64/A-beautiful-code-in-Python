import pygame as pg, time


def nächste_generation(generation, regel):
  gen2 = set()
  regel = f'{regel:08b}'[::-1]
  for x in range(max_x):
    bits = ['1' if pos % max_x in generation else '0'for pos in (x-1, x, x+1)]
    i = int(''.join(bits),2)
    if regel[i] != '1': continue
    gen2.add(x)
  return gen2  


pg.init()
größe = breite, höhe = 1920,1080
fenster = pg.display.set_mode(größe)
fenster.fill('white')

skalierung = 8
max_x, max_y = breite // skalierung, höhe // skalierung
generation = {max_x//2}
regel = y = 0


while True:
  for ereignis in pg.event.get():
      if ereignis.type == pg.QUIT or \
          ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE:
        quit()
  
  for x in generation:
    pg.draw.rect(fenster,'black',(x*skalierung, y*skalierung, skalierung, skalierung))

  generation = nächste_generation(generation, regel)
  y+=1

  if y > max_y:
    pg.display.set_caption(f'Elementary Cellular Automaton (Regel = {regel})')
    pg.display.flip()
    fenster.fill('white')
    time.sleep(1)
    regel, y, generation = (regel+1)%256, 0, {max_x//2}