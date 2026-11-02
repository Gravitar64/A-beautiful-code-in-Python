import sqlite3
import yfinance as yf
from datetime import datetime


def db_connect(db):
  conn = sqlite3.connect(db)
  cursor = conn.cursor()
  
  #Wird nur ausgeführt, wenn die Tabellen noch nicht in der Datenbank angelegt wurden
  sql = """create table if not exists kurse (
    id integer primary key autoincrement,
    name text not null,
    datum text not null,
    kurs float not null,
    unique (name,datum))"""
  cursor.execute(sql)
  conn.commit()
  return conn


def aktuelle_kurse_einlesen():
  cursor = conn.cursor()
  for name, symbol in symbole.items():
    info = yf.Ticker(symbol).info
    stand = datetime.fromtimestamp(info.get('regularMarketTime'))
    kurs = info.get('regularMarketPrice') or info.get('currentPrice')
    cursor.execute('insert or ignore into kurse (name, kurs, datum) \
                    values (?, ?, ?)', (name, kurs, stand))
  conn.commit()


symbole = {'Tesla':'Tl0.DE', 'AMD':'AMD.DE', 'UniFonds -NET-': '0P00000P06.F', 
           'DekaFonds CF':'0P00000EHB.F', 'Bitcoin':'BTC-EUR', 'Dogecoin':'DOGE-EUR'}

conn = db_connect('Teil_130_depot.db')
aktuelle_kurse_einlesen()
conn.close()