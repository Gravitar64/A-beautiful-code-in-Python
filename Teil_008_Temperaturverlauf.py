import matplotlib.pyplot as plt
import datetime as dt
from collections import defaultdict

# Textdatei einlesen und Dictionary füllen
tageswert = defaultdict(list)
with open('temperatur_draußen Temp_2.txt') as f:
    for zeile in f:
        datumStr, _, t = zeile.split()
        datum = dt.datetime.strptime(datumStr, '%d.%m.%Y')
        t = float(t)
        tageswert[datum].append(t)

# Tageswerte ermitteln und Messfehler rausfiltern
tagMax, tagMin, tagDatum = [], [], []
for datum, liste in tageswert.items():
    höchst = max(liste)
    tiefst = min(liste)
    if abs(höchst) < 40 and abs(tiefst) < 40:
        tagMax.append(höchst)
        tagMin.append(tiefst)
        tagDatum.append(datum)

# plotten der bereinigten Werte
fig, ax = plt.subplots()
ax.plot(tagDatum, tagMax, lw=1, label='Hi', color='red')
ax.plot(tagDatum, tagMin, lw=1, label='Low', color='blue')
ax.fill_between(tagDatum, tagMax, tagMin,
                facecolor='orange', alpha=0.2, label='range')
ax.grid(linestyle='-', linewidth='0.5', color='green')
ax.legend()
plt.yticks([-10, 0, 25, 30, 35, 40])
plt.show()
