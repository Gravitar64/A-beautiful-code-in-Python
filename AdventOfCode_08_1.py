puzzleInput =  open('AdventOfCode_08.txt').read().strip().split()
puzzleInput = [int(i) for i in puzzleInput]  

metaSum = pos = 0    

def readMetadata():
  global pos, metaSum
  anzChilds = puzzleInput[pos]
  anzMeta = puzzleInput[pos+1]
  pos += 2
  for i in range(anzChilds):
    readMetadata()
  for i in range(anzMeta):
    metaSum += puzzleInput[pos]
    pos += 1

readMetadata()
print(metaSum)