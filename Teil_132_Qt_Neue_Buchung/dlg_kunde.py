from PySide6.QtWidgets import QDialog, QDataWidgetMapper
from ui_dlg_kunde import Ui_Dlg_Kunde


class Dlg_kunde(QDialog, Ui_Dlg_Kunde):
  def __init__(self, parent, model, zeile):
    super().__init__(parent)
    self.setupUi(self)
    self.show()

    self.model = model
    self.zeile = zeile

    self.mapper = QDataWidgetMapper(self)
    self.mapper.setModel(model)
    self.mapper.setSubmitPolicy(QDataWidgetMapper.SubmitPolicy.ManualSubmit)

    self.mapper.addMapping(self.Te_Anrede, 2)
    self.mapper.addMapping(self.Te_Titel, 3)
    self.mapper.addMapping(self.Te_Vorname, 4)
    self.mapper.addMapping(self.Te_Nachname, 5)
    self.mapper.addMapping(self.Te_Strasse, 6)
    self.mapper.addMapping(self.Te_Land, 7)
    self.mapper.addMapping(self.Te_PLZ, 8)
    self.mapper.addMapping(self.Te_Ort, 9)
    self.mapper.addMapping(self.Te_Tel, 10)
    self.mapper.addMapping(self.Te_Mobile, 11)
    self.mapper.addMapping(self.Te_EMail, 12)
    self.mapper.addMapping(self.Te_Hinweis, 13)

    self.mapper.setCurrentIndex(zeile)

    self.buttonBox.accepted.connect(self.daten_übernehmen)
    
  def daten_übernehmen(self):
    self.mapper.submit()
     


