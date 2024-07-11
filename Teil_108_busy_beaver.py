def busy_beaver(bibers):
  band = dict()
  pos = biber = schritte = 0

  while True:
    schritte += 1
    wert = band.get(pos, 0)
    neuer_wert, richtung, nächster_biber = bibers[biber * 2 + wert]
    band[pos] = int(neuer_wert)
    if nächster_biber == 'H': return schritte, sum(band.values())
    pos += 1 if richtung == 'R' else -1
    biber = ord(nächster_biber) - 65


regeln = ['1RH not_used',
          '1RB 1LB 1LA 1RH',
          '1RB 1RH 0RC 1RB 1LC 1LA',
          '1RB 1LB 1LA 0LC 1RH 1LD 1RD 0RA',
          '1RB 1LC 1RC 1RB 1RD 0LE 1LA 1LD 1RH 0LA']


for bibers in regeln:
  bibers = bibers.split()
  schritte, einsen = busy_beaver(bibers)
  print(f'BB({len(bibers)//2}) = {schritte:>10,} schritte mit {einsen:>5,} Einsen')
