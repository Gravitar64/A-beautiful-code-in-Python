import pygame as pg, time


def nächste_generation(generation, regel):
  gen2 = set()
  regel = f'{regel:08b}'[::-1]
  for spalte in range(max_spalten):
    bits = ['1' if pos % max_spalten in generation else '0' for pos in [spalte-1, spalte, spalte+1]]
    index = int(''.join(bits),2)
    if regel[index] == '0': continue
    gen2.add(spalte)
  return gen2


pg.init()
größe = breite, höhe = 1920,1080
fenster = pg.display.set_mode(größe)
fenster.fill('white')

skalierung = 8
max_spalten, max_zeilen = breite//skalierung, höhe//skalierung
generation = {max_spalten//2}
regel = zeile = 0

while True:
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT or \
        ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE:
      quit()
  for spalte in generation:
    pg.draw.rect(fenster,'black',(spalte*skalierung, zeile*skalierung, skalierung, skalierung))

  generation = nächste_generation(generation, regel)
  zeile += 1

  if zeile > max_zeilen:
    pg.display.set_caption(f'Regel: {regel}')
    pg.display.flip()
    time.sleep(1)
    fenster.fill('white')
    zeile, generation, regel = 0, {max_spalten//2}, regel+1