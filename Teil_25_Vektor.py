import math

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

  def __truediv__(self, divisor):
    return Vec(*tuple(a / divisor for a in self))  

  def abstand(self, other):
    """Liefert den Manhatten-Abstand (https://de.wikipedia.org/wiki/Manhattan-Metrik) zwischen 2 Koordinaten"""
    return sum(abs(a-b) for a, b in zip(self, other))

  def rotate2D(self, rotationspunkt, winkel_rad):
    """
    Rotiert einen Punkt im Uhrzeigersinn um einen gegebenen Winkel um einen gegebenen Rotationspunkt (= Pivot)
    Der Winkel ist in radiant anzugeben
    """
    rx, ry = rotationspunkt
    px, py = self

    qx = rx + math.cos(winkel_rad) * (px - rx) - math.sin(winkel_rad) * (py - ry)
    qy = ry + math.sin(winkel_rad) * (px - rx) + math.cos(winkel_rad) * (py - ry)
    return Vec(qx, qy)  

def pol2cart(radius, winkel_rad):
  return Vec(radius * math.cos(winkel_rad), radius * math.sin(winkel_rad))