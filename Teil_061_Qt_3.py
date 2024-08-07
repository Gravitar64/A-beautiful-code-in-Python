from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6 import QtSql
from Teil_061_Qt.frm_main import Ui_frm_main


class Frm_main(QMainWindow, Ui_frm_main):
  def __init__(self):
    super().__init__()
    self.setupUi(self)
    mod_offene_Leistungen = QtSql.QSqlRelationalTableModel()
    mod_offene_Leistungen.setTable("Leistungen")
    mod_offene_Leistungen.setRelation(1, QtSql.QSqlRelation("Kunden", "id", "Firma"))
    self.tbl_offene_leitsungen.setItemDelegate(QtSql.QSqlRelationalDelegate())
    mod_offene_Leistungen.select()
    self.tbl_offene_leitsungen.setModel(mod_offene_Leistungen)


app = QApplication()

db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName("Teil_061_Qt/Rechnungen.sqlite")

frm_main = Frm_main()
frm_main.show()
app.exec()
