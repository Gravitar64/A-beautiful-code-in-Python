def fibi(n):
  a,b = 0,1
  for i in range(n-1):
    a,b = b, a+b
  return b  

def fibr(n):
  if n < 2: return n
  return fibr(n-1) + fibr(n-2)

def fibd(n,tiefe=0):
  print("   "*tiefe, n)
  if n < 2: return n
  a = fibd(n-1,tiefe+1) 
  print("   "*tiefe,"Fib_n-1",a)
  b = fibd(n-2,tiefe+1)    
  print("   "*tiefe,"Fib_n-2",b)
  return a+b

# for n in range(40):
#   print(n,fibr(n)) 
print(fibi(4000))
