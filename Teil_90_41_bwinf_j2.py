import requests
import re


def datei_einlesen(datei):
  return re.findall('\d+',requests.get(datei).text)


URL = 'https://bwinf.de/fileadmin/bundeswettbewerb/41/'


for n in range(5):
  elemente = datei_einlesen(f'{URL}container{n}.txt')
  leichter = {elemente[i] for i in range(1,len(elemente),2)}
  schwerer = set(elemente) - leichter
  if len(schwerer) == 1:
    print(f'Container {schwerer} ist der schwerste!')
  else:
    print(f'Container {schwerer} kommen für den schwersten in Frage.')
  print()
