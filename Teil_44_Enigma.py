from collections import deque
import string

walzenDict = dict(I    = deque('EKMFLGDQVZNTOWYHXUSPAIBRCJ'),
                  II   = deque('AJDKSIRUXBLHWTMCQGZNPYFVOE'),
                  III  = deque('BDFHJLCPRTXVZNYEIWGAKMUSQO'),
                  IV   = deque('ESOVPZJAYQUIRHXLNFTGKDCMWB'),
                  V    = deque('VZBRGITYUPSDNHLXAWMJQOFECK'),
                  VI   = deque('JPGVOUMFYQBENHZRDKASXLICTW'),
                  VII  = deque('NZJHGRCXMYSWBOUFAIVLPEKQDT'),
                  VIII = deque('FKQHTLXOCBJSPDZRAMEWNIUYGV'))
walzenNamen = walzenDict.keys()

reflDict = dict(B = deque('YRUHQSLDPXNGOKMIEBFZCWVJAT'),
                A = deque('EJMZALYXVBWFCRQUONTSPIKHGD'),
                C = deque('FVPJIAOYEDRZXWGCTKUQSBNMHL'))        
reflNamen = reflDict.keys()

kerbenDict = dict(I='Q', II='E', III='V', IV='J', V='Z', VI='ZM', VII='ZM', VIII='ZM')
alphabet_num = deque(string.ascii_uppercase)          

def enigma_setup(refl, walzen, walzen_pos, ring_pos, steckerbrett):
  enigma_reflektor = reflDict[refl]
  enigma_verdr_r, enigma_verdr_l = [], []
  for name in walzen.split():
    enigma_verdr_r.append(walzenDict[name].copy())
    enigma_verdr_l.append(alphabet_num.copy())
  enigma_pos = [x for x in walzen_pos]
  enigma_ring = [int(x)-1 for x in ring_pos.split()]
  enigma_kerben = [kerbenDict[name] for name in walzen.split()]
  enigma_stecker = {}
  for paar in steckerbrett.split():
    enigma_stecker[paar[0]] = paar[1]
    enigma_stecker[paar[1]] = paar[0]
  for i in range(len(enigma_verdr_r)):
    offset = -ord(walzen_pos[i])-65+enigma_ring[i]
    enigma_verdr_r[i].rotate(offset)
    enigma_verdr_l[i].rotate(offset)
  return enigma_reflektor, enigma_verdr_r, enigma_verdr_l, enigma_pos, enigma_kerben, enigma_stecker

def click(nr,v_r, v_l, positionen):
  v_r[nr].rotate(-1)
  v_l[nr].rotate(-1)
  positionen[nr] = chr((ord(positionen[nr]) + 1) % 65)


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
    if c not in string.ascii_uppercase: continue
    rotiere(v_r, v_l, p, k)
    if c in steckbr:
      c = steckbr[ord(c)-65]
    for i in reversed(range(3)):
      c = v_r[i][ord(c)-65]
      c = chr(v_l[i].index(c)+65)
    c = refl[ord(c)-65]
    for i in range(3):
      c = v_l[i][ord(c)-65]
      c = chr(v_r[i].index(c)+65)
    if c in steckbr:
      c =steckbr[ord(c)-65]
    ciphertext += c
    if crib:
      if c != crib[n]: return ''
  return ciphertext


if __name__ == "__main__":
  refl, v_r, v_l, p, k, steckbr = enigma_setup("B", "III II I", "CAT", "01 01 01","") 
  print("  ##### Enigma Simlator #####\n")
  text = input("Texteingabe: \n")
  print(f'Umgewandelter Text: \n{encode(text, v_r, v_l, p, k, refl, steckbr)}')
