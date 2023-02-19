import time


def dp(zielsumme):
  möglichkeiten = [1]+[0]*zielsumme
  for münze in [200, 100, 50, 20, 10, 5, 2, 1]:
    for i in range(münze, zielsumme+1):
      möglichkeiten[i] += möglichkeiten[i-münze]
  return möglichkeiten[-1]


start = time.perf_counter()
print(f'{dp(200)} Möglichkeiten')
print(time.perf_counter()-start)
