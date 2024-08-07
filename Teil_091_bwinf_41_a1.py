import requests
import re


URL_TEXT = "https://bwinf.de/fileadmin/bundeswettbewerb/41/Alice_im_Wunderland.txt"
URL_AUFGABE = "https://bwinf.de/fileadmin/bundeswettbewerb/41/stoerung"

ALICE = requests.get(URL_TEXT).text.lower()

for i in range(6):
  lückentext = requests.get(f'{URL_AUFGABE}{i}.txt').text
  suchmuster = lückentext.replace('_', '\w+')
  print(lückentext, re.findall(suchmuster, ALICE))
