# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_form.ui'
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


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1008, 646)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.services = QWidget()
        self.services.setObjectName(u"services")
        self.gridLayout_3 = QGridLayout(self.services)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_3 = QLabel(self.services)
        self.label_3.setObjectName(u"label_3")
        font = QFont()
        font.setPointSize(11)
        self.label_3.setFont(font)

        self.gridLayout_3.addWidget(self.label_3, 0, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.list_of_services = QTableWidget(self.services)
        self.list_of_services.setObjectName(u"list_of_services")

        self.horizontalLayout_2.addWidget(self.list_of_services)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_3)

        self.add_serviceButton = QPushButton(self.services)
        self.add_serviceButton.setObjectName(u"add_serviceButton")

        self.verticalLayout_2.addWidget(self.add_serviceButton)

        self.edit_serviceButton = QPushButton(self.services)
        self.edit_serviceButton.setObjectName(u"edit_serviceButton")

        self.verticalLayout_2.addWidget(self.edit_serviceButton)

        self.delete_serviceButton = QPushButton(self.services)
        self.delete_serviceButton.setObjectName(u"delete_serviceButton")

        self.verticalLayout_2.addWidget(self.delete_serviceButton)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_4)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)


        self.gridLayout_3.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)

        self.tabWidget.addTab(self.services, "")
        self.storage = QWidget()
        self.storage.setObjectName(u"storage")
        self.gridLayout_2 = QGridLayout(self.storage)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label = QLabel(self.storage)
        self.label.setObjectName(u"label")
        self.label.setFont(font)

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.label_2 = QLabel(self.storage)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.gridLayout_2.addWidget(self.label_2, 0, 1, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.list_of_materials = QTableWidget(self.storage)
        self.list_of_materials.setObjectName(u"list_of_materials")

        self.horizontalLayout.addWidget(self.list_of_materials)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.total_listView = QListView(self.storage)
        self.total_listView.setObjectName(u"total_listView")

        self.verticalLayout.addWidget(self.total_listView)

        self.add_materialButton = QPushButton(self.storage)
        self.add_materialButton.setObjectName(u"add_materialButton")

        self.verticalLayout.addWidget(self.add_materialButton)

        self.edit_materialButton = QPushButton(self.storage)
        self.edit_materialButton.setObjectName(u"edit_materialButton")

        self.verticalLayout.addWidget(self.edit_materialButton)

        self.delete_materialButton = QPushButton(self.storage)
        self.delete_materialButton.setObjectName(u"delete_materialButton")

        self.verticalLayout.addWidget(self.delete_materialButton)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 2)

        self.tabWidget.addTab(self.storage, "")

        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1008, 26))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MyBeauty", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043f\u0438\u0441\u043e\u043a \u0443\u0441\u043b\u0443\u0433", None))
        self.add_serviceButton.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c", None))
        self.edit_serviceButton.setText(QCoreApplication.translate("MainWindow", u"\u0418\u0437\u043c\u0435\u043d\u0438\u0442\u044c", None))
        self.delete_serviceButton.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.services), QCoreApplication.translate("MainWindow", u"\u0423\u0441\u043b\u0443\u0433\u0438", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043f\u0438\u0441\u043e\u043a \u043c\u0430\u0442\u0435\u0440\u0438\u0430\u043b\u043e\u0432", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0441\u0435\u0433\u043e:", None))
        self.add_materialButton.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c", None))
        self.edit_materialButton.setText(QCoreApplication.translate("MainWindow", u"\u0418\u0437\u043c\u0435\u043d\u0438\u0442\u044c", None))
        self.delete_materialButton.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.storage), QCoreApplication.translate("MainWindow", u"\u0421\u043a\u043b\u0430\u0434", None))
    # retranslateUi

