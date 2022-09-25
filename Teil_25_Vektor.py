import math

class Vec(tuple):
  """Eigene Vektor-Klasse um 2 bis nDimensionale Koordinaten zu hinterlegen und zu addieren, subtrahieren, etc."""
  def __new__(cls, *args):
    return tuple.__new__(cls, args)

  def __add__(self, other):
    return Vec(*tuple(a+b for a, b in zip(self, other)))

  def __sub__(self, other):
    return Vec(*tuple(a-b for a, b in zip(self, other)))

  def __mul__(self, faktor):
    return Vec(*tuple(a*faktor for a in self))

  def __truediv__(self, divisor):
    return Vec(*tuple(a / divisor for a in self))  

  def abstand(self, other):
    """Liefert den Manhatten-Abstand (https://de.wikipedia.org/wiki/Manhattan-Metrik) zwischen 2 Vektoren"""
    return sum(abs(a-b) for a, b in zip(self, other))

  def rotate2D(self, rotationspunkt, 𝜙):
    """
    Rotiert einen Punkt im Uhrzeigersinn um einen gegebenen Winkel um einen gegebenen Rotationspunkt (= Pivot)
    Der Winkel ist in Grad anzugeben
    """
    𝜙 = math.radians(𝜙)
    rx, ry = rotationspunkt
    px, py = self

    qx = rx + math.cos(𝜙) * (px - rx) - math.sin(𝜙) * (py - ry)
    qy = ry + math.sin(𝜙) * (px - rx) + math.cos(𝜙) * (py - ry)
    return Vec(qx, qy)  

def pol2cart(radius, 𝜙):
  """Gibt zu einem Radius und eine Winkel die x,y-Koordinaten as Vektor zurück.
  Der Winkel ist in Grad anzugeben"""
  𝜙 = math.radians(𝜙)
  return Vec(radius * math.cos(𝜙), radius * math.sin(𝜙))