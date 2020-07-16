import random as rnd 

class Karte(object):
  def __init__(self, wert, farbe) -> None:
    self.wert = wert
    self.farbe = farbe

  def __repr__(self):
    karten_namen = {10:'T', 11:'J', 12:'Q', 13:'K', 14:'A'}
    name = str(self.wert) if self.wert < 10 else karten_namen[self.wert]
    return name + self.farbe  

class Kartendeck(object):
  def __init__(self):
    self.karten = self._neu_gemischt()

  def _neu_gemischt(self):
    karten = [Karte(w,f) for f in '♤♡♧♢' for w in range(2,15)]
    rnd.shuffle(karten)
    return karten

  def gib(self, anz):
    return [self.karten.pop() for _ in range(anz)]


deck = Kartendeck()
pocket = deck.gib(2)
board = deck.gib(5)

print(pocket)
print(board)


    