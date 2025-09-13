import random as rnd

zähler = [0] * 40
sonder = {2: "g", 17: "g", 33: "g", 7: "e", 22: "e", 36: "e"}
karten = {"g": [10, 0, 1, "B"] + [None] * 12, "e": [-3, 0, 5, 10, 11, 24, 39] + [None] * 9}
namen = "LOS Badstr Gemeinschaftsfeld Turmstr Einkommensteuer Südbahnhof Chausseestr Ereignisfeld Elisenstr Poststr Gefängnis Seestr Elektrizitätswerk Hafenstr Neue_Str Westbahnhof Münchner_Str Gemeinschaftsfeld Wiener_Str Berliner_Str Frei_Parken Theaterstr Ereignisfeld Museumstr Opernplatz Nordbahnhof Lessingstr Schillerstr Wasserwerk Goethestr Ins_Gefängnis Rathausplatz Hauptstr Gemeinschaftsfeld Bahnhofstr Hauptbahnhof Ereignisfeld Parkstr Zusatzsteuer Schlossalle".split()


pos, sims = 0, 1_000_000
for _ in range(sims):
  wurf = rnd.randrange(1, 7) + rnd.randrange(1, 7)
  pos = (pos + wurf) % 40
  if pos == 30:  pos = 10
  if pos in sonder:
    karte = rnd.choice(karten[sonder[pos]])
    if isinstance(karte, int):
      if karte >= 0:
        pos = karte
      else:
        pos += karte
    elif karte == "B":
      for bahnhof in [5, 15, 25, 35, 45]:
        if pos < bahnhof:
          pos = bahnhof % 40
          break
  zähler[pos] += 1

sortiert = sorted([(besuche, namen[i]) for i, besuche in enumerate(zähler)], reverse=True)

for besuche, name in sortiert:
  print(f"{name:<20} {besuche:,}")
