import re


def edl_einlesen(datei):
  with open(datei, encoding="UTF-8") as f:
    inhalt = f.read()
    beschreibungen = re.findall("M:(.*) \|", inhalt)
    timecodes = re.findall("\d*:\d*:\d*", inhalt)
  return beschreibungen, timecodes


datei = "Teil_120_Timeline 1.edl"
beschreibungen, timecodes = edl_einlesen(datei)
for tc, b in zip(timecodes[::4], beschreibungen):
  print(f"{tc} {b}")
