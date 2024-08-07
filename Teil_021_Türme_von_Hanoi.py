schritte = 0
def hanoi(anzahl, von, temp, ziel):
  global schritte
  if anzahl > 0:
    hanoi(anzahl - 1, von, ziel, temp)
    print(f'Scheibe {anzahl} von {von} nach {ziel}')
    schritte += 1
    hanoi(anzahl - 1, temp, von, ziel) 

hanoi(8, 'A', 'B', 'C')
print(schritte)
