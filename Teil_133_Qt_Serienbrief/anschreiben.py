import sqlite3, pandas as pd, subprocess


def anschreiben():
  conn = sqlite3.connect('db.sqlite')
  sql = """select kunden.*, buchungen.*, wohnungen.*
           from kunden
           inner join (buchungen
           inner join wohnungen on buchungen.wn_id = wohnungen.wn_id)
           on kunden.kd_id = buchungen.kd_id
           where buchungen.dat_anschreiben is null and buchungen.storno = False"""
  df = pd.read_sql_query(sql, conn)
  df.to_csv('anschreiben.csv', index=False)
  subprocess.Popen([
    'libreoffice',
    '--writer',
    '/home/andreas/Dokumente/Texte/Textverarbeitung/VORLAGEN/Qt_Teil5.ott'
  ])         
