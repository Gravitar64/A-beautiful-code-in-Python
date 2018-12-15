from collections import Counter

log = open('AoC_04.txt').read().split('\n')
log.sort()

nickerchen = []

v = b = False
for zeile in log:
	if '#' in zeile:
		guardID = int(zeile[26:].split()[0])
	if 'asleep' in zeile:
		von = int(zeile[15:17])
		v = True
	if 'wakes' in zeile:
		bis = int(zeile[15:17])
		b = True
	if v and b:
		nickerchen.append((guardID, von, bis))
		v = b = False

summiereWächter = Counter()
for schlaf in nickerchen:
	summiereWächter[schlaf[0]] += schlaf[2] - schlaf[1]
schlafmütze = summiereWächter.most_common(1)[0][0]

summiereMinuten = Counter()
for schlaf in nickerchen:
	if schlaf[0] == schlafmütze:
		for i in range(schlaf[1], schlaf[2]):
			summiereMinuten[i] += 1
sichersteMinute = summiereMinuten.most_common(1)[0][0]

print(sichersteMinute*schlafmütze)
