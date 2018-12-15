with open ('AdventOfCode_05.txt') as f:
	aufgabe = list(f.read().strip())

besteLösung = 999999
for n in range(97,123):
	polymer = [i for i in aufgabe if i.lower() != chr(n)]
	for i in reversed(range(len(polymer)-1)):
		try:
			unit1 = polymer[i]
			unit2 = polymer[i+1]
		except IndexError:
			continue
		else:	
			if unit1 != unit2 and (unit1 == unit2.upper() or unit1.upper() == unit2):
				del polymer[i:i+2]
	besteLösung = min(besteLösung, len(polymer))
print(besteLösung)		