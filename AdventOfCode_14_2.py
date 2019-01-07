import time
start = time.perf_counter()

receips = '37'
sequenze = '509671'
ls = len(sequenze)

elf1, elf2 = 0,1

gefunden = False
while not gefunden: 
  score = int(receips[elf1]) + int(receips[elf2])
  receips += str(score)
  lr = len(receips)
  elf1 = (elf1 + int(receips[elf1])+ 1) % lr
  elf2 = (elf2 + int(receips[elf2])+ 1) % lr
      
  if sequenze in receips[-(ls+1):]:
    if sequenze[-1] == receips[-1]:
      lösung = len(receips)-ls
    else:
      lösung = len(receips)-ls-1
    gefunden = True
  
print(lösung)
print(time.perf_counter()-start)
