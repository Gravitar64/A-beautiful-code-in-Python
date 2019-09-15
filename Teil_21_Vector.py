import math

class Vector:

  def __init__(self, *args):
    """ Erstellt einen Vector, Beispiel: v = Vector(1,2) """
    self.werte = args if len(args) > 0 else (0, 0)

  def __add__(self, other):
    """ Liefert einen Vector mit den Summen der Werte aus vector1 und vector2, Beispiel: v = vector1 + vector2"""
    summen = tuple(a + b for a, b in zip(self, other))
    return Vector(*summen)

  def __mul__(self, faktor):
    """ Liefert einen Vector mit den Produkten der Werte aus vector1 und faktor, Beispiel: v = vector1 * faktor"""
    produkte = tuple(a * faktor for a in self)
    return Vector(*produkte)

  def __iter__(self):
    return self.werte.__iter__()

  def __eq__(self, other): 
    return self.werte == other.werte   

  def ManhattanAbstand(self, other):
    """ Liefert den Manhattan Abstand als Summe der absoluten Differenzen der Einzelkoordinaten von vector1 und vector2, Beispiel: abstand = vector1.ManhattanAbstand(vector2) \
      z.B. Vec1(3,9), Vec2(9,5) = 10 (6 + 4) = abs(3-9) + abs(9-5)"""
    return sum(abs(a-b) for a, b in zip(self, other))
    

  def EuklidAbstand(self, other):
    """ Liefert den euklidischen Abstand zwischen vector1 und vector2, Beispiel: abstand = vector1.EuklidAbstand(vector2) \
      z.B. Vec1(3,9), Vec2(9,5) = 7,21 = sqrt(52) = sqrt(36 + 16) = sqrt ((3-9)**2 + (9-5)**2)"""
    return math.sqr(sum((a-b)**2 for a, b in zip(self, other)))