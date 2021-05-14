import random as rnd
from itertools import combinations 

stati = {True:  {'?':'+', '+':'+', '=':'=', '-':'='},
         False: {'?':'-', '-':'-', '=':'=', '+':'='}}

class Kugel():
  def __init__(self, nr, status):
    self.nr = nr
    self.status = status
    self.seite = ''

  def __repr__(self):
    return f'{self.nr}{self.status}'

  def _statusänderung(self, wiegung):
    if wiegung == 'm' and not self.seite:
      return
    if (wiegung == 'm' and self.seite) or (wiegung in 'lr' and not self.seite):
      self.status = '='
      return
    self.status = stati[self.seite == wiegung][self.status]

class Kugeln():
  def __init__(self, gesucht):
    self.kugeln = [Kugel(nr, '?') for nr in range(anz_kugeln)]      
    self.gesucht = gesucht

  def auswerten(self, auf_waage):
    mitte = len(auf_waage)//2
    nicht_auf_waage = set(range(anz_kugeln)) - set(auf_waage)
    self.lrn = {'l': auf_waage[:mitte], 'r': auf_waage[mitte:], '': nicht_auf_waage}
    for seite, nrn in self.lrn.items():
      for nr in nrn:
        self.kugeln[nr].seite = seite
    wiegung = self._wiegen()
    for kugel in self.kugeln:
      kugel._statusänderung(wiegung)
    l = ' '.join(map(str, [k for k in self.kugeln if k.nr in self.lrn['l']]))
    r = ' '.join(map(str, [k for k in self.kugeln if k.nr in self.lrn['r']]))
    n = ' '.join(map(str, [k for k in self.kugeln if k.nr in self.lrn['']]))
    text = f'Gesucht = {self.gesucht}, {wiegung}, [{l} <-> {r}] ({n})\n'
    return wiegung, text  

  def _wiegen(self):
    if self.gesucht.nr in self.lrn['l']:
      return 'l' if self.gesucht.status == '+' else 'r'
    if self.gesucht.nr in self.lrn['r']:
      return 'r' if self.gesucht.status == '+' else 'l'
    return 'm'              


def prüfung(v2lr):
  prüfergebnisse = []
  text = ''
  for nr in range(anz_kugeln):
    gesucht = Kugel(nr,rnd.choice('+-'))
    kugeln = Kugeln(gesucht)
    wiegung, t1 = kugeln.auswerten(range(8))
    if wiegung == 'm':
      _, t2 = kugeln.auswerten([8,9,10,0,1,2])
    else:
      _, t2 = kugeln.auswerten(v2lr)
    kandidaten = [k for k in kugeln.kugeln if k.status != '=']
    prüfergebnisse.append(len(kandidaten) < 4)
    text += t1 + t2 + f'Kandidaten = {kandidaten}\n\n'
  return all(prüfergebnisse), text   

def alle_varianten():
  anz_lösungen = 0
  for v2l in combinations(range(anz_kugeln), 4):
    for v2r in combinations(range(anz_kugeln), 4):
      if set(v2l) & set(v2r): continue
      e, text = prüfung(v2l+v2r)
      if e:
        anz_lösungen += 1
        print(text)
  print(anz_lösungen//2)      



anz_kugeln = 12
alle_varianten()