from dataclasses import dataclass

@dataclass
class Sample():
  opCode : int
  A : int
  B : int
  C : int
  regBefore : list
  regAfter : list

samples = []
part1 = True
with open('aoc_16.txt') as f:
  for zeile in f:
    if part1:
      zeile = zeile.strip()
      if 'Before' in zeile:
        regBefore = [int(a) for a in zeile[9:19].split(',')]
        anzLeer = 0  
      elif 'After' in zeile:
        regAfter = [int(a) for a in zeile[9:19].split(',')]
        samples.append(Sample(opCode, A, B, C, regBefore, regAfter))
      elif zeile:
        opCode, A, B, C = [int(a) for a in zeile.split()]
      else:
        anzLeer += 1
        if anzLeer > 2:
          part1 = False

def addr(a, b, register):
  return register[a] + register[b]

def addi(a, b, register):
  return register[a] + b 
  
def mulr(a, b, register):
  return register[a] * register[b]

def muli(a, b, register):
  return register[a] * b   

def banr(a, b, register):
  return register[a] & register[b]

def bani(a, b, register):
  return register[a] & b

def borr(a, b, register):
  return register[a] | register[b]

def bori(a, b, register):
  return register[a] | b    

def setr(a, b, register):
  return register[a]

def seti(a, b, register):
  return a

def gtir(a, b, register):
  return (1 if a > register[b] else 0)
  
def gtri(a, b, register):
  return (1 if register[a] > b else 0)  

def gtrr(a, b, register):
  return (1 if register[a] > register[b] else 0)

def eqir(a, b, register):
  return (1 if a == register[b] else 0)
  
def eqri(a, b, register):
  return (1 if register[a] == b else 0)  

def eqrr(a, b, register):
  return (1 if register[a] == register[b] else 0)   
  
functions = {addr:'addr', addi:'addi', mulr:'mulr', muli:'muli', 
             banr:'banr', bani:'bani', borr:'borr', bori:'bori', 
             setr:'setr', seti:'seti', gtir:'gtir', gtri:'gtri', 
             gtrr:'gtrr', eqir:'eqir', eqri:'eqri', eqrr:'eqrr'}

def listOfPossibleOpcodes(sample):
  possibleOpcodes = []
  C = sample.regAfter[sample.C]
  for func in functions:
    if C == func(sample.A, sample.B, regBefore):
      possibleOpcodes.append(functions[func])
  return possibleOpcodes    
      
  
ergebnis = {}
for i, sample in enumerate(samples):
  ergebnis[i] = listOfPossibleOpcodes(sample)
  
lösung = [kv for kv in ergebnis.items() if len(kv[1]) < 2]
for l in lösung:
  print(l[0], samples[l[0]],l[1])

print(len(samples))
    
