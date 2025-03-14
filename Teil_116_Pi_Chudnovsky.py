import math, decimal, time


def chudnovsky(genauigkeit):
  genauigkeit += 14
  decimal.getcontext().prec = genauigkeit
  zähler = 426_880 * decimal.Decimal(10_005).sqrt()
  nenner = 0
  for k in range(genauigkeit // 14):
    zähler2 = decimal.Decimal(math.factorial(6 * k) * (545140134 * k + 13591409))
    nenner2 = decimal.Decimal(math.factorial(3 * k) * math.factorial(k)**3 * (-262537412640768000)**k)
    nenner += zähler2 / nenner2
  return zähler / nenner


start = time.perf_counter()
genauigkeit = 10_000
p = str(chudnovsky(genauigkeit))
print(f'Pi ermittelt mit {genauigkeit:,} Nachkommastellen: \n{p[:genauigkeit+2]}')
print(f'Ermittelt in {time.perf_counter() - start:.4f} Sek.')
