import time
start = time.perf_counter()

receips = '37'
von = 509671
bis = von + 10

elf1, elf2 = 0,1

for i in range(bis):  
  score = int(receips[elf1]) + int(receips[elf2])
  receips += str(score)
  lr = len(receips)
  elf1 = (elf1 + int(receips[elf1])+ 1) % lr
  elf2 = (elf2 + int(receips[elf2])+ 1) % lr
  
print(receips[von:bis])
print(time.perf_counter()-start)
  