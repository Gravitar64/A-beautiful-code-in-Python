import random as rnd


class Karte:
  def __init__(self,karte,verdeckt):
    self.karte = karte
    self.verdeckt = verdeckt
    self.quelle = ''

  def __repr__(self):
    return f'{self.quelle}{"🂠" if self.verdeckt else ""}{self.karte}'


def auswahl_karten(stapel, werte):
  return [k for k in stapel if k.karte in werte]


def auswahl_farben(stapel, farben):
  return [k for k in stapel if k.karte[1] in farben]


def umdrehen(stapel):
  for k in stapel: k.verdeckt = not k.verdeckt


def abheben(stapel):
  # mitte = len(stapel)//2
  # varianz = int(mitte*0.2)
  # teilen = rnd.randrange(mitte-varianz, mitte+varianz+1)
  teilen = rnd.randrange(len(stapel))
  return stapel[:teilen], stapel[teilen:]


for _ in range(100_000):
  karten = [Karte(wert+farbe, True) for wert in '23456789TJQKA' for farbe in '♠♥♦♣']

  st_zu = auswahl_karten(karten, ['A♠'])
  st_zu += rnd.sample(auswahl_farben(karten, '♣'),9)
  st_zu += rnd.sample(auswahl_farben(karten, '♥♦'),15)

  for karte in st_zu:
    karte.quelle = 'Z'
    karten.remove(karte)

  st_ma = karten

  rnd.shuffle(st_zu)
  rnd.shuffle(st_ma)

  for _ in range(2):

    st_ma_verbleib, st_ma_wechselt = abheben(st_ma)
    umdrehen(st_ma_wechselt)
    st_zu_verbleib, st_zu_wechselt = abheben(st_zu)
    umdrehen(st_zu_wechselt)

    st_ma = st_ma_verbleib + st_zu_wechselt
    st_zu = st_zu_verbleib + st_ma_wechselt

    rnd.shuffle(st_zu)
    rnd.shuffle(st_ma)

    # print(f'Zuschauer: {sorted(st_zu,key=lambda x:x.quelle)}')
    # print(f'Magier   : {sorted(st_ma,key=lambda x:x.quelle)}')

  umdrehen(st_ma)
  karten = st_ma + st_zu
  rnd.shuffle(karten)

  verdeckte = [k for k in karten if k.verdeckt]
  schwarze = auswahl_farben(verdeckte, '♠♣')
  assert(len(verdeckte) == 25)
  assert(len(schwarze) == 10)
  assert(len(auswahl_karten(schwarze,['A♠'])) == 1)




