import yfinance as yf
import sqlite3
from datetime import datetime


def db_verbinden(datei):
  db = sqlite3.connect(datei)
  cursor = db.cursor()
  sql = """create table if not exists kurse 
           (id integer primary key autoincrement,
           name text not null,
           datum text not null,
           kurs float not null,
           unique (name,datum))
        """
  cursor.execute(sql)
  db.commit()
  return db


def aktuelle_kurse_einlesen():
  cursor = db.cursor()
  for symbol in symbole:
    info = yf.Ticker(symbol).info
    name = info.get('name')
    stand = datetime.fromtimestamp(info.get('regularMarketTime'))
    kurs = info.get('regularMarketPrice') or info.get('currentPrice')
    cursor.execute('insert or ignore into kurse (name, kurs, datum) \
                    values (?, ?, ?)', (name, kurs, stand))
  db.commit()


def abfrage_kurse(datum):
  cursor = db.cursor()
  cursor.execute(f'select name, kurs, max(datum) from kurse \
                   where datum <= "{datum}" \
                   group by name \
                   order by name')
  for name, kurs, datum in cursor.fetchall():
    print(f'{name:<15} {kurs:>10,.2f}€   {datum}')


symbole = 'Tl0.DE AMD.DE 0P00000P06.F 0P00000EHB.F BTC-EUR DOGE-EUR'.split()
db = db_verbinden('Teil_134_depot.db')
aktuelle_kurse_einlesen()
jetzt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
abfrage_kurse(jetzt)
db.close()
