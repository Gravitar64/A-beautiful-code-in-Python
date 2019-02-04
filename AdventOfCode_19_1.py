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
with open('AdventOfCode_19.txt') as f:
  for zeile in f:
    if '#' in zeile:
      ip_reg=int(zeile[4])
    else:  
      op, A, B, C = zeile.split()
      A, B, C = int(A), int(B), int(C)
      samples.append(Sample(op, A, B, C))

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
  return a > register[b]
  
def gtri(a, b, register):
  return register[a] > b  

def gtrr(a, b, register):
  return register[a] > register[b]

def eqir(a, b, register):
  return a == register[b]
  
def eqri(a, b, register):
  return register[a] == b  

def eqrr(a, b, register):
  return register[a] == register[b]   
  
functions = {'addr':addr, 'addi':addi, 'mulr':mulr, 'muli':muli, 
             'banr':banr, 'bani':bani, 'borr':borr, 'bori':bori, 
             'setr':setr, 'seti':seti, 'gtir':gtir, 'gtri':gtri, 
             'gtrr':gtrr, 'eqir':eqir, 'eqri':eqri, 'eqrr':eqrr}

def changeIp(sample,register):
  register[sample.C] = functions[sample.opCode](sample.A, sample.B, register)
  return register  
      
register = [0,0,0,0,0,0]
ip = 0
while ip < len(samples):
  register[ip_reg] = ip
  register = changeIp(samples[ip],register)
  ip = register[ip_reg]+1
    
print(register[0])
print(time.perf_counter()-start)   
