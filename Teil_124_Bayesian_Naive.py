#Quelle: https://www.youtube.com/watch?v=5ePw6J6FqNc
#Naive Bayes Classifier Example | Play Tennis | Outlook, Temperature, Wind 
#by Ankit Verma


def lade_daten(datei):
  with open(datei) as f:
    daten = f.read()
    daten, tests = daten.split("\n\n")
    daten = [zeile.split() for zeile in daten.split("\n")]
    tests = [zeile.split() for zeile in tests.split("\n")]
  return daten, tests


def bayesian_naive(daten, tests):
  daten = daten[1:]
  ergebnisse = [zeile[-1] for zeile in daten]
  wahrscheinlichkeiten = []
  for test in tests:
    for ergebnis in set(ergebnisse):
      anfangswahrscheinlichkeit = ergebnisse.count(ergebnis) / len(daten)  # prior
      daten_mit_ergebnis = [zeile for zeile in daten if zeile[-1] == ergebnis]
      spalten_mit_ergebnis = list(zip(*daten_mit_ergebnis))
      for spalte, test_wort in zip(spalten_mit_ergebnis, test):
        anfangswahrscheinlichkeit *= spalte.count(test_wort) / len(spalte)
      wahrscheinlichkeiten.append((anfangswahrscheinlichkeit, ergebnis))

    # Normalisieren auf 100%
    gesamt = sum(w for w, _ in wahrscheinlichkeiten)
    print(f"Bedingte naive Wahrscheinlichkeit nach Bayes für Testfall {test}")
    for w, e in wahrscheinlichkeiten:
      print(f"Ergebnis = {e} = {w:.4f} (Normalisiert = {w / gesamt * 100:.2f}%)")


daten, tests = lade_daten("Teil_124_Play_Tennis.txt")
bayesian_naive(daten, tests)
