import time
start = time.perf_counter()

grid = []
gsn = 7689

def value(x,y,gsn):
  rackID = x + 10
  powerLevel = rackID * y
  powerLevel += gsn
  powerLevel *= rackID
  powerLevel = (powerLevel // 100) % 10
  return powerLevel - 5

for y in range(1,301):
  for x in range(1,301):  
    grid.append(value(x,y,gsn))

maxSum = 0
for quadrat in range(10,12):
  for y in range(1,301-quadrat):
    for x in range(1,301-quadrat):
      qSum = 0
      for q in range(1,quadrat):
        for n in range(1,quadrat):
          qSum += grid[(y+q)*300+(x+n)]
      if qSum > maxSum:
        maxSum = qSum
        lösung = (x+2,y+2,quadrat-1)
  
print(lösung, maxSum)
print(time.perf_counter()-start)