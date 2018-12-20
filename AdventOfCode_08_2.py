puzzleInput =  open('AdventOfCode_08.txt').read().strip().split()
puzzleInput = [int(i) for i in puzzleInput]  

pos = 0
nodes = {}

def readMetadata():
  global pos, anzNodes
  metaDaten = []
  childIDs = []
  nodesID = pos
  nodes[nodesID] = []
  anzChilds = puzzleInput[pos]
  anzMeta = puzzleInput[pos+1]
  pos += 2
  for i in range(anzChilds):
    childIDs.append(pos)
    readMetadata()
  for i in range(anzMeta):
    metaDaten.append(puzzleInput[pos])
    pos += 1
  nodes[nodesID] = [childIDs, metaDaten]
  


gesamtSumme = 0  
def sumNodes(index):
  global gesamtSumme
  ergebnis = 0
  node = nodes[index]
  if not node[0]:
    gesamtSumme += sum(node[1])
  else:
    for childRef in node[1]:
      if childRef > 0 and childRef <= len(node[0]):
        ergebnis = sumNodes(node[0][childRef-1])
  if ergebnis:
    gesamtSumme += ergebnis
         

readMetadata()
sumNodes(0)
print(gesamtSumme)