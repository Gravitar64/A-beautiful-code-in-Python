import yfinance as yf
import datetime as dt
import sqlite3


def db_verbinden(datei):
  db = sqlite3.connect(datei)
  cursor = db.cursor()
  sqls = ["""create table if not exists kurse
             (id integer primary key autoincrement,
             name text not null,
             datum text not null,
             kurs float not null,
             unique(name,datum))""",
          """create table if not exists transaktionen
             (id integer primary key autoincrement,
             name text not null,
             datum text not null,
             anteile float not null,
             invest float not null,
             unique(name,datum))"""]
  for sql in sqls:
    cursor.execute(sql)

  for transaktion in transaktionen:
    cursor.execute(
        'insert or ignore into transaktionen (name, datum, anteile, invest) values (?, ?, ?, ?)', transaktion)

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
    cursor.execute(sql, (name, kurs, datum))
  db.commit()


def portfolio_bewerten():
  cursor = db.cursor()
  sum_invest = sum_wert = sum_gv = 0
  print(f"{'Name':<30} Ant {'Kurs':>10} {'Wert':>10} {'Invest':>10} {'G/V':>10} {'in %':>10}")
  print('-'*90)
  for name, datum, kurs in cursor.execute('select name, max(datum), kurs from kurse group by name').fetchall():
    name2, anteile, invest = cursor.execute(
        f'select name, sum(anteile), sum(invest) from transaktionen where name = "{name}" group by name')\
        .fetchone()
    gesamtwert = kurs * anteile
    gv = gesamtwert - invest
    sum_invest += invest
    sum_wert += gesamtwert
    sum_gv += gv
    print(f'{name:<30} {anteile:>3} {kurs:>10,.2f} {gesamtwert:>10,.2f} {invest:>10,.2f} {gv:>10,.2f} {gv/invest*100:>10,.2f}%')
  print('-'*90)
  print(f'{'Summen':>45} {sum_wert:>10,.2f} {sum_invest:>10,.2f} {sum_gv:>10,.2f} {sum_gv/sum_invest*100:>10,.2f}%')


symbole = 'TL0.DE AMD.DE BTC-EUR DOGE-EUR'.split()
transaktionen = [('Tesla, Inc.', '2016-01-15', 1, 12.53),
                 ('Advanced Micro Devices, Inc.', '2006-02-15', 1, 33.60),
                 ('Bitcoin EUR', '2016-05-15', 1, 404.66),
                 ('Dogecoin EUR', '2016-05-15', 1, 0.000204),
                 ('Dogecoin EUR', '2023-08-16', 1, 0.0616),
                 ]

db = db_verbinden('Teil_134_depot.db')
aktuelle_kurse_einlesen()
portfolio_bewerten()
