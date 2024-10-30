def zeige_brett():
  feld_nr = 1
  for zeile in brett:
    for feld in zeile:
      print(f'| {feld_nr if feld == "-" else feld} ', end='')
      feld_nr += 1
    print('|')


def zug(spieler):
  while True:
    position = int(input(f"Zug Spieler {spieler} (1-9): "))-1
    z, s = position // 3, position % 3
    if brett[z][s] == '-': break
  brett[z][s] = spieler
  zeige_brett()


def gewinner(spieler):
  if max(zeile.count(spieler) for zeile in brett) == 3: return True
  if max(spalte.count(spieler) for spalte in zip(*brett)) == 3: return True
  if [brett[i][i] for i in range(3)].count(spieler) == 3: return True
  if [brett[i][2 - i] for i in range(3)].count(spieler) == 3: return True


brett = [['-'] * 3 for _ in range(3)]
spieler, freie_felder = "X", 9
zeige_brett()

while freie_felder:
  zug(spieler)
  freie_felder -= 1
  if (gewonnen := gewinner(spieler)): break
  spieler = 'X' if spieler == 'O' else 'O'

if gewonnen:
  print(f'Spieler {spieler} hat gewonnen! Glückwunsch!')
else:
  print('Unentschieden')