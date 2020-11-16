from collections import deque

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

class Enigma():
  def __init__(self):
    self.walzen = []
    self.reflektor = []
    self.reflektor_name = ""
    self.dict_steckerbr = {}
    

  def setup(self, n_refl, n_walz, n_ringpos, n_steckerbr, n_walzpos):
    self.walzen = []
    for i, name in enumerate(n_walz.upper().split()):
      verdr = walzenDict[name].copy()
      kerben = kerbenDict[name]
      walz_pos = ord(n_walzpos[i])-65
      ring_pos = int(n_ringpos.split()[i])-1
      self.walzen.append(Walze(name,verdr, kerben, walz_pos, ring_pos))
    self.reflektor = reflDict[n_refl]
    self.reflektor_name = n_refl
    self.dict_steckerbr = {}
    for paar in n_steckerbr.upper().split():
      self.dict_steckerbr[ord(paar[0])-65] = ord(paar[1])-65
      self.dict_steckerbr[ord(paar[1])-65] = ord(paar[0])-65

  def rotiere(self):
    links, mitte, rechts = self.walzen[-3:]
    if mitte.schaltung():
      mitte.click()
      links.click()
    elif rechts.schaltung():
      mitte.click()
    rechts.click()


class Walze():
  def __init__(self, name, verdr, kerb, w_pos, r_pos):
    self.name = name
    self.verdrahtung = verdr
    self.verdrahtung_i = alphabet_num.copy()
    self.kerben = kerb
    self.walz_pos = w_pos
    self.ring_pos = r_pos
    self.initialize()

  def initialize(self):
    offset = -self.walz_pos+self.ring_pos
    self.verdrahtung.rotate(offset)
    self.verdrahtung_i.rotate(offset)

  def schaltung(self):
    return self.walz_pos in self.kerben

  def click(self):
    self.verdrahtung.rotate(-1)
    self.verdrahtung_i.rotate(-1)
    self.walz_pos = (self.walz_pos + 1) % 26

def encode(e, text):
  ciphertext = ""
  text=text.upper()
  for c in text:
    kette = ''
    c = ord(c)-65
    if c < 0 or c > 65:
      continue
    e.rotiere()
    kette += chr(c+65)
    if c in e.dict_steckerbr:
      c = e.dict_steckerbr[c]
    for w in reversed(e.walzen):
      c = w.verdrahtung[c]
      kette += f' -> {chr(c+65)} wlz {w.name}({chr(w.walz_pos+65)})'
      c = w.verdrahtung_i.index(c)
    c = e.reflektor[c]
    kette += f' -> {chr(c+65)} refl {e.reflektor_name}'
    for w in e.walzen:
      c = w.verdrahtung_i[c]
      kette += f' -> {chr(c+65)} wlz {w.name}'
      c = w.verdrahtung.index(c)
    kette += ' ->'+chr(c+65)
    if c in e.dict_steckerbr:
      c = e.dict_steckerbr[c]
      kette += ' sb->'+chr(c+65)
    ciphertext += chr(c+65)
    #print(kette)    
  return ciphertext


if __name__ == "__main__":
  enigma = Enigma()
  enigma.setup("B", "III II I", "01 01 01","", "CAT")
  
    # Main Program Starts Here
  print("  ##### Enigma Simlator #####\n")
  text = input("Texteingabe: \n")
  print(f'Umgewandelter Text: \n{encode(enigma, text)}')
