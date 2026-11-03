import yfinance as yf
import datetime as dt
import sqlite3


def db_verbinden(datei):
  db = sqlite3.connect(datei)
  cursor = db.cursor()
  sql = """create table if not exists kurse
           (id integer primary key autoincrement,
            name text not null,
            datum text not null,
            kurs float not null,
            unique(name,datum))"""
  cursor.execute(sql)
  db.commit()
  return db          


def aktuelle_kurse_einlesen():
  cursor = db.cursor()
  sql = 'insert or ignore into kurse (name, kurs, datum) values (?, ?, ?)'
  for symbol in symbole:
    daten = yf.Ticker(symbol).info
    name = daten['longName']
    kurs = daten['regularMarketPrice']
    datum = dt.datetime.fromtimestamp(daten['regularMarketTime']).isoformat()
    cursor.execute(sql,(name, kurs, datum))
  db.commit()  


symbole = 'TL0.DE AMD.DE BTC-EUR DOGE-EUR'.split()
db = db_verbinden('Teil_134_depot.db')
aktuelle_kurse_einlesen()
