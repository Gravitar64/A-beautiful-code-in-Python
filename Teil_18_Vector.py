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

  def abstand(self, other):
    """ Liefert den Abstand zwischen vector1 und vector2, Beispiel: abstand = vector1.abstand(vector2)"""
    abstand = sum(abs(a-b) for a, b in zip(self, other))
    return abstand

  def __iter__(self):
    return self.werte.__iter__()

  def __eq__(self, other): 
    return self.werte == other.werte   
