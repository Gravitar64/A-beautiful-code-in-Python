import pyodbc, sqlite3, pandas as pd, time
#64-bit Access, Treiber
# pip install pyodbc, pandas

#32-bit Access, Treiber
#Install 32-bit-Python
#pip install pyodbc, pandas==2.0.3, numpy==1.24.3

time_start = time.perf_counter()
#MS-Access (Quelle)
driver = [x for x in pyodbc.drivers() if x.startswith('Microsoft Access Driver')][0]
access_path = 'd:\\daten\\anwendungen\\access\\föhr.mdb'
ms_conn = pyodbc.connect(f'DRIVER={driver};DBQ={access_path};')
ms_cursor = ms_conn.cursor()

#SQlite (Ziel)
sq_conn = sqlite3.connect('föhr.db')
sq_cursor = sq_conn.cursor()

for tabelle in ms_cursor.tables(tableType='TABLE'):
  df = pd.read_sql_query(f'SELECT * FROM "{tabelle.table_name}"', ms_conn)
  df.to_sql(tabelle.table_name, sq_conn, if_exists='replace',index=False)
  
ms_cursor.close()
ms_conn.close()
sq_cursor.close()
sq_conn.close()

print(f'Erfolgreich ausgeführt in {time.perf_counter()-time_start:.3f} Sek.')