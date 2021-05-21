import time
from itertools import accumulate
import random as rnd

unsorted_array = [rnd.randint(1, 1000) for _ in range(100_000)]


def bucket_sort(array):
  for i in range(len(str(array[0]))):
    digit_buckets = {x: [] for x in range(10)}
    for n in array:
      digit_buckets[n // 10**i % 10].append(n)
    array = [x for value in digit_buckets.values() for x in value]
  return array


def flatten(l):
  return [y for x in l for y in x]


def radix(l, p=None, s=None):
  if s == None:
    s = len(str(max(l)))
  if p == None:
    p = s
  i = s - p
  if i >= s:
    return l
  bins = [[] for _ in range(10)]
  for e in l:
    bins[int(str(e).zfill(s)[i])] += [e]
  return flatten([radix(b, p-1, s) for b in bins])


def radix_sort(array):
  for i in range(len(str(array[0]))):
    counts = [0]*10
    for n in array:
      counts[n // 10**i % 10] += 1
    counts = list(accumulate(counts))
    sorted_array = [0]*len(array)
    for n in reversed(array):
      sorted_array[counts[n // 10**i % 10]-1] = n
      counts[n // 10**i % 10] -= 1
    array = sorted_array.copy()
  return array


# time_start=time.perf_counter_ns()
# sorted_array1=bucket_sort(unsorted_array)
# print(time.perf_counter_ns()-time_start)
# time_start=time.perf_counter_ns()
# sorted_array2=sorted(unsorted_array)
# print(time.perf_counter_ns()-time_start)
# time_start=time.perf_counter_ns()
# sorted_array3=radix_sort(unsorted_array)
# print(time.perf_counter_ns()-time_start)
time_start = time.perf_counter_ns()
sorted_array4 = radix(unsorted_array)
print(time.perf_counter_ns()-time_start)
