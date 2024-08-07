# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frm_kundenauswahl.ui'
##
## Created by: Qt User Interface Compiler version 6.1.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_frm_kundenauswahl(object):
    def setupUi(self, frm_kundenauswahl):
        if not frm_kundenauswahl.objectName():
            frm_kundenauswahl.setObjectName(u"frm_kundenauswahl")
        frm_kundenauswahl.resize(578, 382)
        self.label = QLabel(frm_kundenauswahl)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 0, 581, 20))
        font = QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        self.tableView = QTableView(frm_kundenauswahl)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setGeometry(QRect(0, 60, 581, 261))
        self.bt_ok = QPushButton(frm_kundenauswahl)
        self.bt_ok.setObjectName(u"bt_ok")
        self.bt_ok.setGeometry(QRect(30, 330, 75, 24))
        self.bt_abbruch = QPushButton(frm_kundenauswahl)
        self.bt_abbruch.setObjectName(u"bt_abbruch")
        self.bt_abbruch.setGeometry(QRect(480, 340, 75, 24))

        self.retranslateUi(frm_kundenauswahl)

        QMetaObject.connectSlotsByName(frm_kundenauswahl)
    # setupUi

    def retranslateUi(self, frm_kundenauswahl):
        frm_kundenauswahl.setWindowTitle(QCoreApplication.translate("frm_kundenauswahl", u"Form", None))
        self.label.setText(QCoreApplication.translate("frm_kundenauswahl", u"Bitte Kunden ausw\u00e4hlen", None))
        self.bt_ok.setText(QCoreApplication.translate("frm_kundenauswahl", u"OK", None))
        self.bt_abbruch.setText(QCoreApplication.translate("frm_kundenauswahl", u"Abbruch", None))
    # retranslateUi

