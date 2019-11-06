import random as rnd 

k_namen = {11:'J', 12:'Q', 13:'K', 14:'A'}
k_farben = '♠ ♥ ♦ ♣'.split()


class Karte:
  def __init__(self, wert, farbe, name):
    self.wert = wert
    self.farbe = farbe
    self.name = name

  def __repr__(self):
    return self.name+self.farbe

  def __lt__(self, other):
    return self.wert < other.wert

class Hole:
  def __init__(self, deck):
    self.karten = deck.austeilen(2)
    self.namen = self.namen_ermitteln()

  def namen_ermitteln(self):
    namen = ""
    for karte in self.karten:
      namen = namen + karte.name
    return namen
    

  def __repr__(self):
    return self.karten   

class Board:
  def __init__(self, deck):
    self.karten = deck.austeilen(5)
    

  def __repr__(self):
    return self.karten  

class Kartendeck:
  def __init__(self):
    self.karten = self.neu_gemischt()
    

  def neu_gemischt(self):
    karten = []
    for wert in range(2,15):
      for farbe in k_farben:
        name = str(wert) if wert < 11 else k_namen[wert]
        karten.append(Karte(wert, farbe, name))
    rnd.shuffle(karten)
    return karten

  def austeilen(self, anz):
    ausgeteilte_karten = []
    for i in range(anz):
      ausgeteilte_karten.append(self.karten.pop())
    ausgeteilte_karten.sort()
    return ausgeteilte_karten