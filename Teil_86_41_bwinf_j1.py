import requests, collections, itertools


def gen_endung(wort):
  endungen, vokal = [], False
  for i,buchstabe in enumerate(wort):
    if buchstabe in VOKALE and not vokal:
      endungen.append(wort[i:])
      vokal = True
    elif buchstabe not in VOKALE:
      vokal = False
  l = len(endungen)
  return endungen[-2] if l > 1 else endungen[0] if l == 1 else None 


URL = 'https://bwinf.de/fileadmin/bundeswettbewerb/41/reimerei'
VOKALE = set('aeiouöüä')

for n in range(4):
  datei = requests.get(f'{URL}{n}.txt')
  print(f'Datei Nr. {n} wurde geladen, Return-Code {datei}')
  wörter = [wort.strip().lower() for wort in datei.text.split('\n')]
  
  end2wörter = collections.defaultdict(list)
  for wort in wörter:
    if not (endung := gen_endung(wort)): continue
    end2wörter[endung].append(wort)

  treffer = 0
  for endung,wörter in end2wörter.items():
    for w1,w2 in itertools.combinations(wörter,2):
      if len(endung) < len(w1) / 2: continue
      if len(endung) < len(w2) / 2: continue
      if w1 in w2 or w2 in w1: continue
      print(w1,w2)
      treffer += 1
  print(f'Anz. Wortpaare = {treffer}')
  print()