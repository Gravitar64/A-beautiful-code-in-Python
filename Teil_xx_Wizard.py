import random as rnd
from collections import deque

SIMULATIONEN = 10_000


def ermittle_mögliche_karte(karten):
  farbe_bedienen = [k for k in karten if k[1] == aktuelle_farbe and k[0] < 14]
  if not farbe_bedienen: 
    return rnd.choice(karten)
  return rnd.choice(farbe_bedienen + [k for k in karten if k[0] > 13])


def ermittle_stich_gewinner(stich, höchste_karte=-1):
  if all([k[0] == 14 for _, k in stich]):
    return stich[0][0]
  for name, (wert, farbe) in stich:
    if wert == 14: continue
    if wert == 15: return name
    if farbe == t_farbe: wert += 20
    if wert > höchste_karte and farbe in (aktuelle_farbe, t_farbe):
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
  t_wert, t_farbe = trumpf_karte[0]
  wer_startet = input('Wer startet: ')
  if t_wert == 15:
    t_farbe = input(f'{wer_startet} bestimmt den Trumpf (rgby): ')
  if t_wert == 14:
    t_farbe = None   
  DECK = [(wert, farbe) for wert in range(1, 16)
          for farbe in 'rgby' if (wert, farbe) not in (ich_karten + trumpf_karte)]
  anz_stiche_spieler = {name: 0 for name in spieler_namen}

  for _ in range(SIMULATIONEN):
    deck = DECK.copy()
    rnd.shuffle(deck)
    spieler_karten = {sp: [deck.pop() for i in range(len(ich_karten))]
                      for sp in spieler_namen if sp != ich_spieler}
    spieler_karten[ich_spieler] = ich_karten.copy()
    spieler_namen.rotate(-spieler_namen.index(wer_startet))
    while spieler_karten[wer_startet]:
      aktuelle_farbe, stich = -1, []
      for name in spieler_namen:
        wert, farbe = ermittle_mögliche_karte(spieler_karten[name])
        stich.append((name, (wert, farbe)))
        if aktuelle_farbe == -1 and wert < 14 and stich[0][1][0] != 15: aktuelle_farbe = farbe
        spieler_karten[name].remove((wert, farbe))
      stich_gewinner = ermittle_stich_gewinner(stich)
      anz_stiche_spieler[stich_gewinner] += 1
      spieler_namen.rotate(-spieler_namen.index(stich_gewinner))
  print(
      f'{ich_spieler} mit durchschnittlich {anz_stiche_spieler[ich_spieler]/SIMULATIONEN:.2f}')  
