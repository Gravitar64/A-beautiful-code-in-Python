from PySide6 import QtWidgets, QtSql
from ui_main_window import Ui_MainWindow

class Frm_main(QtWidgets.QMainWindow, Ui_MainWindow):
  def __init__(self):
    super().__init__()
    self.setupUi(self)
    self.mod_kunden = QtSql.QSqlTableModel()
    self.mod_kunden.setTable('kunden')
    self.tbv_kunden.setModel(self.mod_kunden)
    self.mod_kunden.select()

    for i in range(17):
      if i in {4,5,6,8,9,13}: continue
      self.tbv_kunden.hideColumn(i)
    self.tbv_kunden.resizeColumnsToContents()

    self.mod_buchungen = QtSql.QSqlTableModel()
    self.mod_buchungen.setTable('buchungen')
    self.tbv_buchungen.setModel(self.mod_buchungen)
    self.mod_buchungen.select()

    for i in range(27):
      if i in {2,4,5,6,20}: continue
      self.tbv_buchungen.hideColumn(i)
    self.tbv_buchungen.resizeColumnsToContents()

    self.le_suche.textChanged.connect(self.suche)
    self.tbv_kunden.selectionModel().selectionChanged.connect(self.selection_kunde_changed)


  def suche(self, text):
    self.mod_kunden.setFilter(f'vorname || " " || nachname like "%{text}%"') 

  def selection_kunde_changed(self, selected, deselected):
    index = self.tbv_kunden.currentIndex()
    if index.isValid():
      kd_index = self.mod_kunden.index(index.row(), 0)
      kd_id = self.mod_kunden.data(kd_index)
      self.mod_buchungen.setFilter(f'kd_id = {kd_id}')
      #self.mod_buchungen.select()     


app = QtWidgets.QApplication()
db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
db.setDatabaseName('db.sqlite')

frm_main = Frm_main()
frm_main.show()
app.exec()
