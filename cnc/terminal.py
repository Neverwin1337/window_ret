# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'V_terminal.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QPlainTextEdit,
    QPushButton, QSizePolicy, QWidget)

class V_terminal(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(853, 487)
        Form.setMinimumSize(QSize(796, 359))
        Form.setMaximumSize(QSize(861, 496))
        Form.setStyleSheet(u"")
        self.command = QLineEdit(Form)
        self.command.setObjectName(u"command")
        self.command.setGeometry(QRect(10, 440, 761, 41))
        font = QFont()
        font.setFamilies([u"Cascadia Mono Light"])
        font.setPointSize(11)
        self.command.setFont(font)
        self.send = QPushButton(Form)
        self.send.setObjectName(u"send")
        self.send.setGeometry(QRect(780, 440, 71, 41))
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 0, 851, 21))
        font1 = QFont()
        font1.setPointSize(11)
        self.label.setFont(font1)
        self.label.setLayoutDirection(Qt.LeftToRight)
        self.label.setAlignment(Qt.AlignCenter)
        self.result = QPlainTextEdit(Form)
        self.result.setObjectName(u"result")
        self.result.setGeometry(QRect(10, 30, 831, 401))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.command.setText("")
        self.send.setText(QCoreApplication.translate("Form", u"\u53d1\u9001", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u865a\u62df\u7ec8\u7aef", None))
    # retranslateUi

