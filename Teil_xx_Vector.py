import math


class Vec(tuple):
  def __new__(cls, *args):
    return tuple.__new__(cls, args)

  def __add__(self, other):
    if type(other) in (int, float):
      return Vec(*([x+other for x in self]))
    else:
      return Vec(*([sum(x) for x in zip(self, other)]))

  def __sub__(self, other):
    if type(other) in (int, float):
      return Vec(*([x-other for x in self]))
    else:
      return Vec(*([(a-b) for a, b in zip(self, other)]))

  def __mul__(self, faktor):
    return Vec(*([x * faktor for x in self]))

  def __truediv__(self, divisor):
    return Vec(*([x / divisor for x in self]))

  def abstandManhatten(self, other):
    """Liefert den Manhattan Abstand als Summe der absoluten Differenzen der Einzelkoordinaten von vector1 und vector2, Beispiel: abstand = vector1.ManhattanAbstand(vector2) \
      z.B. Vec1(3,9), Vec2(9,5) = 10 (6 + 4) = abs(3-9) + abs(9-5)"""
    return sum(abs(a-b) for a, b in zip(self, other))

  def abstandEuklid(self, other):
    """Liefert den euklidischen Abstand zwischen vector1 und vector2, Beispiel: abstand = vector1.EuklidAbstand(vector2) \
      z.B. Vec1(3,9), Vec2(9,5) = 7,21 = sqrt(52) = sqrt(36 + 16) = sqrt ((3-9)**2 + (9-5)**2)"""
    return math.sqrt(sum((a-b)**2 for a, b in zip(self, other)))

  def betrag(self):
    """Liefert den Betrag (= Länge) eines Vectors und gibt eine float zurück"""
    return math.sqrt(sum(a ** 2 for a in self))
