import requests
import collections
import itertools

def gen_maßgebliche_vokalgruppe(wort):
  vokalgruppe, vokalgruppen = '', []
  for i,buchstabe in enumerate(wort):
    if buchstabe in VOKALE:
      vokalgruppe += buchstabe
    elif vokalgruppe:
      vokalgruppen.append(vokalgruppe + wort[i:])
      vokalgruppe = ''
  if vokalgruppe:
    vokalgruppen.append(vokalgruppe)
  if not vokalgruppen: return None  
  return vokalgruppen[-2] if len(vokalgruppen) > 1 else vokalgruppen[0] 


URL = 'https://bwinf.de/fileadmin/bundeswettbewerb/41/reimerei'
VOKALE = set('aeiouöüä')

for n in range(4):
  mvg2wörter = collections.defaultdict(list)
  datei = requests.get(f'{URL}{n}.txt')
  print(f'Datei Nr. {n} wurde geladen, Return-Code {datei}')
  wörter = [wort.strip().lower() for wort in datei.text.split('\n')]
  
  for wort in wörter:
    mvg = gen_maßgebliche_vokalgruppe(wort)
    if not mvg: continue
    mvg2wörter[mvg].append(wort)

  treffer = 0
  for mvg,einträge in mvg2wörter.items():
    if len(einträge) == 1: continue
    for w1,w2 in itertools.combinations(einträge,2):
      if len(w1) / 2 > len(mvg): continue
      if len(w2) / 2 > len(mvg): continue
      if w1 in w2 or w2 in w1: continue
      print(w1,w2)
      treffer += 1
  print(f'{treffer} gefundene Wortpaare')
  print()    


   

  
