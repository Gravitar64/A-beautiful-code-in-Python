import requests
import re

ALICE = requests.get(
    "https://bwinf.de/fileadmin/bundeswettbewerb/41/Alice_im_Wunderland.txt").text.lower()

for i in range(6):
  lückentext = requests.get(
      f"https://bwinf.de/fileadmin/bundeswettbewerb/41/stoerung{i}.txt").text
  suchmuster = lückentext.replace('_', '\w+')
  print(lückentext, re.findall(suchmuster, ALICE))
