import random as rnd 
from collections import deque

def ermittle_mögliche_karte(erste_farbe, spieler):
  if erste_farbe == -1: return spieler_karten[spieler].pop()
  karten = spieler_karten[spieler]
  mögliche_karten = [(wert,farbe) for wert,farbe in karten if farbe == erste_farbe and wert < 14]
  if not mögliche_karten:
    mögliche_karten = karten
  else:
    mögliche_karten.extend([(wert,farbe) for wert,farbe in karten if wert > 13])
    if erste_farbe != trumpf: 
      mögliche_karten.extend([(wert,farbe) for wert,farbe in karten if farbe == trumpf])
  mögliche_karte = rnd.choice(mögliche_karten)
  spieler_karten[spieler].remove(mögliche_karte)
  return mögliche_karte

def wandle_input_um(input_string):
  karten = []
  teil_strings = input_string.split()
  for teil_string in teil_strings:
    wert = int(teil_string[:-1])
    farbe = teil_string[-1]
    karten.append((wert,farbe))
  return karten

spieler_namen = deque("Peter Jan Andreas".split())
ich_spieler = "Andreas"
while True:
  ich_karten = wandle_input_um(input('Eigene Karten (1-13, 14=N, 15=Z, ygbr=Farben): '))
  trumpf_karte = wandle_input_um(input('Trumpf Karte: '))
  trumpf = trumpf_karte[0][1]
  wer_startet = input('Wer startet: ')
  anz_karten = len(ich_karten)

  spieler_stich = {name:0 for name in spieler_namen}
  simulationsläufe = 10_000
  DECK = [(wert, farbe) for wert in range(1,16) for farbe in 'rgby' if (wert,farbe) not in (ich_karten + trumpf_karte)]

  for _ in range(simulationsläufe):
    deck = DECK.copy()
    rnd.shuffle(deck)
    spieler_karten = {sp:[deck.pop() for i in range(anz_karten)] for sp in spieler_namen if sp != ich_spieler}
    spieler_karten[ich_spieler] = ich_karten.copy()
    höchster_spieler = wer_startet
    spieler_namen.rotate(-spieler_namen.index(höchster_spieler))
    while spieler_karten[spieler_namen[-1]]:
      höchste_karte = höchste_trumpf_karte = aktuelle_farbe = -1
      stich = {}
      for spieler in spieler_namen:
        stich[spieler] = ermittle_mögliche_karte(aktuelle_farbe , spieler)  
        wert,farbe = stich[spieler]
        if wert == 14: continue
        if wert < 14 and aktuelle_farbe == -1: aktuelle_farbe = farbe
        if höchste_karte < 15 and wert == 15:
          höchste_karte = höchste_trumpf_karte = 15
          höchster_spieler = spieler
        elif farbe == trumpf and wert > höchste_trumpf_karte:
          höchste_trumpf_karte = wert
          höchster_spieler = spieler  
        elif wert > höchste_karte and farbe == aktuelle_farbe and wert != 14 and höchste_trumpf_karte == -1:
          höchste_karte = wert
          höchster_spieler = spieler
      spieler_stich[höchster_spieler] += 1
      spieler_namen.rotate(-spieler_namen.index(höchster_spieler))
  print(f'{ich_spieler} mit durchschnittlich {spieler_stich[ich_spieler]/simulationsläufe:.2f}')
