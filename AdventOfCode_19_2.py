lines = open("AdventOfCode_19.txt", "r").readlines()
a, b = int(lines[22].split()[2]), int(lines[24].split()[2])
n = 836 + 22 * a + b + 10550400
sqn = int(n ** .5)
print(sum(d + n // d for d in range(1, sqn + 1) if n %
          d == 0) - sqn * (sqn ** 2 == n))
