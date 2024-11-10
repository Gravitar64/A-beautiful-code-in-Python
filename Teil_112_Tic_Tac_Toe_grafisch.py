import pygame as pg


def zeige_brett():
  fenster.fill('gray75')
  fenster.blit(img_grid, (0, 0))
  for zeile in range(3):
    for spalte in range(3):
      inhalt = brett[zeile][spalte]
      if inhalt == 'X': fenster.blit(img_x, (spalte * raster + 40, zeile * raster + 40))
      if inhalt == 'O': fenster.blit(img_o, (spalte * raster + 40, zeile * raster + 40))
  pg.display.flip()


def zug(spieler):
  zeige_brett()
  while True:
    for ereignis in pg.event.get():
      if ereignis.type == pg.QUIT or ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE: quit()
      if ereignis.type == pg.MOUSEBUTTONDOWN and not win:
        x, y = pg.mouse.get_pos()
        zeile, spalte = y // raster, x // raster
        if brett[zeile][spalte] != '-': continue
        brett[zeile][spalte] = spieler
        return gewinner(spieler)


def gewinner(spieler):
  if max(zeile.count(spieler) for zeile in brett) == 3: return True
  if max(spalte.count(spieler) for spalte in zip(*brett)) == 3: return True
  if [brett[i][i] for i in range(3)].count(spieler) == 3: return True
  if [brett[i][2 - i] for i in range(3)].count(spieler) == 3: return True


pg.init()
größe = breite, höhe = 512, 512
fenster = pg.display.set_mode(größe)
raster = breite // 3

img_grid = pg.image.load('Teil_112_grid.png')
img_x = pg.image.load('Teil_112_x.png')
img_o = pg.image.load('Teil_112_o.png')
clock = pg.time.Clock()
FPS = 40

brett = [['-'] * 3 for _ in range(3)]
spieler, freie_felder, win = "X", 9, False
zeige_brett()

while True:
  win = zug(spieler)
  freie_felder -= 1
  if win:
    pg.display.set_caption(f'Spieler {spieler} hat gewonnen!')
  elif freie_felder == 0:
    pg.display.set_caption(f'Unentschieden!')
  spieler = 'O' if spieler == 'X' else 'X'
