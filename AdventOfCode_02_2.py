def AdventOfCode_02_2():
  ids = []
  with open('AdventOfCode_02_1_Input.txt') as f:
    for zeile in f:
      ids.append(zeile.strip())
  
  for a in ids:
    for b in ids:
      if a != b:
        anzAbweichungen = 0
        lösung = ''
        for i,buchstabe in enumerate(a):
          if buchstabe == b[i]:
            lösung = lösung + buchstabe
          else:
            anzAbweichungen += 1
        if anzAbweichungen == 1:
          return lösung    

print(AdventOfCode_02_2())