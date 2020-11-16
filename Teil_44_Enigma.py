from collections import deque
from time import altzone

walzenDict = dict(I    = 'EKMFLGDQVZNTOWYHXUSPAIBRCJ',
                  II   = 'AJDKSIRUXBLHWTMCQGZNPYFVOE',
                  III  = 'BDFHJLCPRTXVZNYEIWGAKMUSQO',
                  IV   = 'ESOVPZJAYQUIRHXLNFTGKDCMWB',
                  V    = 'VZBRGITYUPSDNHLXAWMJQOFECK',
                  VI   = 'JPGVOUMFYQBENHZRDKASXLICTW',
                  VII  = 'NZJHGRCXMYSWBOUFAIVLPEKQDT',
                  VIII = 'FKQHTLXOCBJSPDZRAMEWNIUYGV')
walzenDict = {name:deque([ord(x)-65 for x in walzenDict[name]]) for name in walzenDict}
walzenNamen = walzenDict.keys()

reflDict = dict(B = 'YRUHQSLDPXNGOKMIEBFZCWVJAT',
                A = 'EJMZALYXVBWFCRQUONTSPIKHGD',
                C = 'FVPJIAOYEDRZXWGCTKUQSBNMHL')        
reflDict = {name:deque([ord(x)-65 for x in reflDict[name]]) for name in reflDict}
reflNamen = reflDict.keys()

kerbenDict = dict(I='Q', II='E', III='V', IV='J', V='Z', VI='ZM', VII='ZM', VIII='ZM')
kerbenDict = {name:{ord(x)-65 for x in kerbenDict[name]} for name in kerbenDict}

alphabet_num = deque(range(26))          

def enigma_setup(refl, walzen, walzen_pos, ring_pos, steckerbrett):
  enigma_reflektor = reflDict[refl]
  enigma_verdr_r, enigma_verdr_l = [], []
  for name in walzen.split():
    enigma_verdr_r.append(walzenDict[name].copy())
    enigma_verdr_l.append(alphabet_num.copy())
  enigma_pos = [ord(x)-65 for x in walzen_pos]
  enigma_ring = [int(x)-1 for x in ring_pos.split()]
  enigma_kerben = [kerbenDict[name] for name in walzen.split()]
  enigma_stecker = {}
  for paar in steckerbrett.split():
    enigma_stecker[ord(paar[0])-65] = ord(paar[1]-65)
    enigma_stecker[ord(paar[1])-65] = ord(paar[0]-65)
  for i in range(len(enigma_verdr_r)):
    offset = -enigma_pos[i]+enigma_ring[i]
    enigma_verdr_r[i].rotate(offset)
    enigma_verdr_l[i].rotate(offset)
  return enigma_reflektor, enigma_verdr_r, enigma_verdr_l, enigma_pos, enigma_kerben, enigma_stecker

def click(nr,v_r, v_l, positionen):
  v_r[nr].rotate(-1)
  v_l[nr].rotate(-1)
  positionen[nr] = (positionen[nr] + 1) % 26


def rotiere(v_r, v_l, positionen, kerben):
  if positionen[1] == kerben[1]:
    click(1, v_r, v_l, positionen)
    click(0, v_r, v_l, positionen)
  elif positionen[2] == kerben[2]:
    click(1, v_r, v_l, positionen)
  click(2, v_r, v_l, positionen)


def encode(text, v_r, v_l, p, k, refl, steckbr, crib=''):
  ciphertext = ""
  text=text.upper()
  for n,c in enumerate(text):
    c = ord(c)-65
    if c < 0 or c > 65: continue
    rotiere(v_r, v_l, p, k)
    if c in steckbr:
      c = steckbr[c]
    for i in reversed(range(3)):
      c = v_r[i][c]
      c = v_l[i].index(c)
    c = refl[c]
    for i in range(3):
      c = v_l[i][c]
      c = v_r[i].index(c)
    if c in steckbr:
      c =steckbr[c]
    ciphertext += chr(c+65)
    if crib:
      if chr(c+65) != crib[n]: return ''
  return ciphertext


if __name__ == "__main__":
  refl, v_r, v_l, p, k, steckbr = enigma_setup("B", "III II I", "CAT", "01 01 01","") 
  print("  ##### Enigma Simlator #####\n")
  text = input("Texteingabe: \n")
  print(f'Umgewandelter Text: \n{encode(text, v_r, v_l, p, k, refl, steckbr)}')
