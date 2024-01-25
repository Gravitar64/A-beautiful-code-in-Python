import pygame as pg
import time


def get_next_rule():
  rule = -1
  while True:
    rule = (rule + 1) % 256 
    yield rule, f'{rule:08b}'[::-1]
    

def next_generation(gen,rules):
  gen2 = set()
  for x in range(breite//skalierung):
    bits = [x-1 in gen, x in gen, x+1 in gen]
    i = int(''.join(str(int(n)) for n in bits),2)
    if rules[i]=='1': gen2.add(x)
  return gen2


pg.init()
größe = breite, höhe = 800,640
fenster = pg.display.set_mode(größe)


skalierung = 10
gen = {breite//skalierung//2}
gnr = get_next_rule()
rule, bits = next(gnr)
y=0


# Zeichenschleife mit FPS Bildern pro Sekunde
while True:
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT or \
       ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE:
      quit()

  for x in gen:
    pg.draw.rect(fenster, 'black', (x * skalierung, y*skalierung, skalierung, skalierung))

  y+=1
  gen = next_generation(gen,bits)
  
  
  if y > höhe//skalierung:
    pg.display.set_caption(f'Elementary Cellular Automaton (rule {rule})')
    pg.display.flip()
    rule, bits = next(gnr)
    y=0
    gen = {breite//skalierung//2}
    fenster.fill('white')
    time.sleep(1)