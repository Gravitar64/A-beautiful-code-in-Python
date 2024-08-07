from itertools import combinations_with_replacement
import math

varianten = [v for v in combinations_with_replacement(range(1, 37), 3)
             if math.prod(v) == 36]

for v in varianten:
  print(f'Alter der Mädchen = {v}, Hausnummer: {sum(v)}')
