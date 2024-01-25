import pygame as pg
import time


def get_next_rule():
  rule = -1
  while True:
    rule = (rule + 1) % 256 
    yield rule, f'{rule:08b}'[::-1]
    

def next_generation(gen,rules):
  gen2 = set()
  l = breite//skalierung
  for x in range(l):
    bits = [(x-1)%l in gen, x in gen, (x+1)%l in gen]
    i = int(''.join(str(int(n)) for n in bits),2)
    if rules[i]=='1': gen2.add(x)
  return gen2


pg.init()
größe = breite, höhe = 1920,1080
fenster = pg.display.set_mode(größe)


skalierung = 10
gen = {breite//skalierung//2}
gnr = get_next_rule()
rule, bits = next(gnr)
y=0

counter = gesamtzeit = 0
# Zeichenschleife mit FPS Bildern pro Sekunde
while True:
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT or \
       ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE:
      quit()

  for x in gen:
    pg.draw.rect(fenster, 'black', (x * skalierung, y*skalierung, skalierung, skalierung))

  y+=1
  t = time.perf_counter()
  gen = next_generation(gen,bits)
  gesamtzeit += time.perf_counter()-t
  counter += 1
  durchschnitt = gesamtzeit/counter
  
  if y > höhe//skalierung:
    pg.display.set_caption(f'Elementary Cellular Automaton (rule {rule})')
    pg.display.flip()
    rule, bits = next(gnr)
    y=0
    gen = {breite//skalierung//2}
    fenster.fill('white')
    print(durchschnitt)
    time.sleep(1)