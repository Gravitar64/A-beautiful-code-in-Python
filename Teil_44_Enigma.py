from collections import deque

def str2num(zeichenkette):
  return deque([ord(c)-65 for c in zeichenkette])

walzen_r = ['EKMFLGDQVZNTOWYHXUSPAIBRCJ',  # I 
            'AJDKSIRUXBLHWTMCQGZNPYFVOE',  # II 
            'BDFHJLCPRTXVZNYEIWGAKMUSQO',  # III 
            'ESOVPZJAYQUIRHXLNFTGKDCMWB',  # IV 
            'VZBRGITYUPSDNHLXAWMJQOFECK',  # V 
            'JPGVOUMFYQBENHZRDKASXLICTW',  # VI 
            'NZJHGRCXMYSWBOUFAIVLPEKQDT',  # VII 
            'FKQHTLXOCBJSPDZRAMEWNIUYGV']  # VIII
walzen_r = [str2num(zeile) for zeile in walzen_r]
walzen_l = deque(range(26))

UKWs = ['EJMZALYXVBWFCRQUONTSPIKHGD',  # UKW A 
        'YRUHQSLDPXNGOKMIEBFZCWVJAT',  # UKW B 
        'FVPJIAOYEDRZXWGCTKUQSBNMHL']  # UKW C 
UKWs = [str2num(zeile) for zeile in UKWs]

kerbenKat = "Q E V J Z ZM ZM ZM"
kerbenKat = [str2num(zeile) for zeile in kerbenKat.split()]

class Walze():
  def __init__(self, nr, w_pos, r_pos):
    self.w_pos = w_pos
    self.r_pos = r_pos
    self.verdr_r = walzen_r[nr-1].copy()
    self.verdr_l = walzen_l.copy()
    self.kerben = kerbenKat[nr-1]
    self.setup()

  def setup(self):
    offset = self.r_pos-self.w_pos
    self.verdr_l.rotate(offset)  
    self.verdr_r.rotate(offset)
    self.kerben = [(k-self.r_pos) % 26 for k in self.kerben]

  def show(self):
    for nr in self.verdr_l:
      print(chr(nr+65),end='')
    print()
    for nr in self.verdr_r:
      print(chr(nr+65),end='')
    print()
    for nr in self.kerben:
      print(chr(nr+65),end='')
    print()

  def click(self):
    self.verdr_l.rotate(-1)  
    self.verdr_r.rotate(-1)

  def schaltung(self):
    return self.verdr_l[0] in self.kerben    

class Enigma():
  def __init__(self):
    self.walzen = []
    self.ukw = []
    self.steckerbr = {}

  def setup(self, nr_ukw, nr_walzen, w_pos, r_pos, paare_steckerbr):
    for i, nr in enumerate(nr_walzen):
      wpos = ord(w_pos[i])-65
      rpos = r_pos[i]-1
      self.walzen.append(Walze(nr, wpos, rpos))
    self.ukw = UKWs[nr_ukw-1]
    for b1,b2 in paare_steckerbr.split():
      self.steckerbr[ord(b1)-65] = ord(b2)-65
      self.steckerbr[ord(b2)-65] = ord(b1)-65

  def rotiere(self):
    links, mitte, rechts = self.walzen
    if mitte.schaltung():
      mitte.click()
      links.click()
    elif rechts.schaltung():
      mitte.click()
    rechts.click()

def umwandeln(e, text):
  u_text = ""
  text = text.upper()
  for c in text:
    c = ord(c)-65
    if c < 0 or c> 26: continue
    e.rotiere()
    c = e.steckerbr.get(c,c)
    for w in reversed(e.walzen):
      c = w.verdr_r[c]
      c = w.verdr_l.index(c)
    c = e.ukw[c]
    for w in e.walzen:
      c = w.verdr_l[c]
      c = w.verdr_r.index(c)
    c = e.steckerbr.get(c,c)
    u_text += chr(c+65)
  return u_text

enigma = Enigma()
enigma.setup(2, [2,4,5], "BLA", [2,21,12], "AV BS CG DL FU HZ IN KM OW RX")

print('##### ENIGMA SIMULATOR #####')
text = input('Texteingabe: ')
u_text = umwandeln(enigma, text)
u_text = u_text.replace('X', ' ')
u_text = u_text.replace('Q', 'CH')
print(u_text)


