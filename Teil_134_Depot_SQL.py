import yfinance as yf
import sqlite3
from datetime import datetime


def db_connect(db):
  conn = sqlite3.connect(db)
  cursor = conn.cursor()
  sql = """create table if not exists kurse 
           (id integer primary key autoincrement,
           name text not null,
           datum text not null,
           kurs float not null,
           unique (name,datum))
        """
  cursor.execute(sql)
  conn.commit()
  return conn


def aktuelle_kurse_einlesen():
  cursor = conn.cursor()
  for symbol in symbole:
    info = yf.Ticker(symbol).info
    name = info.get('name')
    stand = datetime.fromtimestamp(info.get('regularMarketTime'))
    kurs = info.get('regularMarketPrice') or info.get('currentPrice')
    cursor.execute('insert or ignore into kurse (name, kurs, datum) \
                    values (?, ?, ?)', (name, kurs, stand))
  conn.commit()


def abfrage_kurse(datum):
  cursor = conn.cursor()
  datum += ' 23:59:59'
  cursor.execute(f'select name, kurs, max(datum) from kurse \
                   where datum <= "{datum}" \
                   group by name \
                   order by name')
  for name, kurs, datum in cursor.fetchall():
    print(f'{name:<15} {kurs:>10,.2f}€   {datum}')                 


symbole = 'Tl0.DE AMD.DE 0P00000P06.F 0P00000EHB.F BTC-EUR DOGE-EUR'.split()

conn = db_connect('Teil_130_depot.db')
aktuelle_kurse_einlesen()
abfrage_kurse('2026-11-02')
conn.close()