# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHeaderView, QLabel, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QStatusBar,
    QTabWidget, QTableView, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1082, 910)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(0, 0, 1081, 901))
        self.tb_kunden = QWidget()
        self.tb_kunden.setObjectName(u"tb_kunden")
        self.label = QLabel(self.tb_kunden)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(360, 20, 71, 31))
        font = QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.le_suche = QLineEdit(self.tb_kunden)
        self.le_suche.setObjectName(u"le_suche")
        self.le_suche.setGeometry(QRect(440, 20, 251, 41))
        self.le_suche.setFont(font)
        self.tbv_kunden = QTableView(self.tb_kunden)
        self.tbv_kunden.setObjectName(u"tbv_kunden")
        self.tbv_kunden.setGeometry(QRect(30, 80, 1071, 401))
        self.tbv_kunden.setFont(font)
        self.tbv_buchungen = QTableView(self.tb_kunden)
        self.tbv_buchungen.setObjectName(u"tbv_buchungen")
        self.tbv_buchungen.setGeometry(QRect(30, 490, 1071, 281))
        self.tbv_buchungen.setFont(font)
        self.bt_buchung_aendern = QPushButton(self.tb_kunden)
        self.bt_buchung_aendern.setObjectName(u"bt_buchung_aendern")
        self.bt_buchung_aendern.setGeometry(QRect(900, 790, 181, 61))
        font1 = QFont()
        font1.setPointSize(14)
        self.bt_buchung_aendern.setFont(font1)
        self.bt_neue_buchung = QPushButton(self.tb_kunden)
        self.bt_neue_buchung.setObjectName(u"bt_neue_buchung")
        self.bt_neue_buchung.setGeometry(QRect(730, 790, 151, 61))
        self.bt_neue_buchung.setFont(font1)
        self.bt_neuer_kunde = QPushButton(self.tb_kunden)
        self.bt_neuer_kunde.setObjectName(u"bt_neuer_kunde")
        self.bt_neuer_kunde.setGeometry(QRect(30, 790, 151, 61))
        self.bt_neuer_kunde.setFont(font1)
        self.bt_kunde_aendern = QPushButton(self.tb_kunden)
        self.bt_kunde_aendern.setObjectName(u"bt_kunde_aendern")
        self.bt_kunde_aendern.setGeometry(QRect(200, 790, 151, 61))
        self.bt_kunde_aendern.setFont(font1)
        self.tabWidget.addTab(self.tb_kunden, "")
        self.tb_anschreiben = QWidget()
        self.tb_anschreiben.setObjectName(u"tb_anschreiben")
        self.tbv_anschreiben = QTableView(self.tb_anschreiben)
        self.tbv_anschreiben.setObjectName(u"tbv_anschreiben")
        self.tbv_anschreiben.setGeometry(QRect(0, 10, 1071, 531))
        self.tbv_anschreiben.setFont(font)
        self.bt_anschreiben = QPushButton(self.tb_anschreiben)
        self.bt_anschreiben.setObjectName(u"bt_anschreiben")
        self.bt_anschreiben.setGeometry(QRect(20, 780, 151, 61))
        self.bt_anschreiben.setFont(font1)
        self.tabWidget.addTab(self.tb_anschreiben, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Buchungsverwaltung", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Suche:", None))
        self.bt_buchung_aendern.setText(QCoreApplication.translate("MainWindow", u"Buchung \u00e4ndern", None))
        self.bt_neue_buchung.setText(QCoreApplication.translate("MainWindow", u"Neue Buchung", None))
        self.bt_neuer_kunde.setText(QCoreApplication.translate("MainWindow", u"Neuer Kunde", None))
        self.bt_kunde_aendern.setText(QCoreApplication.translate("MainWindow", u"Kunde \u00e4ndern", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tb_kunden), QCoreApplication.translate("MainWindow", u"Kunden", None))
        self.bt_anschreiben.setText(QCoreApplication.translate("MainWindow", u"Anschreiben", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tb_anschreiben), QCoreApplication.translate("MainWindow", u"Anschreiben", None))
    # retranslateUi

