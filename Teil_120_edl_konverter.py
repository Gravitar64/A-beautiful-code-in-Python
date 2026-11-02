import re


def edl_einlesen(datei):
  with open(datei, encoding='UTF-8') as f:
    inhalt = f.read()
    beschreibungen = re.findall(r'M:(.*) \|', inhalt)
    timecodes = re.findall(r'\d*:\d*:\d*', inhalt)
  return beschreibungen, timecodes


datei = '/home/andreas/Schreibtisch/Timeline 1.edl'
beschreibungen, timecodes = edl_einlesen(datei)
for tc, b in zip(timecodes[::4], beschreibungen):
  print(f'{tc} {b}')
