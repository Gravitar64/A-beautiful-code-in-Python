# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
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
    QTableView, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1082, 910)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.le_suche = QLineEdit(self.centralwidget)
        self.le_suche.setObjectName(u"le_suche")
        self.le_suche.setGeometry(QRect(410, 20, 251, 41))
        font = QFont()
        font.setPointSize(16)
        self.le_suche.setFont(font)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(330, 20, 71, 31))
        self.label.setFont(font)
        self.tbv_kunden = QTableView(self.centralwidget)
        self.tbv_kunden.setObjectName(u"tbv_kunden")
        self.tbv_kunden.setGeometry(QRect(10, 110, 1071, 401))
        self.tbv_kunden.setFont(font)
        self.tbv_buchungen = QTableView(self.centralwidget)
        self.tbv_buchungen.setObjectName(u"tbv_buchungen")
        self.tbv_buchungen.setGeometry(QRect(10, 520, 1071, 281))
        self.tbv_buchungen.setFont(font)
        self.bt_neuer_kunde = QPushButton(self.centralwidget)
        self.bt_neuer_kunde.setObjectName(u"bt_neuer_kunde")
        self.bt_neuer_kunde.setGeometry(QRect(10, 810, 151, 61))
        font1 = QFont()
        font1.setPointSize(14)
        self.bt_neuer_kunde.setFont(font1)
        self.bt_kunde_aendern = QPushButton(self.centralwidget)
        self.bt_kunde_aendern.setObjectName(u"bt_kunde_aendern")
        self.bt_kunde_aendern.setGeometry(QRect(180, 810, 151, 61))
        self.bt_kunde_aendern.setFont(font1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Buchungsverwaltung", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Suche:", None))
        self.bt_neuer_kunde.setText(QCoreApplication.translate("MainWindow", u"Neuer Kunde", None))
        self.bt_kunde_aendern.setText(QCoreApplication.translate("MainWindow", u"Kunde \u00e4ndern", None))
    # retranslateUi

