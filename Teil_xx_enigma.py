from collections import deque

rotorDict = {'I': ['EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'Q'],
             'II': ['AJDKSIRUXBLHWTMCQGZNPYFVOE', 'E'],
             'III': ['BDFHJLCPRTXVZNYEIWGAKMUSQO', 'V'],
             'IV': ['ESOVPZJAYQUIRHXLNFTGKDCMWB', 'J'],
             'V': ['VZBRGITYUPSDNHLXAWMJQOFECK', 'Z'],
             'VI': ['JPGVOUMFYQBENHZRDKASXLICTW', 'ZM'],
             'VII': ['NZJHGRCXMYSWBOUFAIVLPEKQDT', 'ZM'],
             'VIII': ['FKQHTLXOCBJSPDZRAMEWNIUYGV', 'ZM'],
             'Beta': ['LEYJVCNIXWPBQMDRTAKZGFUHOS',''],
             'Gamma': ['FSOKANUERHMBTIYCWLQPZXVGJD', '']}
reflDict = {'A': 'EJMZALYXVBWFCRQUONTSPIKHGD',
            'B': 'YRUHQSLDPXNGOKMIEBFZCWVJAT',
            'C': 'FVPJIAOYEDRZXWGCTKUQSBNMHL',
            'Thin B': 'ENKQAUYWJICOPBLMDXZVFTHRGS',
            'Thin C': 'RDOBJNTKVEHMLFCWZAXGYIPSUQ'}


def init_enigma(name_reflektor, name_walzen, name_ringpos, paare_steckerbr, name_walzenpos):
  reflektor = [ord(c)-65 for c in reflDict[name_reflektor]]
  name_walzen = name_walzen.split()
  ringpositionen = [int(x)-1 for x in name_ringpos.split()]
  paare_steckerbr = paare_steckerbr.upper().split()
  walzenpositionen = [ord(c)-65 for c in name_walzenpos.upper()]
  steckerbrett_dict = {}
  for paar in paare_steckerbr:
    steckerbrett_dict[ord(paar[0])-65] = ord(paar[1])-65
    steckerbrett_dict[ord(paar[1])-65] = ord(paar[0])-65
  return reflektor, name_walzen, ringpositionen, steckerbrett_dict, walzenpositionen


def init_walzen(name_walzen, ringpositionen, walzenpositionen):
  walzen = []
  for i, r in enumerate(name_walzen):
    walze = deque([ord(c)-65 for c in rotorDict[r][0]])
    kerbe = {ord(k)-65 for k in rotorDict[r][1]}
    walzen_pos = walzenpositionen[i]
    ring_pos = ringpositionen[i]
    walze.rotate(-walzen_pos+ring_pos)
    walzen.append([walze, kerbe, walzen_pos, ring_pos])
  return walzen

def schalte(w):
  w[0].rotate(-1)
  w[2] = (w[2]+1) % 26

def rotiere(walzen):
  #nur die rechten 3 Walzen rotieren, die 4. Walze (M4) ganz links rotiert nicht 
  rechts, mitte, links = walzen[-1:-4:-1]
  #die Doppelschritt Anomalie der mittleren Walze führt dazu, dass immer wenn sich die linke
  #Walze weiterdreht, diese die mittlere Walze um eine Position mittdreht
  if mitte[2] in mitte[1]:
    schalte(mitte)
    schalte(links)
  elif rechts[2] in rechts[1]:
    schalte(mitte)
  schalte(rechts)

def get_wi(offset):
  alpha = deque([i for i in range(26)])
  alpha.rotate(offset)
  return alpha


def encode(plaintext):
  ciphertext = ""
  for c in plaintext:
    c = ord(c)-65
    if c < 0 or c > 65: continue
    rotiere(walzen)
    if c in steckerbrett_dict:
      c = steckerbrett_dict[c]
    for wlz, _, wp, rp in reversed(walzen):
      wi = get_wi(-wp+rp)
      c = wi.index(wlz[c])
    c = reflektor[c]
    for wlz, _, wp, rp in walzen:
      wi = get_wi(-wp+rp)
      c = wlz.index(wi[c])
    if c in steckerbrett_dict:
      c = steckerbrett_dict[c]
    ciphertext += chr(c+65)
  return ciphertext


#Testfälle
reflektor, name_walzen, ringpositionen, steckerbrett_dict, walzenpositionen = init_enigma(
    "B", "II IV V", "02 21 12", "AV BS CG DL FU HZ IN KM OW RX", "BLA")
walzen = init_walzen(name_walzen, ringpositionen, walzenpositionen)
plaintext = 'EDPUD NRGYS ZRCXN UYTPO MRMBO FKTBZ REZKM LXLVE FGUEY SIOZV EQMIK UBPMM YLKLT TDEIS MDICA GYKUA CTCDO MOHWX MUUIA UBSTS LRNBZ SZWNR FXWFY SSXJZ VIJHI DISHP RKLKA YUPAD TXQSP INQMA TLPIF SVKDA SCTAC DPBOP VHJK-'
cyphertext = 'AUFKLXABTEILUNGXVONXKURTINOWAXKURTINOWAXNORDWESTLXSEBEZXSEBEZXUAFFLIEGERSTRASZERIQTUNGXDUBROWKIXDUBROWKIXOPOTSCHKAXOPOTSCHKAXUMXEINSAQTDREINULLXUHRANGETRETENXANGRIFFXINFXRGTX' 
assert encode(plaintext) == cyphertext

reflektor, name_walzen, ringpositionen, steckerbrett_dict, walzenpositionen = init_enigma(
    "B", "II IV V", "02 21 12", "AV BS CG DL FU HZ IN KM OW RX", "LSD")
walzen = init_walzen(name_walzen, ringpositionen, walzenpositionen)
plaintext = 'SFBWD NJUSE GQOBH KRTAR EEZMW KPPRB XOHDR OEQGB BGTQV PGVKB VVGBI MHUSZ YDAJQ IROAX SSSNR EHYGG RPISE ZBOVM QIEMM ZCYSG QDGRE RVBIL EKXYQ IRGIR QNRDN VRXCY YTNJR'
cyphertext = 'DREIGEHTLANGSAMABERSIQERVORWAERTSXEINSSIEBENNULLSEQSXUHRXROEMXEINSXINFRGTXDREIXAUFFLIEGERSTRASZEMITANFANGXEINSSEQSXKMXKMXOSTWXKAMENECXK' 
assert encode(plaintext) == cyphertext

reflektor, name_walzen, ringpositionen, steckerbrett_dict, walzenpositionen = init_enigma(
    "B", "III VI VIII", "01 08 13", "AN EZ HK IJ LR MQ OT PV SW UX", "UZV")
walzen = init_walzen(name_walzen, ringpositionen, walzenpositionen)
plaintext = 'YKAE NZAP MSCH ZBFO CUVM RMDP YCOF HADZ IZME FXTH FLOL PZLF GGBO TGOX GRET DWTJ IQHL MXVJ WKZU ASTR'
cyphertext = 'STEUEREJTANAFJORDJANSTANDORTQUAAACCCVIERNEUNNEUNZWOFAHRTZWONULSMXXSCHARNHORSTHCO' 
assert encode(plaintext) == cyphertext

reflektor, name_walzen, ringpositionen, steckerbrett_dict, walzenpositionen = init_enigma(
    "Thin B", "Beta II IV I", "01 01 01 22", "AT BL DF GJ HM NW OP QY RZ VX", "VJNA")
walzen = init_walzen(name_walzen, ringpositionen, walzenpositionen)
plaintext = 'NCZW VUSX PNYM INHZ XMQX SFWX WLKJ AHSH NMCO CCAK UQPM KCSM HKSE INJU SBLK IOSX CKUB HMLL XCSJ USRR DVKO HULX WCCB GVLI YXEO AHXR HKKF VDRE WEZL XOBA FGYU JQUK GRTV UKAM EURB VEKS UHHV OYHA BCJW MAKL FKLM YFVN RIZR VVRT KOFD ANJM OLBG FFLE OPRG TFLV RHOW OPBE KVWM UQFM PWPA RMFH AGKX IIBG'
cyphertext = 'VONVONJLOOKSJHFFTTTEINSEINSDREIZWOYYQNNSNEUNINHALTXXBEIANGRIFFUNTERWASSERGEDRUECKTYWABOSXLETZTERGEGNERSTANDNULACHTDREINULUHRMARQUANTONJOTANEUNACHTSEYHSDREIYZWOZWONULGRADYACHTSMYSTOSSENACHXEKNSVIERMBFAELLTYNNNNNNOOOVIERYSICHTEINSNULL' 
assert encode(plaintext) == cyphertext

reflektor, name_walzen, ringpositionen, steckerbrett_dict, walzenpositionen = \
  init_enigma("Thin B", "Beta II IV I", "01 01 01 22", "AT BL DF GJ HM NW OP QY RZ VX", "VJNA")
walzen = init_walzen(name_walzen, ringpositionen, walzenpositionen)

# Main Program Starts Here
print("  ##### Enigma Encoder #####")
print("")
plaintext = input("Enter text to encode or decode: \n").upper()
print(f'Encoded text: \n{encode(plaintext).lower()}')
