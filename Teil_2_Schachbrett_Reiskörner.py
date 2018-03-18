summe = 0

for feld in range(64):
    reiskörner = 2**feld
    summe += reiskörner
    print("Feld {}. = {:>27,} Reiskörner und damit insgesamt"
          "{:>28,} Reiskörner".format(feld+1, reiskörner, summe))

gewicht = summe * 0.02 / 1000 / 1000
print()
print("Wenn ein Reiskorn 0,02 Gramm wiegt, wiegen die gesamten"
      " Reiskörner {:,.0f} Tonnen".format(gewicht))
