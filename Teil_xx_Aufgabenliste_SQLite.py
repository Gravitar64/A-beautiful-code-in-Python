import sqlite3 as sql 
import arrow

def create_db_and_tables():
  con = sql.connect("Teil_xx_Aufgaben.sql3")
  cur = con.cursor()
  assets_create_sql = """
    CREATE TABLE IF NOT EXISTS aufgaben (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Aufgabe text NOT NULL,
    Faellig datetime NOT NULL,
    Verantwortlich text NOT NULL,
    Status text DEFAULT 'offen')"""
  cur.execute(assets_create_sql)
  return con,cur

def add_aufgabe(data):
  sql = ''' INSERT INTO aufgaben (Aufgabe, Faellig, Verantwortlich, Status)
            VALUES(?,?,?,?) '''
  cur.execute(sql, data)
  

def sel_aufgaben(status):
  asset_ids = {}
  sql = f"select * from aufgaben WHERE Status = '{status}' ORDER BY Faellig"
  cur.execute(sql)
  rows = cur.fetchall()
  for row in rows:
    print(row)
  



con, cur = create_db_and_tables()  
add_aufgabe(('Test3','16.10.2020','Andreas','erledigt'))
add_aufgabe(('Test4','02.10.2020','Maja','erledigt'))
con.commit()
sel_aufgaben('erledigt')
con.close()



