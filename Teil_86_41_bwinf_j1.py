import requests, collections, itertools


def url_einlesen(url):
  datei = requests.get(url)
  return [wort.strip().lower() for wort in datei.text.split('\n')]


def gen_endung(wort):
  endungen, vokal = [], False
  for i,buchstabe in enumerate(wort):
    if buchstabe in VOKALE and not vokal:
      endungen.append(wort[i:])
      vokal = True
    elif buchstabe not in VOKALE:
      vokal = False  
  if not endungen: return None
  endung = endungen[0] if len(endungen) == 1 else endungen[-2]
  return endung if len(endung) >= len(wort)/2 else None


URL = 'https://bwinf.de/fileadmin/bundeswettbewerb/41/'
VOKALE = set('aeiouöüä')

for n in range(4):
  wörter = url_einlesen(f'{URL}reimerei{n}.txt')
  
  end2wörter = collections.defaultdict(list)
  for wort in wörter:
    endung = gen_endung(wort)
    if not endung: continue
    end2wörter[endung].append(wort)

  paare = 0
  for endung, wörter in end2wörter.items():
    for w1, w2 in itertools.combinations(wörter,2):
      if w1 in w2 or w2 in w1: continue
      print(f'{w1}/{w2}    ', end='')
      paare += 1
      
  print(f'Anz. Wortpaare = {paare}\n')

    

