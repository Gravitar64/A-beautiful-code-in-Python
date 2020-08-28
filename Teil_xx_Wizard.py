import random as rnd 
from collections import deque


def ermittle_mögliche_karte(karten):
  if aktuelle_farbe == -1: return rnd.choice(karten)
  trumpf_karten = [(wert,farbe) for wert,farbe in karten if farbe == trumpf and wert < 14]
  joker = [(wert,farbe) for wert,farbe in karten if wert > 13]
  karten_der_Farbe = [(wert,farbe) for wert,farbe in karten if farbe == aktuelle_farbe and wert < 14]
  if aktuelle_farbe == trumpf:
    if trumpf_karten:
      return rnd.choice((trumpf_karten+joker))
    else:
      return rnd.choice(karten)
  else:
    if karten_der_Farbe:
      return rnd.choice(karten_der_Farbe+joker+trumpf_karten)
    else:
      return rnd.choice(karten)

def input2karten(input_string):
  return [(int(k[:-1]), k[-1]) for k in input_string.split()]

spieler_namen = deque("Peter Jan Andreas".split())
ich_spieler = "Andreas"
while True:
  ich_karten = input2karten(input('Eigene Karten (1-13, Narr=14, Zauberer=15, ygbr=Farben): '))
  trumpf_karte = input2karten(input('Trumpf Karte: '))
  trumpf = trumpf_karte[0][1]
  wer_startet = input('Wer startet: ')
  spieler_stich = {name:0 for name in spieler_namen}
  simulationsläufe = 1
  DECK = [(wert, farbe) for wert in range(1,16) for farbe in 'rgby' if (wert,farbe) not in (ich_karten + trumpf_karte)]
  
  for _ in range(simulationsläufe):
    deck = DECK.copy()
    rnd.shuffle(deck)
    spieler_karten = {sp:[deck.pop() for i in range(len(ich_karten))] for sp in spieler_namen if sp != ich_spieler}
    spieler_karten[ich_spieler] = ich_karten.copy()
    stich_gewinner = wer_startet
    spieler_namen.rotate(-spieler_namen.index(stich_gewinner))
    while spieler_karten[spieler_namen[-1]]:
      höchste_karte = höchste_trumpf_karte = aktuelle_farbe = -1
      for spieler in spieler_namen:
        wert,farbe = ermittle_mögliche_karte(spieler_karten[spieler])
        spieler_karten[spieler].remove((wert,farbe))
        if wert == 14: continue
        if wert < 14 and aktuelle_farbe == -1: aktuelle_farbe = farbe
        if höchste_karte < 15 and wert == 15:
          höchste_karte = höchste_trumpf_karte = 15
          stich_gewinner = spieler
        elif farbe == trumpf and wert > höchste_trumpf_karte:
          höchste_trumpf_karte = wert
          stich_gewinner = spieler  
        elif wert > höchste_karte and farbe == aktuelle_farbe and höchste_trumpf_karte == -1:
          höchste_karte = wert
          stich_gewinner = spieler
      spieler_stich[stich_gewinner] += 1
      
      spieler_namen.rotate(-spieler_namen.index(stich_gewinner))
  print(f'{ich_spieler} mit durchschnittlich {spieler_stich[ich_spieler]/simulationsläufe:.2f}')