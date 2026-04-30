from PySide6.QtWidgets import QDialog, QDataWidgetMapper, QMessageBox
from ui_dlg_buchung import Ui_Dlg_Buchung
from datetime import datetime
import sqlite3


class Dlg_buchung(QDialog, Ui_Dlg_Buchung):
  def __init__(self, parent, model, zeile):
    super().__init__(parent)
    self.setupUi(self)
    self.show()

    self.model = model
    self.zeile = zeile

    self.mapper = QDataWidgetMapper(self)
    self.mapper.setModel(model)
    self.mapper.setSubmitPolicy(QDataWidgetMapper.SubmitPolicy.ManualSubmit)

    self.mapper.addMapping(self.te_wohnung, 2)
    self.mapper.addMapping(self.dt_vom, 4)
    self.mapper.addMapping(self.dt_bis, 5)
    self.mapper.addMapping(self.te_tage, 6)
    self.mapper.addMapping(self.te_preis_uebern, 7)
    self.mapper.addMapping(self.te_preis_reinigung, 8)
    self.mapper.addMapping(self.te_preis_wp, 9)
    self.mapper.addMapping(self.te_anzahlung, 10)
    self.mapper.addMapping(self.te_rest, 11)
    self.mapper.addMapping(self.cb_reinigung, 12)
    self.mapper.addMapping(self.cb_betten_beziehen, 13)
    self.mapper.addMapping(self.te_anz_wp_e, 14)
    self.mapper.addMapping(self.te_anz_wp_k, 15)
    self.mapper.addMapping(self.te_anz_erwachsene, 16)
    self.mapper.addMapping(self.te_anz_kinder, 17)
    self.mapper.addMapping(self.te_anz_hunde, 18)
    self.mapper.addMapping(self.cb_Babyset, 19)
    self.mapper.addMapping(self.te_preis_gesamt, 20)
    self.mapper.addMapping(self.cb_Steuer, 24)
    self.mapper.addMapping(self.cb_Storno, 25)

    self.mapper.setCurrentIndex(zeile)

    self.buttonBox.accepted.connect(self.daten_übernehmen)
    self.dt_vom.editingFinished.connect(self.tage_berechnen)
    self.dt_bis.editingFinished.connect(self.tage_berechnen)
    self.te_preis_uebern.editingFinished.connect(self.gesamtpreis_ermitteln)
    self.te_preis_reinigung.editingFinished.connect(self.gesamtpreis_ermitteln)
    self.te_preis_wp.editingFinished.connect(self.gesamtpreis_ermitteln)
    self.te_anzahlung.editingFinished.connect(self.gesamtpreis_ermitteln)
    
    
  def daten_übernehmen(self):
    self.mapper.submit()

  def tage_berechnen(self):
    vom = datetime.strptime(self.dt_vom.text(), '%d.%m.%y')
    bis = datetime.strptime(self.dt_bis.text(), '%d.%m.%y')
    self.te_tage.setText(f'{(bis-vom).days}')
    self.doppelbelegung(vom, bis)
    self.gesamtpreis_ermitteln()

  def gesamtpreis_ermitteln(self):
    tage = int(self.te_tage.text())
    übern = float(self.te_preis_uebern.text())  
    reinigung = float(self.te_preis_reinigung.text())  
    wäsche = float(self.te_preis_wp.text())  
    anzahlung = float(self.te_anzahlung.text())

    gesamt = übern * tage + reinigung + wäsche
    self.te_preis_gesamt.setText(f'{gesamt:.2f}')
    self.te_rest.setText(f'{gesamt-anzahlung:.2f}')

  def doppelbelegung(self, vom, bis):
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    sql = f'select bu_id, vom, bis, vorname \
            from buchungen \
            inner join kunden on kunden.kd_id = buchungen.kd_id \
            where wn_id = {self.te_wohnung.text()} and storno = False'
    bid = self.model.data(self.model.index(self.zeile, 0))
    for bu_id, v, b, name in cursor.execute(sql):
      if bid == bu_id: continue
      v1 = datetime.strptime(v[:10], '%Y-%m-%d')        
      b1 = datetime.strptime(b[:10], '%Y-%m-%d')
      if vom >= b1: continue        
      if bis <= v1: continue
      QMessageBox.critical(self, 'Kritischer Fehler', f'Doppelbelegung {name}\n{v[:10]} - {b[:10]}')
      break

