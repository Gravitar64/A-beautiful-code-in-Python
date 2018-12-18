puzzleInput = []
steps = set()
abhängigkeiten = {}
with open('AdventOfCode_07.txt') as f:
  for zeile in f:
    vor = zeile[5:6]
    nach = zeile[36:37]
    puzzleInput.append((vor, nach))
    steps.update(vor, nach)

for step in steps:
  vorarbeiten = set()
  for zeile in puzzleInput:
    if zeile[1] == step:
      vorarbeiten.add(zeile[0])
  abhängigkeiten[step] = vorarbeiten

möglicheSchritte = set()
lösung = ''
while abhängigkeiten:
  for step, vorarbeiten in abhängigkeiten.items():
    if not vorarbeiten:
      möglicheSchritte.add(step)
  nächsterSchritt = sorted(möglicheSchritte)[0]
  lösung += nächsterSchritt
  möglicheSchritte.remove(nächsterSchritt)
  del abhängigkeiten[nächsterSchritt]

  for vorarbeiten in abhängigkeiten.values():
    if nächsterSchritt in vorarbeiten:
      vorarbeiten.remove(nächsterSchritt)

print(lösung)
