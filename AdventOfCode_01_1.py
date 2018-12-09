zahlen = []

with open('AdventOfCode_01_1_Input.txt') as f:
  for zeile in f:
    zahlen.append(int(zeile))

print(sum(zahlen))  