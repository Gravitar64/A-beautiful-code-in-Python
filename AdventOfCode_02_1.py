from collections import Counter

anzZweier, anzDreier = 0,0
with open('AdventOfCode_02_1_Input.txt') as f:
  for zeile in f:
    zweierGefunden, dreierGefunden = False, False
    counter = Counter(zeile)
    for key,value in counter.items():
      if value == 3 and not dreierGefunden: 
        anzDreier += 1
        dreierGefunden = True
      if value == 2 and not zweierGefunden:
        anzZweier += 1
        zweierGefunden = True

print(anzDreier*anzZweier)