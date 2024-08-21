import ttg

elemente = ["apple", "vase", "grapes", "wine", "banana", "sunflower", "pinecone", "bowl"]
bedingungen = ["vase => sunflower", 
               "grapes xor apple xor banana",
               "(wine and bowl) or (vase and bowl) and (~wine or ~vase)",
               "(apple xor vase) and (grapes xor wine) and (banana xor sunflower) and (pinecone xor bowl)"
               ]

ergebnis = ttg.Truths(elemente, bedingungen).as_pandas
ergebnis.columns = ["apple", "vase", "grapes", "wine", "banana", "sunflower", "pinecone", "bowl", "r1", "r2", "r3", "r4"]
treffer = ergebnis[(ergebnis["r1"] == 1) & (ergebnis["r2"] == 1) & (ergebnis["r3"] == 1) & (ergebnis["r4"] == 1)]
print(treffer)
