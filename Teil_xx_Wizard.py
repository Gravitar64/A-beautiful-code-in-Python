import random as rnd 
from collections import deque

class Karte:
  def __init__(self,wert,farbe):
    self.wert = wert
    self.farbe = farbe

  def __repr__(self):
    name = str(self.wert)+self.farbe
    if self.wert == 14:
      name = 'Narr'
    if self.wert == 15:
      name = 'Zauberer'
    return name

  def __eq__(self, other):
    return self.wert == other.wert and self.farbe == other.farbe  

class Deck:
  def __init__(self):
    self.karten = []
    self.neues_deck()

  def neues_deck(self):
    self.karten = [Karte(wert, farbe) for wert in range(1,16) for farbe in 'rgby']
    rnd.shuffle(self.karten)

  def gib(self,anz):
    return [self.karten.pop() for _ in range(anz)]

  def gib_karten(self,karten):
    self.karten = list(filter(lambda k: k not in karten, self.karten))

class Spieler:
  def __init__(self):
    self.karten = []
    self.stiche = 0

  def gib(self,karte):
    self.karten.remove(self.karten.index(karte))
  


def an_der_reihe(name):
  namen.rotate(-namen.index(name))

def nächster_spieler():
  namen.rotate(-1)

deck = Deck()
namen = deque('Andreas Jan Peter Franzi'.split())
ich = 'Andreas'
spielers = {}
for name in namen:
  if name == ich: continue
  spielers[name] = Spieler()
  spielers[name].karten = deck.gib(9)

for name, val in spielers.items():
  print(name, val.karten)

# def ermittle_mögliche_karte(erste_farbe, spieler):
#   karten = spieler_karten[spieler]
#   trumpf = trumpf_karte[0][1]
#   mögliche_karten = [(wert,farbe) for wert,farbe in karten if farbe == erste_farbe and wert < 14]
#   if not mögliche_karten:
#     mögliche_karten = karten
#   else:
#     mögliche_karten.extend([(wert,farbe) for wert,farbe in karten if wert > 13])
#     if erste_farbe != trumpf: 
#       mögliche_karten.extend([(wert,farbe) for wert,farbe in karten if farbe == trumpf])
#   mögliche_karte = rnd.choice(mögliche_karten)
#   spieler_karten[spieler].remove(mögliche_karte)
#   return mögliche_karte

# def wandle_input_um(input_string):
#   karten = []
#   farbe2wert = dict(y=0, g=1, b=2, r=3)
#   teil_strings = input_string.split()
#   for teil_string in teil_strings:
#     wert = int(teil_string[:-1])
#     farbe = farbe2wert[teil_string[-1]]
#     karten.append((wert,farbe))
#   return karten

# def liefer_reihenfolge(spieler_namen, start_name):
#   namen = deque(spieler_namen)
#   namen.rotate(-namen.index(start_name))
#   return namen

# spieler_namen = "Peter Jan Andreas".split()
# anz_spieler = len(spieler_namen)
# ich_spieler = "Andreas"
# while True:
#   ich_karten = wandle_input_um(input('Eigene Karten (1-13, 14=N, 15=Z, ygbr=Farben): '))
#   trumpf_karte = wandle_input_um(input('Trumpf Karte: '))
#   #print(trumpf_karte)
#   wer_startet = input('Wer startet: ')
#   anz_karten = len(ich_karten)

#   spieler_stich = {name:0 for name in spieler_namen}
#   simulationsläufe = 10_000

#   for _ in range(simulationsläufe):
#     deck = [(wert, farbe) for wert in range(1,16) for farbe in range(4)]
#     deck.remove(trumpf_karte[0])
#     rnd.shuffle(deck)
#     for karte in ich_karten:
#       deck.remove(karte)
#     spieler_karten = {sp:[deck.pop() for i in range(anz_karten)] for sp in spieler_namen if sp != ich_spieler}
#     spieler_karten[ich_spieler] = ich_karten.copy()
#     #print(spieler_karten)
#     höchster_spieler = wer_startet
#     while spieler_karten[ich_spieler]:
#       höchste_karte = höchste_trumpf_karte = aktuelle_farbe = -1
#       stich = {}
#       for spieler in liefer_reihenfolge(spieler_namen, höchster_spieler):
#         if aktuelle_farbe == -1:
#           stich[spieler] = spieler_karten[spieler].pop()
#         else:
#           stich[spieler] = ermittle_mögliche_karte(aktuelle_farbe , spieler)  
#         wert,farbe = stich[spieler]
#         if wert == 14: continue
#         if wert < 14 and aktuelle_farbe == -1: aktuelle_farbe = farbe
#         if höchste_karte < 15 and wert == 15:
#           höchste_karte = höchste_trumpf_karte = 15
#           höchster_spieler = spieler
#         elif farbe == trumpf_karte[0][1] and wert > höchste_trumpf_karte:
#           höchste_trumpf_karte = wert
#           höchster_spieler = spieler  
#         elif wert > höchste_karte and farbe == aktuelle_farbe and wert != 14 and höchste_trumpf_karte == -1:
#           höchste_karte = wert
#           höchster_spieler = spieler
#       spieler_stich[höchster_spieler] += 1
#       #print(stich)
#       #print(höchste_karte, höchste_trumpf_karte, höchster_spieler)
#   print(f'{ich_spieler} mit durchschnittlich {spieler_stich[ich_spieler]/simulationsläufe:.2f}')







