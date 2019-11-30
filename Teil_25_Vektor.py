class Vec(tuple):
  """Eigene Vektor-Klasse um 2D-nDimensionale Koordinaten zu hinterlegen und zu addieren, subtrahieren, etc."""
  def __new__(cls, *args):
    return tuple.__new__(cls, args)

  def __add__(self, other):
    return Vec(*tuple(a+b for a, b in zip(self, other)))

  def __sub__(self, other):
    return Vec(*tuple(a-b for a, b in zip(self, other)))

  def __mul__(self, faktor):
    return Vec(*tuple(a*faktor for a in self))

  def abstand(self, other):
    """Liefert den Manhatten-Abstand (https://de.wikipedia.org/wiki/Manhattan-Metrik) zwischen 2 Koordinaten"""
    return sum(abs(a-b) for a, b in zip(self, other))
