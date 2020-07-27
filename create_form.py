# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'create_form.ui'
##
## Created by: Qt User Interface Compiler version 5.14.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(454, 218)
        Form.setBaseSize(QSize(454, 218))
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.price_label = QLabel(Form)
        self.price_label.setObjectName(u"price_label")

        self.gridLayout_2.addWidget(self.price_label, 3, 0, 1, 1)

        self.volume_label = QLabel(Form)
        self.volume_label.setObjectName(u"volume_label")
        font = QFont()
        font.setPointSize(10)
        self.volume_label.setFont(font)

        self.gridLayout_2.addWidget(self.volume_label, 1, 0, 1, 1)

        self.name_lineedit = QLineEdit(Form)
        self.name_lineedit.setObjectName(u"name_lineedit")

        self.gridLayout_2.addWidget(self.name_lineedit, 0, 1, 1, 1)

        self.quantity_label = QLabel(Form)
        self.quantity_label.setObjectName(u"quantity_label")

        self.gridLayout_2.addWidget(self.quantity_label, 2, 0, 1, 1)

        self.volume_lineedit = QLineEdit(Form)
        self.volume_lineedit.setObjectName(u"volume_lineedit")

        self.gridLayout_2.addWidget(self.volume_lineedit, 1, 1, 1, 1)

        self.quantity_lineedit = QLineEdit(Form)
        self.quantity_lineedit.setObjectName(u"quantity_lineedit")

        self.gridLayout_2.addWidget(self.quantity_lineedit, 2, 1, 1, 1)

        self.name_label = QLabel(Form)
        self.name_label.setObjectName(u"name_label")
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(False)
        font1.setWeight(50)
        self.name_label.setFont(font1)
        self.name_label.setLineWidth(1)
        self.name_label.setTextFormat(Qt.MarkdownText)

        self.gridLayout_2.addWidget(self.name_label, 0, 0, 1, 1)

        self.price_lineedit = QLineEdit(Form)
        self.price_lineedit.setObjectName(u"price_lineedit")

        self.gridLayout_2.addWidget(self.price_lineedit, 3, 1, 1, 1)


        self.gridLayout.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer, 3, 0, 1, 1)

        self.applyButton = QPushButton(Form)
        self.applyButton.setObjectName(u"applyButton")
        font2 = QFont()
        font2.setPointSize(9)
        self.applyButton.setFont(font2)

        self.gridLayout.addWidget(self.applyButton, 1, 0, 1, 1)

        self.cancelButton = QPushButton(Form)
        self.cancelButton.setObjectName(u"cancelButton")
        self.cancelButton.setFont(font2)

        self.gridLayout.addWidget(self.cancelButton, 2, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u0421\u043e\u0437\u0434\u0430\u0442\u044c \u043c\u0430\u0442\u0435\u0440\u0438\u0430\u043b", None))
        self.price_label.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:10pt;\">\u0426\u0435\u043d\u0430</span></p></body></html>", None))
        self.volume_label.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:10pt;\">\u041e\u0431\u044a\u0435\u043c (\u043c\u043b, \u0448\u0442)</span></p></body></html>", None))
        self.quantity_label.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-size:10pt;\">\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e</span></p></body></html>", None))
        self.name_label.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435</p></body></html>", None))
        self.applyButton.setText(QCoreApplication.translate("Form", u"\u041f\u0440\u0438\u043c\u0435\u043d\u0438\u0442\u044c", None))
        self.cancelButton.setText(QCoreApplication.translate("Form", u"\u041e\u0442\u043c\u0435\u043d\u0430", None))
    # retranslateUi

