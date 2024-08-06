import decimal, time
from math import factorial as fac


def chudnovsky(genauigkeit):
  decimal.getcontext().prec = genauigkeit
  zähler = 426_880 * decimal.Decimal(10_005).sqrt()
  nenner = 0
  for k in range(genauigkeit // 14):
    zähler2 = decimal.Decimal(fac(6 * k) * (545140134 * k + 13591409))
    nenner2 = decimal.Decimal(fac(3 * k) * fac(k)**3 * (-262537412640768000)**k)
    nenner += zähler2 / nenner2
  return zähler / nenner


start = time.perf_counter()
genauigkeit = 100
print(f'Pi mit {genauigkeit:,} Stellen Genauigkeit: \n{chudnovsky(genauigkeit)}')
print(f'Ermittelt in {time.perf_counter() - start:.4f} Sek.')
