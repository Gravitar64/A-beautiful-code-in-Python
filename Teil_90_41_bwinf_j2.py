import requests
import re

URL = "https://bwinf.de/fileadmin/bundeswettbewerb/41/"


def datei_einlesen(datei):
  return re.findall('\d+', requests.get(datei).text)


for i in range(5):
  container = datei_einlesen(f'{URL}container{i}.txt')
  leichter = {container[i] for i in range(1, len(container), 2)}
  schwerer = set(container) - leichter
  if len(schwerer) == 1:
    print(f'Container {schwerer} ist der schwerste')
  else:
    print(f'Container {schwerer} kommen für den schwersten in Frage')
