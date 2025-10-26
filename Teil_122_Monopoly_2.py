from bokeh.plotting import figure, show
from bokeh.io import curdoc
import time


class Objekte:
  def __init__(self, daten):
    self.name = daten[0]
    self.preis_obj = int(daten[1])
    self.preis_haus = int(daten[2])
    self.mieten = list(map(int, daten[3:9]))
    self.gruppe = daten[9]
    self.farbe = daten[10]
    self.wahrsch = float(daten[11])
    self.rentabilität_berechnen()

  def rentabilität_berechnen(self):
    self.rent = []
    besuche = anz_würfe * self.wahrsch
    for häuser in range(6):
      invest = self.preis_obj + häuser * self.preis_haus
      mieteinnahmen = self.mieten[häuser] * besuche
      self.rent.append((mieteinnahmen - invest) / invest * 100)

      if häuser == 0:
        if self.gruppe == "versorgung":
          mieteinnahmen *= 2.5
        elif self.gruppe == "bahnhof":
          mieteinnahmen *= 8
        else:
          mieteinnahmen *= 2
        self.rent.append((mieteinnahmen - invest) / invest * 100)


class Gruppe:
  def __init__(self, name):
    self.name = name
    self.mitglieder = [obj for obj in objekte if obj.gruppe == name]
    self.farbe = self.mitglieder[0].farbe
    self.rentabilität_berechnen()

  def rentabilität_berechnen(self):
    self.rent = []
    for rent_id in range(1, 7):
      d_rent = sum(m.rent[rent_id] for m in self.mitglieder) / len(self.mitglieder)
      self.rent.append(d_rent)


def datei_einlesen():
  objekte = []
  with open("Teil_122_monopoly_2.txt", encoding="UTF-8") as f:
    for zeile in f.readlines():
      daten = zeile.strip().split(",")
      objekte.append(Objekte(daten))
  return objekte


def plot_init(titel):
  curdoc().theme = "dark_minimal"
  f = figure(
    title=titel,
    x_axis_label="Anz. Häuser",
    y_axis_label="Rentabilität in %",
    sizing_mode="stretch_both",
    tools="wheel_zoom, pan, reset, hover",
    tooltips="$name Rentabilität @y%",
  )
  return f


anz_würfe = 171  # für einen Mitspieler
objekte = datei_einlesen()
gruppen = [Gruppe(name) for name in set(obj.gruppe for obj in objekte)]

f1 = plot_init("Rentabilität Objekte")
x = list(range(6))
for obj in objekte:
  f1.line(x, obj.rent[0:1] + obj.rent[2:], color=obj.farbe, line_width=5, name=obj.name)
show(f1)

time.sleep(0.5)

f2 = plot_init("Rentabilität Gruppen")
x = list(range(6))
for obj in gruppen:
  f2.line(x, obj.rent, color=obj.farbe, line_width=5, name=obj.name)
show(f2)
