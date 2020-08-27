import random as rnd
from collections import deque, namedtuple
import time


def wandle_input(input_string):
  karten = []
  teil_strings = input_string.split()
  for teil_string in teil_strings:
    wert = int(teil_string[:-1])
    farbe = teil_string[-1]
    karten.append(Karte(wert, farbe))
  return karten


def ermittle_mögliche_karte(erste_farbe, name):
  if erste_farbe == -1:
    return players[name]['karten'].pop()
  karten = players[name]['karten']
  mögliche_karten = [k for k in karten if k.farbe ==
                     erste_farbe and k.wert < 14]
  if not mögliche_karten:
    mögliche_karten = karten
  else:
    mögliche_karten.extend([k for k in karten if k.wert > 13])
    if erste_farbe != trumpf:
      mögliche_karten.extend([k for k in karten if farbe == trumpf])
  mögliche_karte = rnd.choice(mögliche_karten)
  players[name]['karten'].remove(mögliche_karte)
  return mögliche_karte


Karte = namedtuple('Karte', ['wert', 'farbe'])
namen = deque('Andreas Peter Jan Franzi'.split())
players = {name: {'karten': [], 'stiche': 0} for name in namen}
ich_spieler = "Andreas"


while True:
  ich_karten = wandle_input(
      input('Eigene Karten (1-13, 14=N, 15=Z, ygbr=Farben): '))

  trumpf_karte = wandle_input(input('Trumpf Karte: '))
  trumpf = trumpf_karte[0].wert

  name = input(f'Wer startet (ENTER = {namen[1]}): ')
  namen.rotate(-1) if not name else namen.rotate(-namen.index(name))

  DECK = [Karte(wert, farbe) for wert in range(1, 16)
            for farbe in 'rgby' if (wert, farbe) not in (ich_karten+trumpf_karte)]

  simulationsläufe = 10_000

  time_start = time.perf_counter()
  for _ in range(simulationsläufe):
    deck = DECK.copy()
    rnd.shuffle(deck)
    players[ich_spieler]['karten'] = ich_karten.copy()
    for name in namen:
      if name == ich_spieler:
        continue
      players[name]['karten'].extend([deck.pop() for _ in range(len(ich_karten))])
    höchster_spieler = namen[0]
    while players[namen[-1]]['karten']:
      höchste_karte = höchste_trumpf_karte = aktuelle_farbe = -1
      stich = {}
      for name in namen:
        stich[name] = ermittle_mögliche_karte(aktuelle_farbe, name)
        wert, farbe = stich[name]
        if wert == 14:
          continue
        if wert < 14 and aktuelle_farbe == -1:
          aktuelle_farbe = farbe
        if höchste_karte < 15 and wert == 15:
          höchste_karte = höchste_trumpf_karte = 15
          höchster_spieler = name
        elif farbe == trumpf and wert > höchste_trumpf_karte:
          höchste_trumpf_karte = wert
          höchster_spieler = name
        elif wert > höchste_karte and farbe == aktuelle_farbe and wert != 14 and höchste_trumpf_karte == -1:
          höchste_karte = wert
          höchster_spieler = name
      players[höchster_spieler]['stiche'] += 1
      namen.rotate(-namen.index(höchster_spieler))
  print(
      f'{ich_spieler} mit durchschnittlich {players[ich_spieler]["stiche"]/simulationsläufe:.2f}')
  print(time.perf_counter()-time_start)    
