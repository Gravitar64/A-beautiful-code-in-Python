import pygame as pg, time


def nächste_generation(generation, regel):
  next_generation = set()
  regel = f'{regel:08b}'[::-1]
  for spalte in range(spalten):
    bits = ['1' if pos % spalten in generation else '0' for pos in [spalte - 1, spalte, spalte + 1]]
    index = int(''.join(bits), base=2)
    if regel[index] == '0': continue
    next_generation.add(spalte)
  return next_generation


pg.init()
größe = breite, höhe = 1920, 1080
fenster = pg.display.set_mode(größe)
fenster.fill('white')

skalierung = 8
spalten, zeilen = breite // skalierung, höhe // skalierung
generation = {spalten // 2}
zeile = regel = 0


while True:
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT or ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE: quit()

  for spalte in generation:
    pg.draw.rect(fenster, 'black', (spalte * skalierung, zeile * skalierung, skalierung, skalierung))

  generation = nächste_generation(generation, regel)
  zeile += 1

  if zeile > zeilen:
    pg.display.flip()
    pg.display.set_caption(f'Elementary Cellular Automata (Regel: {regel})')
    fenster.fill('white')
    zeile, generation, regel = 0, {spalten // 2}, regel + 1
    time.sleep(1)