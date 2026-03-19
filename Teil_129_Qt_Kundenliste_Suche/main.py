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

    self.le_suche.textChanged.connect(self.suche)

  def suche(self, text):
    self.mod_kunden.setFilter(f'vorname || " " || nachname like "%{text}%"')    


app = QtWidgets.QApplication()
db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
db.setDatabaseName('db.sqlite')

frm_main = Frm_main()
frm_main.show()
app.exec()
