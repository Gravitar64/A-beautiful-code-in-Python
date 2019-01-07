rules = {}
raw = open('AdventOfCode_12.txt').read().split('\n')
for zeile in raw:
  if 'initial state' in zeile:
    initial = zeile[15:]
  else:
    rules[zeile[:5]] = zeile[9:10]

initial = 10000*'.'+initial+10000*'.'
summevor = 0
for n in range (2000):  
  gen = '.'*len(initial)
  for i in range(len(initial)-5):
    cup = initial[i:i+5]    
    if cup in rules:
      gen = gen[:i+2]+rules[cup]+gen[i+3:]
  initial = gen

  summe = 0
  for i, char in enumerate(initial):
    if char == '#':
      summe += i-10000
     
  print(n, summe, summe - summevor)
  summevor = summe 