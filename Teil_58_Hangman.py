import random as rnd

with open("Teil_58_wörter.txt") as f:
  wort = rnd.choice([w.strip().upper() for w in f])

versuche, gesucht, geraten = 8, set(c for c in wort), set()

while versuche > 0:
  text = f'Noch {versuche:>2} Versuche: '
  text += " ".join([f'{b if b in geraten else "_"}' for b in wort])
  versuch = input(text+" Ihr Buchstabe? ").upper()
  geraten.add(versuch)
  if versuch not in wort: versuche -= 1
  if gesucht.issubset(geraten): break  

print("GEWONNEN! ", end = "") if gesucht.issubset(geraten) else print("VERLOREN! ", end = "")
print(f"Das gesuchte Wort war {wort}")