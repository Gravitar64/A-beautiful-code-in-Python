def suche_lösung(pos, besucht):
  besucht.append(pos)
  for delta_sp, delta_ze in [(-1, -2), (1, -2), (-2, -1), (-2, 1), (2, -1), (2, 1), (-1, 2), (1, 2)]:
    zielfeld = pos[0] + delta_sp, pos[1] + delta_ze
    if zielfeld not in rätsel or zielfeld in besucht: continue
    suche_lösung(zielfeld, besucht.copy())

  if len(besucht) == len(rätsel) and rätsel[besucht[-1]][-1] == '.':
    lösungen.append(" ".join([rätsel[p] for p in besucht]))


# Dict tuple(spalte,zeile): str "Wort/Silbe"
rätsel = {(0, 0): "HERZ,", (1, 0): "VER", (2, 0): "WAS", (3, 0): "ES",
          (4, 0): "SUCHT,", (5, 0): "HERZ,", (0, 1): "ET", (1, 1): "ENT",
          (2, 1): "DAS", (3, 1): "DAS", (4, 1): "MAN", (5, 1): "DASS",
          (0, 2): "LO", (1, 2): "EIN", (2, 2): "HAT,", (3, 2): "DASS",
          (4, 2): "EIN", (5, 2): "FÜHLT", (1, 3): "IHM", (2, 3): "BEH",
          (3, 3): "GE", (4, 3): "FÜHLT,", (0, 4): "RE.", (1, 4): "REN",
          (4, 4): "WOHL", (5, 4): "LE;"
          }

lösungen = []
suche_lösung((1, 2), [])

for lösung in lösungen:
  print(lösung)
