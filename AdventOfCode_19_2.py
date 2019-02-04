from dataclasses import dataclass
import time 

start = time.perf_counter()
@dataclass
class Sample():
  opCode : str
  A : int
  B : int
  C : int
  

samples = []
with open('.\AdventOfCode_19.txt') as f:
  for zeile in f:
    if '#' in zeile:
      ip_reg=int(zeile[4])
    else:  
      op, A, B, C = zeile.split()
      A, B, C = int(A), int(B), int(C)
      samples.append(Sample(op, A, B, C))

def addr(a, b):
  return register[a] + register[b]

def addi(a, b):
  return register[a] + b 
  
def mulr(a, b):
  return register[a] * register[b]

def muli(a, b):
  return register[a] * b   

def banr(a, b):
  return register[a] & register[b]

def bani(a, b):
  return register[a] & b

def borr(a, b):
  return register[a] | register[b]

def bori(a, b):
  return register[a] | b    

def setr(a, b):
  return register[a]

def seti(a, b):
  return a

def gtir(a, b):
  return 1 if a > register[b] else 0
  
def gtri(a, b):
  return 1 if register[a] > b else 0 

def gtrr(a, b):
  return 1 if register[a] > register[b] else 0

def eqir(a, b):
  return 1 if a == register[b] else 0
  
def eqri(a, b):
  return 1 if register[a] == b else 0 

def eqrr(a, b):
  return 1 if register[a] == register[b] else 0   
  
functions = {'addr':addr, 'addi':addi, 'mulr':mulr, 'muli':muli, 
             'banr':banr, 'bani':bani, 'borr':borr, 'bori':bori, 
             'setr':setr, 'seti':seti, 'gtir':gtir, 'gtri':gtri, 
             'gtrr':gtrr, 'eqir':eqir, 'eqri':eqri, 'eqrr':eqrr}

def changeIp(sample):
  register[sample.C] = functions[sample.opCode](sample.A, sample.B)
 
      
register = [1,0,0,0,0,0]
ip = 0
for i in range(20):
  register[ip_reg] = ip
  changeIp(samples[ip])
  ip = register[ip_reg]+1

produkt = max(register)  
wurzel = int(produkt ** 0.5)

#suche nach Faktoren, die eine ganzzahlige Division zulassen
faktoren = []
for d in range(1, wurzel +1):
  if produkt % d != 0:
    continue
  faktoren.extend((d, produkt//d))

#die Summe der Faktoren ist die Lösung
print(f'Faktoren : {sorted(faktoren)}')  
print(f'Lösung   = {sum(faktoren)}')  
print(time.perf_counter()-start) 
