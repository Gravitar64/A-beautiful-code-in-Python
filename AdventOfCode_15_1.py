from dataclasses import dataclass
import networkx as nx
import time

start = time.perf_counter()
map = []
personen = []
nachbarn = [(0, -1), (-1, 0), (1, 0), (0, 1)]
G = nx.Graph()


def xy2i(pos):
  pass


def addPos(pos1, pos2):
  return (pos1[0]+pos2[0], pos1[1]+pos2[1])


def addNodeEdges(G, source):
  G.add_node(source)
  for nachbar in nachbarn:
    target = addPos(source, nachbar)
    if map[xy2i(target)] == '.':
      G.add_edge(source, target)


def printMap():
  print('Runde: ', runde)
  for i, char in enumerate(map):
    print(char, end='')
    if (i+1) % spalten == 0:
      print()
  print()


@dataclass
class Person():
  goblin: bool
  pos: tuple
  attack: int = 3
  hit: int = 200
  alive: bool = True

  def attackEnemy(self, enemy):
    enemy.hit -= self.attack
    if enemy.hit < 0:
      enemy.alive = False
      map[xy2i(enemy.pos)] = '.'
      addNodeEdges(G, enemy.pos)

  def move(self, newPos):
    oldPos = self.pos
    map[xy2i(oldPos)] = '.'
    i = xy2i(newPos)
    if self.goblin:
      map[i] = 'G'
    else:
      map[i] = 'E'
    self.pos = newPos
    G.remove_node(newPos)
    addNodeEdges(G, oldPos)

  def attackFields(self):
    attackFields = []
    for nachbar in nachbarn:
      newPos = addPos(self.pos, nachbar)
      if map[xy2i(newPos)] == '.':
        attackFields.append(newPos)
    return attackFields

  def targets(self):
    targets = []
    for nachbar in nachbarn:
      newPos = addPos(self.pos, nachbar)
      if map[xy2i(newPos)] != '#':
        targets.append(newPos)
    return targets


with open('AdventOfCode_15.txt') as f:
  for y, zeile in enumerate(f):
    zeile = zeile.strip()
    for x, zeichen in enumerate(zeile):
      map.append(zeichen)
      if zeichen == 'G':
        personen.append(Person(True, (x, y)))
      elif zeichen == 'E':
        personen.append(Person(False, (x, y)))
spalten = len(zeile)


def buildGraph():
  G = nx.Graph()
  for i, char in enumerate(map):
    if char == '.':
      G.add_node((i % spalten, i // spalten))
  for node in G.nodes:
    addNodeEdges(G, node)
  G.edges
  return G


def xy2i(pos):
  return pos[1]*spalten+pos[0]


def findAttackEnemy(person, enemies):
  attackEnemies = []
  for enemy in enemies:
    if person.pos in enemy.targets():
      attackEnemies.append(enemy)
  if attackEnemies:
    attackEnemies.sort(key=lambda s: (s.hit, s.pos[1], s.pos[0]))
    return attackEnemies[0]


def findBestPath(person, enemies):
  addNodeEdges(G, person.pos)
  shortestPath = 9999
  bestTargets = set()
  for enemy in enemies:
    for attackField in enemy.attackFields():
      try:
        path = nx.shortest_path(G, person.pos, attackField)
        pathLength = len(path)
        if pathLength < shortestPath:
          shortestPath = pathLength
          bestTargets = set()
        if pathLength <= shortestPath:
          bestTargets.add(attackField)
      except nx.NetworkXNoPath:
        pass
  if bestTargets:
    bestNextMoves = set()
    bestTarget = sorted(bestTargets, key=lambda t: (t[1], t[0]))[0]
    for nachbar in person.attackFields():
      try:
        path = nx.shortest_path(G, nachbar, bestTarget)
        if len(path) < shortestPath:
          G.remove_node(person.pos)
          return nachbar
      except nx.NetworkXNoPath:
        pass
  else:
    G.remove_node(person.pos)


G = buildGraph()
beendet = False
runde = 0
while not beendet:
  runde += 1
  personen = [p for p in personen if p.alive]
  personen.sort(key=lambda p: (p.pos[1], p.pos[0]))
  for person in personen:
    if person.alive:
      enemies = []
      for enemy in personen:
        if enemy.goblin != person.goblin and enemy.alive:
          enemies.append(enemy)
      if not enemies:
        beendet = True
        runde -= 1
        break
      else:
        attackEnemy = findAttackEnemy(person, enemies)
        if attackEnemy:
          person.attackEnemy(attackEnemy)
        else:
          pos = findBestPath(person, enemies)
          if pos:
            person.move(pos)
          attackEnemy = findAttackEnemy(person, enemies)
          if attackEnemy:
            person.attackEnemy(attackEnemy)


summeHitPoints = sum([p.hit for p in personen if p.alive])
print('Vollendete Runden: ', runde)
print('Summe HitPoints  : ', summeHitPoints)
print('Lösung           : ', runde*summeHitPoints)
print('gefunden in        ', time.perf_counter()-start)
