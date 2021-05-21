from collections import deque

walzen_r = ['EKMFLGDQVZNTOWYHXUSPAIBRCJ',  # I = 0
            'AJDKSIRUXBLHWTMCQGZNPYFVOE',  # II = 1
            'BDFHJLCPRTXVZNYEIWGAKMUSQO',  # III = 2
            'ESOVPZJAYQUIRHXLNFTGKDCMWB',  # IV = 3
            'VZBRGITYUPSDNHLXAWMJQOFECK',  # V = 4
            'JPGVOUMFYQBENHZRDKASXLICTW',  # VI = 5
            'NZJHGRCXMYSWBOUFAIVLPEKQDT',  # VII = 6
            'FKQHTLXOCBJSPDZRAMEWNIUYGV']  # VIII = 7
walzen_r = [deque([ord(x)-65 for x in zeile]) for zeile in walzen_r]
walzen_l = deque(range(26))

reflKat = ['EJMZALYXVBWFCRQUONTSPIKHGD',  # A = 0
           'YRUHQSLDPXNGOKMIEBFZCWVJAT',  # B = 1
           'FVPJIAOYEDRZXWGCTKUQSBNMHL']  # C = 2
reflKat = [[ord(x)-65 for x in zeile] for zeile in reflKat]

kerbenKat = 'Q E V J Z ZM ZM ZM'
kerbenKat = [[ord(x)-65 for x in kerben] for kerben in kerbenKat.split()]


class Enigma():
  def __init__(self):
    self.walzen = []
    self.reflektor = []
    self.steckerbr = {}

  def setup(self, nr_refl, nr_walz, nr_walzpos, nr_ringpos, paare_steckerbr):
    self.walzen = []
    for i, nr in enumerate(nr_walz):
      walz_pos = ord(nr_walzpos[i])-65
      ring_pos = nr_ringpos[i]-1
      self.walzen.append(Walze(nr, walz_pos, ring_pos))
    self.reflektor = reflKat[nr_refl]
    self.steckerbr = {}
    for paar in paare_steckerbr.upper().split():
      self.steckerbr[ord(paar[0])-65] = ord(paar[1])-65
      self.steckerbr[ord(paar[1])-65] = ord(paar[0])-65

  def rotiere(self):
    links, mitte, rechts = self.walzen[-3:]
    if mitte.schaltung():
      mitte.click()
      links.click()
    elif rechts.schaltung():
      mitte.click()
    rechts.click()


class Walze():
  def __init__(self, nr, w_pos, r_pos):
    self.walz_pos = w_pos
    self.ring_pos = r_pos
    self.verdr_r = walzen_r[nr].copy()
    self.verdr_l = walzen_l.copy()
    self.kerben = kerbenKat[nr]
    self.initialize()

  def initialize(self):
    offset = -self.walz_pos+self.ring_pos
    self.verdr_r.rotate(offset)
    self.verdr_l.rotate(offset)
    for k in self.kerben:
      k = (k + self.ring_pos) % 26

  def schaltung(self):
    return self.verdr_l[0] in self.kerben

  def click(self):
    self.verdr_r.rotate(-1)
    self.verdr_l.rotate(-1)


def encode(e, text, crib=''):
  ciphertext = ""
  text = text.upper()
  for n, c in enumerate(text):
    c = ord(c)-65
    if c < 0 or c > 65:
      continue
    e.rotiere()
    c = e.steckerbr.get(c, c)
    for w in reversed(e.walzen):
      c = w.verdr_r[c]
      c = w.verdr_l.index(c)
    c = e.reflektor[c]
    for w in e.walzen:
      c = w.verdr_l[c]
      c = w.verdr_r.index(c)
    c = e.steckerbr.get(c, c)
    if crib and chr(c+65) != crib[n]:
      return ''
    ciphertext += chr(c+65)
  return ciphertext


enigma = Enigma()
enigma.setup(1, [2,5,7], "UZV", [1,8,13], "AN EZ HK IJ LR MQ OT PV SW UX")

# Main Program Starts Here
print("  ##### Enigma Simlator #####\n")
text = input("Texteingabe: \n")
print(f'Umgewandelter Text: \n{encode(enigma, text)}')
