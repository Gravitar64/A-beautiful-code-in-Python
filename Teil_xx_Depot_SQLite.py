import sqlite3 as sql 
import arrow

def create_db_and_tables():
  con = sql.connect("Teil_29_depot.sql3")
  cur = con.cursor()
  assets_create_sql = """
    CREATE TABLE IF NOT EXISTS assets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol text NOT NULL,
    langname text NOT NULL,
    bestand integer NOT NULL)"""
  cur.execute(assets_create_sql)
  kurs_create_sql = """
    CREATE TABLE IF NOT EXISTS kurse (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    datum datetime NOT NULL,
    asset_id integer NOT NULL,
    kurs long,
    FOREIGN KEY (asset_id) REFERENCES assets (id))"""
  cur.execute(kurs_create_sql)
  return con,cur

def add_asset(data):
  sql = ''' INSERT INTO assets (symbol, langname, bestand)
            VALUES(?,?,?) '''
  cur.execute(sql, data)
  

def sel_assets():
  asset_ids = {}
  sql = "select * from assets"
  cur.execute(sql)
  rows = cur.fetchall()
  for row in rows:
    asset_ids[row[1]] = row[0]
  return asset_ids  

def sel_kurs():
  sql = """
    SELECT datum, langname, bestand, kurs 
    FROM kurse
    INNER JOIN assets ON assets.id = kurse.asset_id
    """
  cur.execute(sql)
  rows = cur.fetchall()
  for row in rows:
    print(row)


def add_kurs(data):
  sql = ''' INSERT INTO kurse (datum, asset_id, kurs)
              VALUES(?,?,?) '''
  cur.execute(sql, data)

con, cur = create_db_and_tables()  
asset_ids = sel_assets()
sel_kurs()


start_datum = arrow.now().shift(days=-7).date()
end_datum   = arrow.now().shift(days=-1).date()

yahoo_ergebnis = web.DataReader(
  list(asset_ids.keys()), "yahoo", start_datum, end_datum)["Adj Close"].iloc[-1]
datum_jetzt = yahoo_ergebnis.name
yahoo_ergebnis = yahoo_ergebnis.to_dict()
print(datum_jetzt, yahoo_ergebnis)



# nachricht = "AKTUELLER DEPOTWERT\n\n"
# gesamt_summe_neu, gesamt_summe_alt = 0, 0
# for symbol, kurs in yahoo_ergebnis.items():
#   bezeichnung       = bestand[symbol]['Bez']
#   anzahl            = bestand[symbol]['Anz']
#   kurs_alt          = kurs_historie[datum_vergleich][symbol]
#   summe, summe_alt  = kurs*anzahl, kurs_alt * anzahl
#   gesamt_summe_alt += summe_alt
#   gesamt_summe_neu += summe

#   nachricht += f'{bezeichnung:<40} {kurs:>8.2f} ({kurs-kurs_alt:5.2f}) x {anzahl:>3} = {kurs*anzahl:>10,.2f} ({summe-summe_alt:,.2f})\n'

# nachricht += f'{gesamt_summe_neu:>76,.2f} ({gesamt_summe_neu - gesamt_summe_alt:,.2f})\n'

# msg = MIMEText(nachricht)
# msg["From"] = cred.FROM
# msg["To"] = cred.TO
# msg["Subject"] = "Aktueller Depot-Wert"
# server = smtplib.SMTP('smtp.web.de: 587')
# server.starttls()
# server.login(cred.FROM, cred.PASSWORD)
# error_text = server.sendmail(cred.FROM, cred.TO, msg.as_string())
# server.quit()
# if not error_text:
#   print(nachricht)
# else:
#   print(f'Probleme beim Versand ({error_text})')