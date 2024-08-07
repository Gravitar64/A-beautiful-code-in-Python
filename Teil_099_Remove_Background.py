import rembg, PIL


def remove_bg(pfad, datei):
  quelle = PIL.Image.open(pfad + datei)
  ziel = rembg.remove(quelle)
  ziel.save(pfad + datei[:datei.rfind('.')] + '_bg_removed.png')

  vergleich = PIL.Image.new('RGBA', (quelle.width * 2, quelle.height))
  vergleich.paste(quelle, (0, 0))
  vergleich.paste(ziel, (quelle.width, 0))
  vergleich.show()


pfad = 'd:/Daten/grafik/affinity/'
datei = 'jinkyoung-oh-untitled-camera-9-fullquality-001.jpg'
remove_bg(pfad, datei)
