def leseDatei(dateiname):
  with open(dateiname, encoding='utf-8') as f:
    return f.readline().split(), f.readline().split()


def findeEindeutigesWort(lücke):
  kandidaten = [w for w in wörter if len(w) == len(lücke) and
                all([a == b for a,b in zip(w, lücke) if b != '_'])]
  if len(set(kandidaten)) == 1: return kandidaten[0]              


for n in range(5):
  lücken, wörter = leseDatei(f'teil_66_raetsel{n}.txt')
  while wörter:
    for i, lücke in enumerate(lücken):
      lücke = ''.join([b for b in lücke if b.isalnum() or b == '_'])
      if (wort := findeEindeutigesWort(lücke)):
        lücken[i] = lücken[i].replace(lücke, wort)
        wörter.remove(wort)
  print(' '.join(lücken),end='\n\n')