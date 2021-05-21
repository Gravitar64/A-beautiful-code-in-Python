def fib_iter(n):
  a,b = 0, 1
  for i in range(n-1):
    a,b = b, a+b
  return b

def fib_rek(n):
  if n < 2: return n
  return fib_rek(n-1) + fib_rek(n-2)

cache = {0:0, 1:1}
def fib_cache(n):  
  if n in cache: return cache[n]
  cache[n] = fib_cache(n-1) + fib_cache(n-2)
  return cache[n]

def fib_debug(n,tiefe=0):
  print(f'{"   "*tiefe}Fib({n})')
  if n < 2: return n
  a = fib_debug(n-1,tiefe+1)
  print(f'{"   "*tiefe}Fib_n-1({n-1}) = {a}')
  b = fib_debug(n-2,tiefe+1)
  print(f'{"   "*tiefe}Fib_n-2({n-2}) = {b}')
  print(f'{"   "*tiefe}Fib({n}) = {a+b}')
  return  a+b  

print(fib_cache(50)) 