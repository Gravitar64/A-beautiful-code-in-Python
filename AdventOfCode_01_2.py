zahlen = []
zwischenErgebnisse = {}

with open('AdventOfCode_01_1_Input.txt') as f:
  for zeile in f:
    zahlen.append(int(zeile))

zwischenErgebnis = 0
ergebnisGefunden = False
anzLoops = 0
while not ergebnisGefunden:
  anzLoops += 1
  print(anzLoops)
  for zahl in zahlen:
    zwischenErgebnis += zahl
    if zwischenErgebnis in zwischenErgebnisse:
      print(zwischenErgebnis)
      ergebnisGefunden = True
      break
    else:
      zwischenErgebnisse[zwischenErgebnis]=False