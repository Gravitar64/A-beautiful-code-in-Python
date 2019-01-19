from dataclasses import dataclass
import collections
import time

start = time.perf_counter()
map = {}
personen = []
# Achtung! Koordinaten enthalten (zeile, spalte oder y,x)-Werte um dann danach sortieren zu können
# (sort pos = y,x nach Leserichtung lt. Aufgabenstellung)
nachbarn = [(-1, 0), (0, -1), (0, 1), (1, 0)]


def addPos(pos1, pos2):
  return (pos1[0]+pos2[0], pos1[1]+pos2[1])


def sucheAttackFields(pos):
  attackFields = []
  for nachbar in nachbarn:
    target = addPos(pos, nachbar)
    if map[target] != '#':
      attackFields.append(target)
  return attackFields


def sucheFreieNachbarn(pos):
  freieNachbarn = []
  for nachbar in nachbarn:
    target = addPos(pos, nachbar)
    if map[target] == '.':
      freieNachbarn.append(target)
  return freieNachbarn


def attackEnemy(person):
  attackEnemies = []
  for pos in sucheAttackFields(person.pos):
    if pos in enemies:
      attackEnemies.append(enemies[pos])
  if attackEnemies:
    enemy = sorted(attackEnemies, key=lambda p: (p.healthPoints, p.pos))[0]
    person.attackEnemy(enemy)
    return True
  return False


@dataclass
class Person():
  typ: str
  pos: tuple
  attack: int
  healthPoints: int = 200

  def attackEnemy(self, enemy):
    enemy.healthPoints -= self.attack
    if enemy.healthPoints < 1:
      map[enemy.pos] = '.'
      
  def move(self, newPos):
    map[self.pos], map[newPos] = map[newPos], map[self.pos]
    self.pos = newPos

with open('AdventOfCode_15.txt') as f:
  for z, zeile in enumerate(f):
    zeile = zeile.strip()
    for sp, zeichen in enumerate(zeile):
      map[(z, sp)] = zeichen
      if zeichen == 'G':
        personen.append(Person(zeichen, (z, sp), 3))
      elif zeichen == 'E':
        personen.append(Person(zeichen, (z, sp), 3))
spalten = len(zeile)


def bfs(person):
  visited, queue, gefundeneZiele = set(), collections.deque(), []
  root = person.pos
  queue.append((root, 0, []))
  visited.add(root)
  tiefe = 0
  while True:
    vertex, d, path = queue.popleft()
    if d > tiefe:
      tiefe += 1
      if gefundeneZiele:
        # zuerst nach zielfeld (zeile, spalte = y,x) und dann nach erstem Schritt zum Ziel (zeile, spalte = y,x) sortieren
        gefundeneZiele.sort(key=lambda x: (x[0], x[1]))
        return gefundeneZiele[0][1]
    for nachbar in sucheFreieNachbarn(vertex):
      if nachbar in visited:
        continue
      visited.add(nachbar)
      queue.append((nachbar, tiefe+1, path+[vertex]))
      if nachbar not in targets:
        continue
      path += [vertex]+[nachbar]
      gefundeneZiele.append([nachbar, path[1]])
    
    if not queue:
      return


beendet = False
runde = 0
while not beendet:
  runde += 1
  personen.sort(key=lambda p: p.pos)
  for person in personen:
    if person.healthPoints < 1:
      continue
    targets = set()
    enemies = {}

    for enemy in personen:
      if person.typ == enemy.typ or enemy.healthPoints < 1:
        continue
      targets.update(sucheFreieNachbarn(enemy.pos))
      enemies[enemy.pos] = enemy
      
    if not enemies:
      beendet = True
      runde -= 1
      break

    if not attackEnemy(person):
      pos = bfs(person)
      if pos:
        person.move(pos)
        attackEnemy(person)


summeHitPoints = sum([p.healthPoints for p in personen if p.healthPoints > 0])
print()
print('Vollendete Runden: ', runde)
print('Summe HitPoints  : ', summeHitPoints)
print('Lösung           : ', runde*summeHitPoints)
print('gefunden in        ', time.perf_counter()-start)
