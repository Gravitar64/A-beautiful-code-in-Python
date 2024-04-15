import time, itertools

counter = 0
start = time.perf_counter()
for x in range(100):
  for y in range(100):
    for z in range(100):
      counter += 1
time1 = time.perf_counter() - start

start = time.perf_counter()
for x,y,z in itertools.product(range(100), range(100), range(100)):
  counter += 1
time2 = time.perf_counter() - start

print(time1)
print(time2)
print(time2-time1, (time2/time1-1)*100)