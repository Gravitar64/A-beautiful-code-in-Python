import pygame as pg, time


def next_generation(gen,rules):
  gen2 = set()
  l = breite//skalierung
  for x in range(l):
    bits = ['1' if i%l in gen else '0' for i in (x+1,x,x-1)]
    i = int(''.join(bits),2)
    if rules[i]=='1': gen2.add(x)
  return gen2


pg.init()
größe = breite, höhe = 1920,1080
fenster = pg.display.set_mode(größe)
fenster.fill('white')

skalierung = 15
gen = {breite//skalierung//2}
y=rule=0

while True:
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT or \
       ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE:
      quit()

  for x in gen:
    pg.draw.rect(fenster, 'black', (x * skalierung, y*skalierung, skalierung, skalierung))

  gen = next_generation(gen,f'{rule:08b}'[::-1])
  y+=1
    
  if y > höhe//skalierung:
    pg.display.set_caption(f'Elementary Cellular Automaton (rule {rule})')
    pg.display.flip()
    rule, y, gen = rule+1, 0, {breite//skalierung//2}
    fenster.fill('white')
    time.sleep(1)