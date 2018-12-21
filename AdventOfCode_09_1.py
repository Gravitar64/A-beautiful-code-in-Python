from collections import defaultdict, deque

puzzleInput =  open('AdventOfCode_09.txt').read().strip().split()
players, marbles  = int(puzzleInput[0]), int(puzzleInput[6])

marble, pos = 1, 0
circle = deque([0])
scoreList = defaultdict(int)
while marble < marbles:
  if marble % 23 != 0:
    pos += 2
    circle.rotate(-pos)
    circle.appendleft(marble)
  else:
    scoreList[player] += marble
    pos -= 7
    circle.rotate(-pos)
    scoreList[player] += circle.popleft()   
  marble += 1
  pos = 0
  player = (marble) % players 
    
print(max(scoreList.values()))  
      

