import networkx as nx
from time import perf_counter as t1


def gen_graph(labyrinth):
  g = nx.DiGraph()
  leer = {(x, y) for y, z in enumerate(labyrinth) for x, b in enumerate(z) if b == ' '}
  löcher = {(x, y) for y, z in enumerate(labyrinth) for x, b in enumerate(z) if b == 'O'}
  zu_besuchen = [(6, 9)]
  besucht = set()

  while zu_besuchen:
    pos1 = x, y = zu_besuchen.pop(0)
    besucht.add(pos1)

    for dx, dy in richtungen:
      for multi in range(1, 20):
        pos2 = x2, y2 = x+dx*multi, y+dy*multi
        if pos2 in leer: continue
        if pos2 in löcher:
          pos2 = [loch for loch in löcher if loch != pos2][0]
        else:
          pos2 = x2, y2 = x2-dx, y2-dy
          multi -= 1
        if pos2 in besucht: break
        #stattdessen if (pos1,pos2) in g.edges: break um die kürzeste Distanz zu finden
        g.add_edge(pos1, pos2, weight=multi, richtung=richtungen[(dx, dy)])
        zu_besuchen.append(pos2)
        break
  return g


start = t1()
labyrinth = [z[:20] for z in open('Teil_94_Labyrinth.txt')]
richtungen = {(-1, 0): 'L', (1, 0): 'R', (0, 1): 'D', (0, -1): 'U'}

g = gen_graph(labyrinth)
pfad = nx.dijkstra_path(g, (6, 9), (19, 17))
züge = len(pfad)-1
distanz = nx.path_weight(g, pfad, 'weight')
lösungswort = ''.join([g.edges[pos1, pos2]['richtung'] for pos1, pos2 in zip(pfad, pfad[1:])])

print(f'Lösungswort = {lösungswort}')
print(f'Anzahl Züge = {züge}, Distanz = {distanz}')
print(f'Ermittelt in {t1()-start:.5f} Sek.')
