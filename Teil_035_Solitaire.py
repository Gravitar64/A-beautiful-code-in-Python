from Teil_25_Vektor import Vec

def generiere_feld():
  feld = map(int,
             """9 9 1 1 1 9 9
                9 9 1 1 1 9 9
                1 1 1 1 1 1 1
                1 1 1 0 1 1 1
                1 1 1 1 1 1 1
                9 9 1 1 1 9 9
                9 9 1 1 1 9 9""".split())
             
  feld_dict = {Vec(i % 7, i // 7): f for i, f in enumerate(feld) if f != 9}
  return feld_dict, len(feld_dict)-1


zugfolge = []
richtungen = [Vec(-1, 0), Vec(1, 0), Vec(0, -1), Vec(0, 1)]


def dfs(anz_steine):
  if anz_steine == 1 and feld_dict[(3, 3)] == 1:
    return True
  for p1, inhalt in feld_dict.items():
    if inhalt == 0:
      continue
    for r in richtungen:
      p2, p3 = p1+r, p1+r*2
      if p2 in feld_dict and p3 in feld_dict and \
              feld_dict[p2] == 1 and feld_dict[p3] == 0:
        feld_dict[p1], feld_dict[p2], feld_dict[p3] = 0, 0, 1
        if dfs(anz_steine - 1):
          zugfolge.append((p1, p2, p3))
          return True
        feld_dict[p1], feld_dict[p2], feld_dict[p3] = 1, 1, 0


def zeige_lösung():
  feld_dict, _ = generiere_feld()
  for p1, p2, p3 in zugfolge:
    for i in range(7*7):
      sp, ze = i % 7, i // 7
      if sp == 0:
        print()
      if (sp, ze) in feld_dict:
        print(str(feld_dict[(sp, ze)]) + ' ', end='')
      else:
        print('  ', end='')
    feld_dict[p1], feld_dict[p2], feld_dict[p3] = 0, 0, 1
    print()
    print(f'Zug (Sp, Ze): {p1} - {p3}')
    print()


feld_dict, anz_steine = generiere_feld()
dfs(anz_steine)
zeige_lösung()