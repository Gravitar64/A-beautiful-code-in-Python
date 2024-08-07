import time


def münzsumme(summe):
  möglichkeiten = [1] + [0] * summe
  for münze in [1, 2, 5, 10, 20, 50, 100, 200]:
    for i in range(münze, summe + 1):
      möglichkeiten[i] += möglichkeiten[i - münze]
  return möglichkeiten[-1]


start = time.perf_counter()
print(f'{münzsumme(200)} Möglichkeiten')
print(time.perf_counter() - start)
