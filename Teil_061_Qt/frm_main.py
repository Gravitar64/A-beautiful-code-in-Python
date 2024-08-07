# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frm_main.ui'
##
## Created by: Qt User Interface Compiler version 6.1.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_frm_main(object):
    def setupUi(self, frm_main):
        if not frm_main.objectName():
            frm_main.setObjectName(u"frm_main")
        frm_main.resize(1200, 800)
        self.actionQuit = QAction(frm_main)
        self.actionQuit.setObjectName(u"actionQuit")
        self.actionKunden_verwalten = QAction(frm_main)
        self.actionKunden_verwalten.setObjectName(u"actionKunden_verwalten")
        self.actionAuftragnehmer_verwalten = QAction(frm_main)
        self.actionAuftragnehmer_verwalten.setObjectName(u"actionAuftragnehmer_verwalten")
        self.centralwidget = QWidget(frm_main)
        self.centralwidget.setObjectName(u"centralwidget")
        self.lb_offene_leistungen = QLabel(self.centralwidget)
        self.lb_offene_leistungen.setObjectName(u"lb_offene_leistungen")
        self.lb_offene_leistungen.setGeometry(QRect(0, 10, 1191, 41))
        font = QFont()
        font.setPointSize(16)
        self.lb_offene_leistungen.setFont(font)
        self.lb_offene_leistungen.setAlignment(Qt.AlignCenter)
        self.lb_offene_rechnungen = QLabel(self.centralwidget)
        self.lb_offene_rechnungen.setObjectName(u"lb_offene_rechnungen")
        self.lb_offene_rechnungen.setGeometry(QRect(0, 340, 1191, 41))
        self.lb_offene_rechnungen.setFont(font)
        self.lb_offene_rechnungen.setAlignment(Qt.AlignCenter)
        self.tbl_offene_leitsungen = QTableView(self.centralwidget)
        self.tbl_offene_leitsungen.setObjectName(u"tbl_offene_leitsungen")
        self.tbl_offene_leitsungen.setGeometry(QRect(0, 70, 1201, 251))
        self.tbl_offene_rechnungen = QTableView(self.centralwidget)
        self.tbl_offene_rechnungen.setObjectName(u"tbl_offene_rechnungen")
        self.tbl_offene_rechnungen.setGeometry(QRect(0, 400, 1201, 251))
        self.bt_leistungen_erfassen = QPushButton(self.centralwidget)
        self.bt_leistungen_erfassen.setObjectName(u"bt_leistungen_erfassen")
        self.bt_leistungen_erfassen.setGeometry(QRect(10, 680, 171, 51))
        font1 = QFont()
        font1.setPointSize(12)
        self.bt_leistungen_erfassen.setFont(font1)
        self.bt_rechnungen_erstellen = QPushButton(self.centralwidget)
        self.bt_rechnungen_erstellen.setObjectName(u"bt_rechnungen_erstellen")
        self.bt_rechnungen_erstellen.setGeometry(QRect(490, 680, 171, 51))
        self.bt_rechnungen_erstellen.setFont(font1)
        self.bt_zahlungen_erfassen = QPushButton(self.centralwidget)
        self.bt_zahlungen_erfassen.setObjectName(u"bt_zahlungen_erfassen")
        self.bt_zahlungen_erfassen.setGeometry(QRect(1020, 680, 171, 51))
        self.bt_zahlungen_erfassen.setFont(font1)
        frm_main.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(frm_main)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1200, 22))
        self.menuDatei = QMenu(self.menubar)
        self.menuDatei.setObjectName(u"menuDatei")
        self.menuStammdaten = QMenu(self.menubar)
        self.menuStammdaten.setObjectName(u"menuStammdaten")
        frm_main.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(frm_main)
        self.statusbar.setObjectName(u"statusbar")
        frm_main.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuDatei.menuAction())
        self.menubar.addAction(self.menuStammdaten.menuAction())
        self.menuDatei.addAction(self.actionQuit)
        self.menuStammdaten.addAction(self.actionKunden_verwalten)
        self.menuStammdaten.addAction(self.actionAuftragnehmer_verwalten)

        self.retranslateUi(frm_main)

        QMetaObject.connectSlotsByName(frm_main)
    # setupUi

    def retranslateUi(self, frm_main):
        frm_main.setWindowTitle(QCoreApplication.translate("frm_main", u"MainWindow", None))
        self.actionQuit.setText(QCoreApplication.translate("frm_main", u"Quit", None))
        self.actionKunden_verwalten.setText(QCoreApplication.translate("frm_main", u"Kunden verwalten", None))
        self.actionAuftragnehmer_verwalten.setText(QCoreApplication.translate("frm_main", u"Auftragnehmer verwalten", None))
        self.lb_offene_leistungen.setText(QCoreApplication.translate("frm_main", u"Offene Leistungen", None))
        self.lb_offene_rechnungen.setText(QCoreApplication.translate("frm_main", u"Offene Rechnungen", None))
        self.bt_leistungen_erfassen.setText(QCoreApplication.translate("frm_main", u"Leistungen erfassen", None))
        self.bt_rechnungen_erstellen.setText(QCoreApplication.translate("frm_main", u"Rechnungen erstellen", None))
        self.bt_zahlungen_erfassen.setText(QCoreApplication.translate("frm_main", u"Zahlungen erfassen", None))
        self.menuDatei.setTitle(QCoreApplication.translate("frm_main", u"Datei", None))
        self.menuStammdaten.setTitle(QCoreApplication.translate("frm_main", u"Stammdaten", None))
    # retranslateUi

