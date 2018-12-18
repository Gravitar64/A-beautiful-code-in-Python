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


inAbarbeitung = {}
verfügbareArbeiter = 5
dauer = 0
fertig = False
erledigteAufgaben = ''
while not fertig:
  fertig = True
  dauer += 1
  for step, vorarbeiten in abhängigkeiten.items():
    if not vorarbeiten and verfügbareArbeiter:
      inAbarbeitung[step] = ord(step)-4
      verfügbareArbeiter -= 1

  for step in inAbarbeitung:
    inAbarbeitung[step] -= 1

  for step, restzeit in inAbarbeitung.items():
    if step in abhängigkeiten:
      del abhängigkeiten[step]
    if restzeit == 0:
      verfügbareArbeiter += 1
      erledigteAufgaben += step
      for vorarbeiten in abhängigkeiten.values():
        if step in vorarbeiten:
          vorarbeiten.remove(step)

  for restzeit in inAbarbeitung.values():
    if restzeit or abhängigkeiten:
      fertig = False

  for step in erledigteAufgaben:
    if step in inAbarbeitung:
      del inAbarbeitung[step]

print(dauer)
