puzzleInput = open('AdventOfCode_08.txt').read().strip().split()
puzzleInput = [int(i) for i in puzzleInput]

pos = 0
nodes = {}


def readMetaData():
  global pos
  childIDs = []
  metaDaten = []
  nodeID = pos
  nodes[nodeID] = []
  anzChilds = puzzleInput[pos]
  anzMeta = puzzleInput[pos+1]
  pos += 2
  for i in range(anzChilds):
    childIDs.append(pos)
    readMetaData()
  for i in range(anzMeta):
    metaDaten.append(puzzleInput[pos])
    pos += 1
  nodes[nodeID] = [childIDs, metaDaten]


gesamtSumme = 0


def sumNodes(index):
  global gesamtSumme
  node = nodes[index]
  if not node[0]:
    gesamtSumme += sum(node[1])
  else:
    for meta in node[1]:
      if meta > 0 and meta <= len(node[0]):
        sumNodes(node[0][meta-1])


readMetaData()
sumNodes(0)
print(gesamtSumme)
