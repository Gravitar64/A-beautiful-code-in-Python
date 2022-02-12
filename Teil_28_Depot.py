import pandas_datareader.data as web
import arrow
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import EMail_credentials as cred


bestand = {"AMD.DE": {"Bez": "Advanced Micro Devices, Inc.", "Anz": 3},
           "OG7T.F": {"Bez": "DEKAFONDS CF", "Anz": 1},
           "FK83.F": {"Bez": "DEKARENT-INTERNATIONAL CF", "Anz": 5},
           "UI4M.F": {"Bez": "UniFonds -net", "Anz": 3},
           "FHDD.F": {"Bez": "AMUNDI AUSTRIA STOCK A", "Anz": 10}}

start_datum = arrow.now().shift(days=-4).date()
end_datum = arrow.now().shift(days=-1).date()

yahoo_ergebnis = web.DataReader(
    list(bestand.keys()), "yahoo", start_datum, end_datum)["Adj Close"].iloc[-1]

nachricht = "AKTUELLER DEPOTWERT\n\n"
gesamt_summe = 0
for symbol, details in bestand.items():
  anz = details["Anz"]
  gesamt_summe += (summe:= yahoo_ergebnis[symbol] * anz)
  nachricht += f'{details["Bez"] + " ("+symbol+") ":<40} {yahoo_ergebnis[symbol]:>8.2f} x {anz:>5} = Summe {summe:>10,.2f}\n'
nachricht += f'{gesamt_summe:>76,.2f}\n'


msg = MIMEMultipart()
msg["From"] = cred.FROM
msg["To"] = cred.TO
msg["Subject"] = "Aktueller Depot-Wert"
msg.attach(MIMEText(nachricht, 'plain'))
server = smtplib.SMTP('smtp.web.de: 587')
server.starttls()
server.login(cred.FROM, cred.PASSWORD)
error_text = server.sendmail(cred.FROM, cred.TO, msg.as_string())
server.quit()
if not error_text:
  print(nachricht)
else:
  print(f'Probleme beim Versand ({error_text})')
print(nachricht)
