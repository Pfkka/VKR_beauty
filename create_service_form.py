# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'create_service_form.ui'
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


class Ui_Service_form(object):
    def setupUi(self, Service_form):
        if not Service_form.objectName():
            Service_form.setObjectName(u"Service_form")
        Service_form.resize(627, 322)
        self.gridLayout = QGridLayout(Service_form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(7)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.service_name_label = QLabel(Service_form)
        self.service_name_label.setObjectName(u"service_name_label")
        self.service_name_label.setMaximumSize(QSize(300, 16777215))
        font = QFont()
        font.setPointSize(10)
        self.service_name_label.setFont(font)

        self.verticalLayout_2.addWidget(self.service_name_label)

        self.service_name_lineEdit = QLineEdit(Service_form)
        self.service_name_lineEdit.setObjectName(u"service_name_lineEdit")
        self.service_name_lineEdit.setMaximumSize(QSize(200, 400))
        font1 = QFont()
        font1.setPointSize(9)
        self.service_name_lineEdit.setFont(font1)

        self.verticalLayout_2.addWidget(self.service_name_lineEdit)

        self.service_price_label = QLabel(Service_form)
        self.service_price_label.setObjectName(u"service_price_label")
        self.service_price_label.setMaximumSize(QSize(300, 16777215))
        self.service_price_label.setFont(font)

        self.verticalLayout_2.addWidget(self.service_price_label)

        self.service_price_lineEdit = QLineEdit(Service_form)
        self.service_price_lineEdit.setObjectName(u"service_price_lineEdit")
        self.service_price_lineEdit.setMaximumSize(QSize(200, 16777215))
        self.service_price_lineEdit.setFont(font1)

        self.verticalLayout_2.addWidget(self.service_price_lineEdit)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.addButton = QPushButton(Service_form)
        self.addButton.setObjectName(u"addButton")
        self.addButton.setFont(font1)

        self.verticalLayout.addWidget(self.addButton)

        self.cancelButton = QPushButton(Service_form)
        self.cancelButton.setObjectName(u"cancelButton")
        self.cancelButton.setFont(font1)

        self.verticalLayout.addWidget(self.cancelButton)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.left_table = QTableWidget(Service_form)
        self.left_table.setObjectName(u"left_table")
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.left_table.sizePolicy().hasHeightForWidth())
        self.left_table.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.left_table)

        self.right_table = QTableWidget(Service_form)
        self.right_table.setObjectName(u"right_table")
        sizePolicy.setHeightForWidth(self.right_table.sizePolicy().hasHeightForWidth())
        self.right_table.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.right_table)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)


        self.retranslateUi(Service_form)

        QMetaObject.connectSlotsByName(Service_form)
    # setupUi

    def retranslateUi(self, Service_form):
        Service_form.setWindowTitle(QCoreApplication.translate("Service_form", u"Create service", None))
        self.service_name_label.setText(QCoreApplication.translate("Service_form", u"\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0443\u0441\u043b\u0443\u0433\u0438:", None))
        self.service_price_label.setText(QCoreApplication.translate("Service_form", u"\u0426\u0435\u043d\u0430 \u0443\u0441\u043b\u0443\u0433\u0438:", None))
        self.addButton.setText(QCoreApplication.translate("Service_form", u"\u041f\u0440\u0438\u043c\u0435\u043d\u0438\u0442\u044c", None))
        self.cancelButton.setText(QCoreApplication.translate("Service_form", u"\u041e\u0442\u043c\u0435\u043d\u0430", None))
    # retranslateUi

