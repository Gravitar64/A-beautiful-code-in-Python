from dataclasses import dataclass

@dataclass
class Claim():
	spalte: int
	zeile : int
	breite: int
	höhe : int


claims=[]

spalten, zeilen = 0,0
with open('AoC_03.txt') as f:
	for zeile in f:
		wörter = zeile.split()
		x,y = wörter[2][:-1].split(',')
		x,y = int(x), int(y)
		w,h = wörter[3].split('x')
		w,h = int(w), int(h)
		spalten = max(spalten, x+w)
		zeilen = max(zeilen, y+h)
		claims.append(Claim(x,y,w,h))
			

großesTuch = [0] * spalten * zeilen

for claim in claims:
	for y in range(claim.zeile,claim.zeile+claim.höhe):
		for x in range(claim.spalte, claim.spalte+claim.breite):
			i = y * spalten + x
			großesTuch[i] += 1

for n, claim in enumerate(claims):
	gefunden = True
	for y in range(claim.zeile,claim.zeile+claim.höhe):
		for x in range(claim.spalte, claim.spalte+claim.breite):
			i = y * spalten + x
			if großesTuch[i] > 1:
				gefunden = False

	if gefunden:
		print(n+1)

		


			