import pygame as pg
import random as rnd


class Element(pg.sprite.Sprite):
  def __init__(self, id, typ, image, pos, enabled):
    super().__init__()
    self.id = id
    self.typ = typ
    self.image_e = pg.image.load(image + '_e.png')
    self.image_d = pg.image.load(image + '_d.png')
    self.enabled = enabled
    self.image = self.image_e.copy() if enabled else self.image_d.copy()
    self.rect = self.image.get_rect()
    self.rect.topleft = pos
    self.selektiert = False

  def change_enabled(self, t):
    self.enabled = t
    self.image = self.image_e.copy() if enabled else self.image_d.copy()


def clicked_button(e):
  if e.id == 0:
    start_würfeln(e)


def clicked_würfel(e):
  e.selektiert = not e.selektiert
  e.image = e.image_d if e.selektiert else e.image_e


def start_würfeln(e):
  global anim_würfeln, würfel_zähler
  pg.time.set_timer(pg.USEREVENT, 1000, True)
  anim_würfeln = True
  würfel_zähler += 1
  if würfel_zähler == 3:
    e.change_enabled(False)


def würfeln():
  for e in group_elemente:
    if e.typ != 'Würfel' or e.selektiert: continue
    e.id = rnd.randint(1, 6)
    e.image_e = bild_würfel_e[e.id - 1]
    e.image_d = bild_würfel_d[e.id - 1]
    e.image = e.image_e


pg.init()
BREITE, HÖHE = 1280, 720
FPS = 40
zentrum = (BREITE / 2, HÖHE / 2)
screen = pg.display.set_mode((BREITE, HÖHE))
pg.time.set_timer(pg.USEREVENT, 1000, True)
anim_würfeln = True
würfel_zähler = 1

pfad = 'Teil_063_Bilder/'
bild_gui = pg.image.load(f'{pfad}gui.png')
bild_würfel_e = [pg.image.load(f'{pfad}{n+1}_e.png') for n in range(6)]
bild_würfel_d = [pg.image.load(f'{pfad}{n+1}_d.png') for n in range(6)]
group_elemente = pg.sprite.Group()

for n in range(1, 6):
  pos = (606, 130 + 90 * (n - 1))
  group_elemente.add(Element(n, 'Würfel', f'{pfad}{n}', pos, True))

for n in range(3):
  pos = [(400, 615), (815, 615), (506, 450)]
  enabled = n == 0
  group_elemente.add(Element(n, 'Button', f'{pfad}Button{n}', pos[n], enabled))


weitermachen = True
clock = pg.time.Clock()

while weitermachen:
  clock.tick(FPS)
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT:
      weitermachen = False
    if ereignis.type == pg.USEREVENT:
      anim_würfeln = False
    if ereignis.type == pg.MOUSEBUTTONDOWN:
      point = pg.mouse.get_pos()
      for e in group_elemente:
        if not e.enabled or not e.rect.collidepoint(point): continue
        if e.typ == "Button": clicked_button(e)
        if e.typ == "Würfel": clicked_würfel(e)

  screen.blit(bild_gui, (0, 0))
  group_elemente.draw(screen)
  if anim_würfeln:
    würfeln()

  pg.display.flip()

pg.quit()
