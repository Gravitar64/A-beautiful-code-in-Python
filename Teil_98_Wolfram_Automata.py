import pygame as pg
import time


def next_generation(gen1,rules):
  gen2 = []
  for i in range(len(gen1)):
    bits = [gen1[i-1], gen1[i], gen1[(i+1) % len(gen1)]]
    i = int(''.join(str(n) for n in bits),2)
    gen2.append(rules[i])
  return gen2


pg.init()
größe = breite, höhe = 1920, 1080
fenster = pg.display.set_mode(größe)
clock = pg.time.Clock()
FPS = 80

skalierung = 10
gen1 = [0]*(breite//skalierung)
gen1[len(gen1)//2] = 1
rule = 0
rule_bits = f'{rule:08b}'[::-1]
y=0


# Zeichenschleife mit FPS Bildern pro Sekunde
while True:
  clock.tick(FPS)

  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT or \
       ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE:
      quit()

  if y > höhe//skalierung:
    rule = (rule + 1) % 256
    rule_bits = f'{rule:08b}'[::-1]
    y=0
    gen1 = [0]*(breite//skalierung)
    gen1[len(gen1)//2] = 1
    fenster.fill('black')
    time.sleep(1) 
    pg.display.set_caption(f'Elementary Cellular Automaton (rule {rule})')


  for x,n in enumerate(gen1):
    if n != '0': continue
    pg.draw.rect(fenster, 'white', (x * skalierung, y*skalierung, skalierung, skalierung))

  y+=1
  gen1 = next_generation(gen1,rule_bits)
  
  pg.display.flip()

