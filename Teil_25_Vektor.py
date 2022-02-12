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

  def rotate2D(self, rotationspunkt, winkel_grad):
    """
    Rotiert einen Punkt im Uhrzeigersinn um einen gegebenen Winkel um einen gegebenen Rotationspunkt (= Pivot)
    Der Winkel ist in Grad anzugeben. Grad 0 ist horizontal rechts, danach im UZS
    """
    winkel_rad = grad2rad(winkel_grad)
    rx, ry = rotationspunkt
    px, py = self

    qx = rx + math.cos(winkel_rad) * (px - rx) - math.sin(winkel_rad) * (py - ry)
    qy = ry + math.sin(winkel_rad) * (px - rx) + math.cos(winkel_rad) * (py - ry)
    return Vec(qx, qy)

  def runde(self,stellen):
    """ Rundet die Werte im Vektor auf <stellen> stellen hintern komma"""
    return Vec(*tuple(round(a,stellen) for a in self)) 

def pol2cart(winkel_grad, dez, radius=1):
  """Wandelt einen Radius und einen Winkel in Grad in einen x,y-Vector um.
  0 Grad ist horizontal nach rechts, 90 Grad is senkrecht nach unten usw."""
  winkel_rad = math.radians(winkel_grad)
  return Vec(round(radius * math.cos(winkel_rad),dez), round(radius * math.sin(winkel_rad),dez))