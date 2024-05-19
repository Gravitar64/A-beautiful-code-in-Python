verbindung = bezahlt = internet = online = True


def prüfe_verbindung(online, internet, bezahlt, verbindung):
  if not verbindung: return 'Keine Verbindung'
  if not bezahlt: return 'Du hast nicht bezahlt'
  if not internet: return 'Kein Internet'
  if not online: return 'Du bist offline'
  return 'Du bist online!'

  
print(prüfe_verbindung(online, internet, bezahlt, verbindung))                
