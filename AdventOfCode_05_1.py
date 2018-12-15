with open ('Aoc_beispiel.txt') as f:
	polymer = list(f.read().strip())

print(len(polymer))

for i in reversed(range(len(polymer)-1)):
	unit1 = polymer[i]
	unit2 = polymer[i+1]
	if unit1 != unit2 and (unit1 == unit2.upper() or unit1.upper() == unit2):
		del polymer[i:i+2]

print(len(polymer))		