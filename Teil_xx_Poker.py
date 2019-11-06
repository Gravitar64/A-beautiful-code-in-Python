import Teil_xx_Class_Poker as pkr
import random as rnd 

anz_spieler = 4

rnd.seed()
anz_Treffer = 0
starthand = 'AA'

for sim in range(100_000):
  deck = pkr.Kartendeck()
  holes = []
  for player in range(anz_spieler):
    holes.append(pkr.Hole(deck))
  board = pkr.Board(deck)

  for hole in holes:
    if hole.namen == starthand:
      anz_Treffer += 1

print(f'Wahrscheinlichkeit für {starthand} = {anz_Treffer / (sim * anz_spieler) * 100 :.2f}% oder alle {sim // anz_Treffer * anz_spieler} Hände')
print((sim // anz_Treffer * anz_spieler) ** 2 // 4)


                