# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHeaderView, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QTableWidget,
    QTableWidgetItem, QWidget)
import logo_rc

class control_panel(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1097, 592)
        MainWindow.setMinimumSize(QSize(731, 487))
        MainWindow.setMaximumSize(QSize(1097, 999))
        MainWindow.setStyleSheet(u"background-color: rgb(149, 149, 149);\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0.858, stop:0 rgba(182, 200, 162, 255), stop:1 rgba(217, 255, 255, 255));")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 560, 51, 16))
        font = QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);")
        self.client_num = QLabel(self.centralwidget)
        self.client_num.setObjectName(u"client_num")
        self.client_num.setGeometry(QRect(60, 560, 21, 16))
        self.client_num.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);")
        self.bar = QWidget(self.centralwidget)
        self.bar.setObjectName(u"bar")
        self.bar.setGeometry(QRect(0, 0, 1101, 31))
        self.bar.setStyleSheet(u"background-color: rgb(84, 84, 84);\n"
"background-color: rgb(170, 255, 255);")
        self.exit = QPushButton(self.bar)
        self.exit.setObjectName(u"exit")
        self.exit.setGeometry(QRect(1070, 10, 15, 15))
        self.exit.setStyleSheet(u"border-radius:6px; \n"
"background-color: rgb(255, 0, 0);")
        self.label_2 = QLabel(self.bar)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(120, 10, 51, 16))
        self.label_3 = QLabel(self.bar)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(190, 30, 111, 16))
        self.IP = QLabel(self.bar)
        self.IP.setObjectName(u"IP")
        self.IP.setGeometry(QRect(160, 10, 171, 16))
        self.label_4 = QLabel(self.bar)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(560, 10, 53, 15))
        self.currenttime = QLabel(self.bar)
        self.currenttime.setObjectName(u"currenttime")
        self.currenttime.setGeometry(QRect(620, 10, 151, 16))
        self.bar_2 = QWidget(self.centralwidget)
        self.bar_2.setObjectName(u"bar_2")
        self.bar_2.setGeometry(QRect(0, 30, 1101, 41))
        self.bar_2.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);")
        self.pushButton_2 = QPushButton(self.bar_2)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(20, 10, 1061, 23))
        self.pushButton_2.setStyleSheet(u"background-color: rgb(255, 252, 164);")
        self.client_table = QTableWidget(self.centralwidget)
        if (self.client_table.columnCount() < 9):
            self.client_table.setColumnCount(9)
        __qtablewidgetitem = QTableWidgetItem()
        self.client_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.client_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.client_table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.client_table.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.client_table.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.client_table.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.client_table.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.client_table.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.client_table.setHorizontalHeaderItem(8, __qtablewidgetitem8)
        if (self.client_table.rowCount() < 12):
            self.client_table.setRowCount(12)
        self.client_table.setObjectName(u"client_table")
        self.client_table.setGeometry(QRect(10, 80, 1081, 471))
        self.client_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.client_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.client_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.client_table.setGridStyle(Qt.NoPen)
        self.client_table.setSortingEnabled(False)
        self.client_table.setRowCount(12)
        self.client_table.horizontalHeader().setCascadingSectionResizes(False)
        self.client_table.horizontalHeader().setDefaultSectionSize(121)
        self.client_table.verticalHeader().setVisible(False)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u5728\u7ebf\u6570\uff1a", None))
        self.client_num.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.exit.setText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u4f60\u7684IP:", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u4f60\u7684IP:", None))
        self.IP.setText("")
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u7576\u524d\u6642\u9593\uff1a", None))
        self.currenttime.setText("")
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"\u751f\u6210\u5ba2\u6237\u7aef", None))
        ___qtablewidgetitem = self.client_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"\u5916\u7db2IP", None));
        ___qtablewidgetitem1 = self.client_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"\u7528\u6237", None));
        ___qtablewidgetitem2 = self.client_table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"\u7cfb\u7d71", None));
        ___qtablewidgetitem3 = self.client_table.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"\u9032\u7a0b", None));
        ___qtablewidgetitem4 = self.client_table.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"\u9032\u7a0bPID", None));
        ___qtablewidgetitem5 = self.client_table.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"\u4e0a\u7dab\u6642\u9593", None));
        ___qtablewidgetitem6 = self.client_table.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"QQ\u5728\u7ebf", None));
        ___qtablewidgetitem7 = self.client_table.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"\u5fae\u4fe1\u5728\u7ebf", None));
        ___qtablewidgetitem8 = self.client_table.horizontalHeaderItem(8)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"\u4f01\u696d\u5fae\u4fe1", None));
    # retranslateUi

