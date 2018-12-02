summe = 0

for feld in range(64):
    reiskörner = 2**feld
    summe += reiskörner
    print(f"Feld {feld+1}. = {reiskörner:>27,} Reiskörner und damit insgesamt"
          f"{summe:>28,} Reiskörner")


gewicht = summe * 0.02 / 1000 / 1000
print()
print("Wenn ein Reiskorn 0,02 Gramm wiegt, wiegen die gesamten"
      f" Reiskörner {gewicht:,.0f} Tonnen")
