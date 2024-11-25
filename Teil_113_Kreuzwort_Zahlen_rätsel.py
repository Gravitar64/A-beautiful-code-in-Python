import pygame as pg


def lade_rätsel(datei):
  with open(datei) as f:
    raster = [zeile.split() for zeile in f.readlines()]
    lz = raster[-1]
    gelöst = {lz[i]: lz[i + 1] for i in range(0, len(lz) - 1, 2)}
  return raster[:-1], gelöst


def zeichne_bildschirm():
  fenster.fill('white')
  pg.draw.rect(fenster, 'gray50', (900, 0, 300, 980))
  for z, zeile in enumerate(raster):
    for s, nummer in enumerate(zeile):
      rect_zelle = pg.Rect(s * zelle_br, z * zelle_hö, zelle_br, zelle_hö)
      if sel_nummer == nummer:
        pg.draw.rect(fenster, 'yellow', rect_zelle)
      if nummer == '0':
        pg.draw.rect(fenster, 'gray40', rect_zelle)
      else:
        t = pg.font.SysFont('Arial', 14).render(nummer, True, 'black')
        fenster.blit(t, rect_zelle.topleft + pg.Vector2(3, 1))
      if nummer in gelöst:
        t = pg.font.SysFont('Arial_bold', 48).render(gelöst[nummer], True, 'black')
        rect_t = t.get_rect(midbottom=rect_zelle.midbottom)
        fenster.blit(t, rect_t)
      pg.draw.rect(fenster, 'black', rect_zelle, 1)

  for z, buchstabe in enumerate(ungelöst):
    rect_buchst = pg.Rect(1030, z * buchst_hö, zelle_br, buchst_hö)
    pg.draw.rect(fenster, 'white', rect_buchst, 1)
    t = pg.font.SysFont('Arial', 32).render(buchstabe, True, 'white')
    rect_t = t.get_rect(center=rect_buchst.center)
    fenster.blit(t, rect_t)
  pg.display.flip()


def click(sel_nummer, sel_buchst):
  x, y = pg.mouse.get_pos()
  z, s = y // zelle_hö, x // zelle_br

  if x < 900 and raster[z][s] != '0':
    sel_nummer = raster[z][s]
    sel_buchst = False
    if pg.mouse.get_pressed(3)[2] and sel_nummer in gelöst:
      del gelöst[sel_nummer]
      sel_nummer = False

  if x >= 900 and sel_nummer:
    sel_buchst = ungelöst[y // buchst_hö]
    gelöst[sel_nummer] = sel_buchst
    sel_buchst = False

  return sel_nummer, sel_buchst


pg.init()
größe = breite, höhe = 1200, 980
fenster = pg.display.set_mode(größe)
clock = pg.time.Clock()
FPS = 40

raster, gelöst = lade_rätsel('Teil_113_Kreuzwort_Zahlen_rätsel_01.txt')
zeilen, spalten = len(raster), len(raster[0])
zelle_br, zelle_hö = 900 // spalten, höhe // zeilen
buchst_hö = höhe // 26
ungelöst = sorted({chr(i) for i in range(65, 91)} - set(gelöst.values()))
sel_nummer = sel_buchst = False
zeichne_bildschirm()


while True:
  clock.tick(FPS)

  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT or ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE: quit()
    if ereignis.type == pg.MOUSEBUTTONDOWN:
      sel_nummer, sel_buchst = click(sel_nummer, sel_buchst)
      ungelöst = sorted({chr(i) for i in range(65, 91)} - set(gelöst.values()))
      zeichne_bildschirm()
