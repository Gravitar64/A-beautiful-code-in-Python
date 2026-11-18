import yfinance as yf
import datetime as dt
import sqlite3
import itertools as itt


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
    cursor.execute(sql, (name, kurs, datum))
  db.commit()


def portfolio_bewerten():
  cursor = db.cursor()
  sql = 'select name, max(datum), kurs from kurse group by name'
  sum_invest = sum_wert = sum_gv = 0
  print(f"{'Name':<30} {'Invest':>10} {'Ant':>8} {'Kurs':>10} {'Wert':>10} {'G/V':>10} {'in %':>11}")
  print('-'*95)

  for name, datum, kurs in cursor.execute(sql).fetchall():
    anteile, invest = werte[name]
    akt_wert = kurs * anteile
    gv = akt_wert - invest
    sum_wert += akt_wert
    sum_gv += gv
    sum_invest += invest
    print(f'{name:<30} {invest:>10,.2f} {anteile:>8.2f} {kurs:>10,.2f} {akt_wert:>10,.2f} {gv:>10,.2f} {gv/invest*100:>10,.2f}%')

  print('-'*95)
  print(f'{'Summen':>30} {sum_invest:>10,.2f} {sum_wert:>30,.2f} {sum_gv:>10,.2f} {sum_gv/sum_invest*100:>10,.2f}%')
  return sum_wert


def rendite_berechnen(wert, transaktionen):
  konto = [(t[1], t[3]) for t in transaktionen]
  konto.append((dt.datetime.now().date().isoformat(), 0))
  konto.sort()

  rendite, schritt, zu_hoch, saldo = 0, 10, False, 0
  while abs(saldo-wert) > 0.01:
    saldo = saldo_ermitteln(rendite, konto)
    diff = saldo - wert
    if diff < 0 and zu_hoch or diff > 0 and not zu_hoch:
      schritt *= -0.5
      zu_hoch = not zu_hoch
    rendite += schritt
  return rendite


def saldo_ermitteln(rendite, konto):
  saldo = zinsen = 0
  for (vom, invest), (bis, _) in itt.pairwise(konto):
    saldo += invest
    if vom[:4] == bis[:4]:
      tage = tage360(vom, bis)
      zinsen += zinsen_berechnen(saldo, rendite, tage)
    else:
      jahresende = vom[:4]+'-12-30'
      tage = tage360(vom, jahresende)
      zinsen += zinsen_berechnen(saldo, rendite, tage)
      saldo += zinsen

      for jahr in range(int(vom[:4])+1, int(bis[:4])):
        saldo += zinsen_berechnen(saldo, rendite, 360)

      vorjahresende = str(jahr)+'-12-30'
      tage = tage360(vorjahresende, bis)
      zinsen = zinsen_berechnen(saldo, rendite, tage)
  return saldo + zinsen


def tage360(vom, bis):
  vj, vm, vt = map(int, vom.split('-'))
  bj, bm, bt = map(int, bis.split('-'))
  return (bj-vj)*360 + (bm-vm)*30 + min(bt, 30)-min(vt, 30)


def zinsen_berechnen(k, p, t):
  return k * p * t / 360 / 100


symbole = 'TL0.DE AMD.DE BTC-EUR DOGE-EUR'.split()
transaktionen = [('Tesla, Inc.', '2020-09-14', 10, 1080.40),
                 ('Advanced Micro Devices, Inc.', '2007-08-06', 100, 1036.95),
                 ('Bitcoin EUR', '2023-08-21', 0.045297, 1086.07801554),
                 ('Dogecoin EUR', '2021-05-10', 18011.52738, 1094.70),
                 ('Bitcoin EUR', '2026-01-06', 0.01245928, 1000)]

werte = dict()
for name, datum, anteile, invest in transaktionen:
  if name not in werte:
    werte[name] = [anteile, invest]
  else:
    werte[name][0] += anteile
    werte[name][1] += invest

db = db_verbinden('Teil_134_depot.db')
aktuelle_kurse_einlesen()
wert = portfolio_bewerten()
rendite = rendite_berechnen(wert, transaktionen)
print(
    f'Die jährliche Mindest-Rendite müsste auf einem Geldanlagekonto {rendite:,.2f}% betragen.')
