import random as rnd
from collections import deque

SIMULATIONEN = 10_000
DEBUG_PRINT = False


def ermittle_mögliche_karte(karten):
  if aktuelle_farbe == -1 or len(karten) == 1:
    return rnd.choice(karten)
  trumpf_joker = {k for k in karten if k[1] == trumpf or k[0] > 13}
  karten_der_Farbe = {
      k for k in karten if k[1] == aktuelle_farbe and k[0] < 14}
  if karten_der_Farbe:
    return rnd.choice(list(karten_der_Farbe | trumpf_joker))
  else:
    return rnd.choice(karten)


def ermittle_stich_gewinner(stich, höchste_karte=-1):
  if all([k[0] == 14 for n, k in stich]):
    return stich[0][0]
  for name, (wert, farbe) in stich:
    if wert == 14:
      continue
    if wert == 15:
      return name
    if farbe == trumpf:
      wert += 20
    if wert > höchste_karte and farbe in (aktuelle_farbe, trumpf):
      höchste_karte = wert
      stich_gewinner = name
  return stich_gewinner


def input2karten(input_string):
  return [(int(k[:-1]), k[-1]) for k in input_string.split()]


spieler_namen = deque("Peter Jan Andreas Franzi".split())
ich_spieler = "Andreas"
while True:
  ich_karten = input2karten(
      input('Eigene Karten (1-13, Narr=14, Zauberer=15, ygbr=Farben): '))
  trumpf_karte = input2karten(input('Trumpf Karte: '))
  trumpf = trumpf_karte[0][1]
  wer_startet = input('Wer startet: ')
  spieler_stich = {name: 0 for name in spieler_namen}
  DECK = [(wert, farbe) for wert in range(1, 16)
          for farbe in 'rgby' if (wert, farbe) not in (ich_karten + trumpf_karte)]
  for _ in range(SIMULATIONEN):
    deck = DECK.copy()
    rnd.shuffle(deck)
    spieler_karten = {sp: [deck.pop() for i in range(len(ich_karten))]
                      for sp in spieler_namen if sp != ich_spieler}
    spieler_karten[ich_spieler] = ich_karten.copy()
    spieler_namen.rotate(-spieler_namen.index(wer_startet))
    while spieler_karten[wer_startet]:
      aktuelle_farbe, stich = -1, []
      if DEBUG_PRINT:
        for name in spieler_namen:
          print(name, spieler_karten[name])
      for name in spieler_namen:
        wert, farbe = ermittle_mögliche_karte(spieler_karten[name])
        spieler_karten[name].remove((wert, farbe))
        stich.append((name, (wert, farbe)))
        if wert < 14 and aktuelle_farbe == -1:
          aktuelle_farbe = farbe
      stich_gewinner = ermittle_stich_gewinner(stich)
      if DEBUG_PRINT:
        for name, (wert, farbe) in stich:
          print(name, str(wert)+farbe)
        print(stich_gewinner)
        print()
      spieler_stich[stich_gewinner] += 1
      spieler_namen.rotate(-spieler_namen.index(stich_gewinner))

  print(
      f'{ich_spieler} mit durchschnittlich {spieler_stich[ich_spieler]/SIMULATIONEN:.2f}')
