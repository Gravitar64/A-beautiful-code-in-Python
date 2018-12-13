from collections import Counter

log = open('AoC_04.txt').read().split('\n')
log.sort()

nickerchen = []
guards = set()

v = b = False
for zeile in log:
	if '#' in zeile:
		guardID = int(zeile[26:].split()[0])
		guards.add(guardID)

	if 'asleep' in zeile:
		von = int(zeile[15:17])
		v = True
	if 'wakes' in zeile:
		bis = int(zeile[15:17])
		b = True
	if v and b:
		nickerchen.append((guardID, von, bis))
		v = b = False

bestGuard = bestMinute = bestAnzahl = 0
for guard in guards:
	summiereMinuten = Counter()
	for schlaf in nickerchen:
		if schlaf[0] == guard:
			for i in range(schlaf[1], schlaf[2]):
				summiereMinuten[i] += 1
	if summiereMinuten:
		if summiereMinuten.most_common(1)[0][1] > bestAnzahl:
			bestAnzahl = summiereMinuten.most_common(1)[0][1]
			bestMinute = summiereMinuten.most_common(1)[0][0]
			bestGuard = guard
			print(bestGuard,bestAnzahl,bestMinute)

print(bestMinute*bestGuard)
