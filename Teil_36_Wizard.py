from collections import deque
import random as rnd

SIMULATIONEN = 10000

def string2karten(input_str):
  return [(int(k[0:-1]), k[-1])for k in input_str.split()]

def ermittel_mögliche_karte(karten):
  zu_bedienende_karten = [k for k in karten if k[1] == zu_bedienende_farbe and k[0] < 14]
  if not zu_bedienende_karten:
    return rnd.choice(karten)
  else:
    return rnd.choice(zu_bedienende_karten + [k for k in karten if k[0] > 13])

def ermittel_stich_gewinner(stich, höchster_wert = -1):
  if all([k[0] == 14 for _, k in stich]): return stich[0][0]
  for name, (wert,farbe) in stich:
    if wert == 15: return name
    if wert == 14: continue
    if farbe == trumpf_farbe: wert += 20
    if wert > höchster_wert and farbe in (zu_bedienende_farbe, trumpf_farbe):
      höchster_wert = wert
      stich_gewinner = name
  return stich_gewinner    



spieler_namen = deque("a b c d".split())
ich_spieler = "a"
eigene_karten = string2karten(input("Eigene Karten (1-13, Narr=14, Zauberer=15 + Farbe(yrgb): "))
trumpf_karte = string2karten(input("Trumpf-Karte: "))
trumpf_farbe = trumpf_karte[0][1]
wer_startet = input("Wer startet: ")
#wenn der Narr aufgedeckt wird, gibt es keine Trumpf-Farbe
if trumpf_karte[0][0] == 14: trumpf_farbe = ''
#wenn der Wizard aufgedeckt wird, kann der ausspielende Spieler auswählen,
#nachdem er seine Karten geprüft hat, welche Farbe Trumpf sein soll
if trumpf_karte[0][0] == 15: 
  trumpf_farbe = input(f'Welche Farbe ist Trumpf (Spieler {wer_startet})? ')


DECK = [(wert,farbe) for wert in range(1,16) for farbe in 'rbgy' if (wert,farbe) not in (eigene_karten + trumpf_karte)]
spieler_stiche = {name:0 for name in spieler_namen}


for _ in range(SIMULATIONEN):
  deck = DECK.copy()
  rnd.shuffle(deck)

  spieler_karten = {name:[deck.pop() for _ in range(len(eigene_karten))] for name in spieler_namen if name != ich_spieler}
  spieler_karten[ich_spieler] = eigene_karten.copy()
  spieler_namen.rotate(-spieler_namen.index(wer_startet))
  while spieler_karten[ich_spieler]:
    zu_bedienende_farbe = -1
    stich = []
    for name in spieler_namen:
      wert, farbe = ermittel_mögliche_karte(spieler_karten[name])
      if wert < 14 and zu_bedienende_farbe == -1:
        zu_bedienende_farbe = farbe
      spieler_karten[name].remove((wert,farbe))
      stich.append((name, (wert, farbe)))
    stich_gewinner = ermittel_stich_gewinner(stich)
    spieler_stiche[stich_gewinner] += 1
    spieler_namen.rotate(-spieler_namen.index(stich_gewinner))

print(spieler_stiche[ich_spieler] / SIMULATIONEN)


  






