import random as rnd
rnd.seed()

SUITS = '♤ ♡ ♧ ♢'.split()
class Karte:
  def __init__(self, wert, farbe):
    self.wert = wert
    self.name = self._name_ermitteln()
    self.farbe = farbe

  def _name_ermitteln(self):
    k_namen = {10: 'T', 11: 'J', 12: 'Q', 13: 'K', 14: 'A'}
    return str(self.wert) if self.wert < 10 else k_namen[self.wert]

  def __str__(self):
    return f'{self.name}{self.farbe}'


class Kartendeck:
  def __init__(self):
    self.karten = self._neu_gemischt()

  def _neu_gemischt(self):
    karten = [Karte(w, f) for f in SUITS for w in range(2, 15)]
    rnd.shuffle(karten)
    return karten

  def geben(self, anz):
    return [self.karten.pop() for _ in range(anz)]

def zeige_karten(karten):
  for k in karten:
    print(k,' ', end='')
  print()  

    
deck = Kartendeck()
pocket = deck.geben(2)
board = deck.geben(5)

zeige_karten(pocket)
zeige_karten(board)
