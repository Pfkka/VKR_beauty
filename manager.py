import json
from PySide2.QtGui import QCloseEvent
from main_form_1 import Ui_MainWindow
from create_form import Ui_Form
from create_service_form import Ui_Service_form
from PySide2.QtWidgets import QMainWindow, QWidget, QApplication, QTableWidget, QTableWidgetItem, QAbstractItemView, \
    QHeaderView
from PySide2.QtCore import Slot, QSettings, QSize, QPoint, Qt, Signal


# class Forms:
# 	def writeSettings(self):
# 		pass
#
# 	def writeSettings(self):
# 		pass


class Item:
    def __init__(self, name: str, nominal_volume: int, quantity: int, price: int):
        self.name = name.capitalize()
        self.nominal = nominal_volume
        self.quantity = quantity
        self.price = price
        self.rt = 0
        self.rate_price = 0
        self.current_volume = nominal_volume

    def one_use(self):
        if self.current_volume > self.rate:
            self.current_volume -= self.rate
        else:
            pass  # забрать со склада новую пачку - обновить объем - в случае чего изменить цену и объем пачки

    @property
    def rate(self):
        return self.rate_price

    @rate.setter
    def rate(self, rate):
        self.rt = rate
        self.rate_price = (self.rt / self.nominal) * self.price

    def __str__(self):
        return f"Name: {self.name}\n" \
               f"Volume: {self.nominal}\n" \
               f"Price: {self.price}\n" \
               f"Quantity: {self.quantity}\n"


class Storage:
    def __init__(self):
        self._boxes = dict()
        self.total_amount = 0

    def add_item(self, item: Item):
        try:
            if self._boxes[item.name][item.nominal].nominal == item.nominal:
                print("Item is exist")
        except KeyError:
            try:
                self._boxes[item.name].update({item.nominal: item})
            except KeyError:
                self._boxes[item.name] = {item.nominal: item}

    def edit_box(self, current_name: str, current_nominal_volume: int, name: str, nominal_volume: int, quantity: int,
                 price: int):
        print(current_name, current_nominal_volume)
        print(self._boxes[current_name])
        del self._boxes[current_name][current_nominal_volume]
        self.add_item(Item(name, nominal_volume, quantity, price))

    def delete_item(self, name: str, volume: int):
        try:
            del self._boxes[name][volume]
        except KeyError:
            print("Item not found")

    def sum_total_amount(self):
        self.total_amount = 0
        for nominal in self._boxes:
            for item in self._boxes[nominal]:
                self.total_amount += self._boxes[nominal][item].price * self._boxes[nominal][item].quantity

    def to_dict(self):
        dict_storage = dict()
        for item in self._boxes:
            dict_storage[item] = dict()
            for nominal_vol in self._boxes[item]:
                dict_storage[item][nominal_vol] = {"name": self._boxes[item][nominal_vol].name,
                                                   "nominal_volume": self._boxes[item][nominal_vol].nominal,
                                                   "quantity": self._boxes[item][nominal_vol].quantity,
                                                   "price": self._boxes[item][nominal_vol].price}
        return dict_storage

    def save_storage(self):
        with open("storage.json", "wt") as file:
            dict_storage = self.to_dict()
            json.dump(dict_storage, file)

    def load_storage(self):
        try:
            with open("storage.json", "rt") as file:
                data = json.load(file)
                for itm in data:
                    for nominal in data[itm]:
                        item = Item(data[itm][nominal]["name"], data[itm][nominal]["nominal_volume"],
                                    data[itm][nominal]["quantity"], data[itm][nominal]["price"])
                        self.add_item(item)
            self.sum_total_amount()
        except FileNotFoundError:
            with open("storage.json", "wt") as file:
                pass

    def __iter__(self):
        for nominal in self._boxes:
            for item in self._boxes[nominal]:
                yield self._boxes[nominal][item]

    def __getitem__(self, item):
        return self._boxes[item]

    def __str__(self):
        return f"{self._boxes}"


class Service:

    def __init__(self, name: str, service_price: int, cost_price: float):
        self.name = name
        self.service_price = service_price
        self.cost_price = cost_price  # себестоимость
        self.net_profit = service_price - cost_price
        self.service_storage = dict()

    def add_item(self, item: Item, rate):
        item.rate = rate
        self.service_storage[item.name] = item


class MainWindow(QMainWindow):
    class ServiceForm(QWidget):
        def __init__(self, storage, service, total=0):
            super().__init__()
            self.service_ui = Ui_Service_form()
            self.service_ui.setupUi(self)
            self.right_storage = storage
            self.service_storage = dict()
            self.list_of_services = service

            self.service_ui.right_table.setSortingEnabled(True)
            self.service_ui.right_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.service_ui.right_table.setColumnCount(4)
            self.service_ui.right_table.setHorizontalHeaderLabels(["Название", "Объем", "Количество", "Цена"])
            self.load_right_table()

            self.service_ui.left_table.setColumnCount(4)
            self.service_ui.left_table.setRowCount(1)
            self.service_ui.left_table.setHorizontalHeaderLabels(
                ["Название", "Объем/текущий", "Расход", "Себестоимость"])
            header = self.service_ui.right_table.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.ResizeToContents)
            header.setSectionResizeMode(0, QHeaderView.Stretch)

            header = self.service_ui.left_table.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.ResizeToContents)
            header.setSectionResizeMode(0, QHeaderView.Stretch)

            qitem = QTableWidgetItem(str(total))
            qitem.setFlags(Qt.ItemIsEnabled)
            self.service_ui.left_table.setItem(self.service_ui.left_table.rowCount() - 1, 3, qitem)

            qitem = QTableWidgetItem("Всего:")
            qitem.setFlags(Qt.ItemIsEnabled)
            self.service_ui.left_table.setItem(self.service_ui.left_table.rowCount() - 1, 2, qitem)

            self.service_ui.right_table.itemDoubleClicked.connect(self.add_item)
            self.service_ui.left_table.itemDoubleClicked.connect(self.delete_row)
            self.service_ui.left_table.itemChanged.connect(self.change_rate)

            self.service_ui.addButton.clicked.connect(self.apply)
            self.service_ui.cancelButton.clicked.connect(self.close)
            self.readSettings()

        def load_right_table(self):
            for item in self.right_storage:
                row_pos = self.service_ui.right_table.rowCount()
                self.service_ui.right_table.insertRow(row_pos)
                self.service_ui.right_table.setItem(row_pos, 0, QTableWidgetItem(item.name))
                self.service_ui.right_table.setItem(row_pos, 1, QTableWidgetItem(str(item.nominal)))
                self.service_ui.right_table.setItem(row_pos, 2, QTableWidgetItem(str(item.quantity)))
                self.service_ui.right_table.setItem(row_pos, 3, QTableWidgetItem(str(item.price)))
            self.service_ui.right_table.resizeColumnToContents(0)

        @Slot()
        def apply(self):
            service_name = self.service_ui.service_name_lineEdit.text()
            service_price = self.service_ui.service_price_lineEdit.text()
            if not service_price.isdigit():
                return
            service_price = float(service_price)

        @Slot()
        def add_item(self):
            current_name = self.service_ui.right_table.item(self.service_ui.right_table.currentRow(), 0).text()
            volume = int(self.service_ui.right_table.item(self.service_ui.right_table.currentRow(), 1).text())

            item = self.right_storage[current_name][volume]
            self.service_storage[item.name] = item

            names = {0: item.name, 1: f"{item.nominal}/{item.current_volume}", 2: item.rate, 3: item.rate_price}
            row_pos = self.service_ui.left_table.rowCount() - 1
            self.service_ui.left_table.insertRow(row_pos)
            for i in range(4):
                qitem = QTableWidgetItem(str(names[i]))
                if i != 2:
                    qitem.setFlags(Qt.ItemIsEnabled)
                self.service_ui.left_table.setItem(row_pos, i, qitem)

        @Slot()
        def delete_row(self):
            current_row = self.service_ui.left_table.currentRow()
            if self.service_ui.left_table.currentColumn() != 2 and current_row != self.service_ui.left_table.rowCount() - 1:
                self.service_ui.left_table.removeRow(current_row)

        def writeSettings(self):
            settings = QSettings()
            settings.beginGroup("ServiceForm")
            settings.setValue("size", self.size())
            settings.setValue("pos", self.pos())
            settings.endGroup()

        def readSettings(self):
            settings = QSettings()
            settings.beginGroup("ServiceForm")
            self.resize(settings.value("size", QSize(500, 500)))
            self.move(settings.value("pos", QPoint(int(QApplication.desktop().size().width() / 2),
                                                   int(QApplication.desktop().size().height() / 2))))
            settings.endGroup()

        @Slot()
        def change_rate(self, item: QTableWidgetItem):
            if item.column() == 2 and float(item.text()) != 0:
                rate = float(item.text())
                storage_item = self.service_storage[self.service_ui.left_table.item(item.row(), 0).text()]
                if storage_item.rate == rate:
                    return

                cost = self.service_ui.left_table.item(item.row(), 3)
                cost.setText(str(storage_item.rate_price))
                total = self.service_ui.left_table.item(self.service_ui.left_table.rowCount() - 1, 3)
                amount = float(total.text())
                amount -= storage_item.rate_price
                storage_item.rate = rate
                amount += storage_item.rate_price
                total.setText(str(amount))

        def closeEvent(self, event: QCloseEvent):
            self.writeSettings()
            self.close()

    class CreateForm(QWidget):

        data_changed = Signal(str, str, str, str, str, str)
        data_set = Signal(str, str, str, str)

        def __init__(self, storage: Storage, table: QTableWidget, flag=None, current_name=None, current_volume=None):
            super().__init__()
            self.ui = Ui_Form()
            self.ui.setupUi(self)
            if all([flag, current_name, current_volume]):
                self.ui.applyButton.pressed.connect(self.apply_edit)
                self.current_name = current_name
                self.current_volume = current_volume
            elif any([flag, current_name, current_volume]):
                return
            else:
                self.ui.applyButton.pressed.connect(self.apply)
            self.ui.cancelButton.clicked.connect(self.close)

            self.storage = storage
            self.table = table

            self.readSettings()

        def writeSettings(self):
            settings = QSettings()
            settings.beginGroup("CreateForm")
            settings.setValue("size", self.size())
            settings.setValue("pos", self.pos())
            settings.endGroup()

        def readSettings(self):
            settings = QSettings()
            settings.beginGroup("CreateForm")
            self.resize(settings.value("size", QSize(500, 500)))
            self.move(settings.value("pos", QPoint(int(QApplication.desktop().size().width() / 2),
                                                   int(QApplication.desktop().size().height() / 2))))
            settings.endGroup()

        def closeEvent(self, event: QCloseEvent):
            self.writeSettings()
            self.close()

        @Slot()
        def apply(self):
            name = self.ui.name_lineedit.text().capitalize()
            volume = self.ui.volume_lineedit.text()
            quantity = self.ui.quantity_lineedit.text()
            price = self.ui.price_lineedit.text()
            if not all([name, volume, quantity, price]):
                return
            self.data_set.emit(name, volume, quantity, price)
            self.ui.name_lineedit.setText("")
            self.ui.volume_lineedit.setText("")
            self.ui.quantity_lineedit.setText("")
            self.ui.price_lineedit.setText("")

        @Slot()
        def apply_edit(self):
            name = self.ui.name_lineedit.text().capitalize()
            volume = self.ui.volume_lineedit.text()
            quantity = self.ui.quantity_lineedit.text()
            price = self.ui.price_lineedit.text()

            self.data_changed.emit(self.current_name, self.current_volume, name, volume, quantity, price)

            self.close()

    def __init__(self):
        super().__init__()
        self.main_ui = Ui_MainWindow()
        self.main_ui.setupUi(self)
        self.storage = Storage()
        self.service_storage = dict()
        self.create = None
        self.service_form = None
        self.main_ui.add_materialButton.pressed.connect(self.add_material)
        self.main_ui.edit_materialButton.pressed.connect(self.edit_storage_item)
        self.main_ui.delete_materialButton.pressed.connect(self.delete_storage_item)
        self.main_ui.list_of_materials.itemDoubleClicked.connect(self.edit_storage_item)

        self.main_ui.add_serviceButton.pressed.connect(self.add_service)

        self.main_ui.list_of_materials.setSortingEnabled(True)
        self.main_ui.list_of_materials.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.main_ui.list_of_materials.setColumnCount(4)
        self.main_ui.list_of_materials.setHorizontalHeaderLabels(["Название", "Объем", "Количество", "Цена"])

        header = self.main_ui.list_of_materials.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setSectionResizeMode(0, QHeaderView.Stretch)

        self.main_ui.list_of_services.setSortingEnabled(True)
        self.main_ui.list_of_services.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.main_ui.list_of_services.setColumnCount(5)
        self.main_ui.list_of_services.setHorizontalHeaderLabels(["Название", "Цена", "Себестоимость", "+1", "-1"])
        header = self.main_ui.list_of_services.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setSectionResizeMode(0, QHeaderView.Stretch)

        self.main_ui.total_list.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.main_ui.total_list.setColumnCount(2)
        self.main_ui.total_list.setRowCount(1)
        self.main_ui.total_list.horizontalHeader().setVisible(False)
        self.main_ui.total_list.verticalHeader().setVisible(False)
        self.main_ui.total_list.setShowGrid(False)
        self.main_ui.total_list.setItem(0, 0, QTableWidgetItem("Стоимость склада:"))
        self.readSettings()

    @Slot()
    def edit_storage_row(self, current_name, current_volume, name, volume, quantity, price):
        self.storage.edit_box(current_name, int(current_volume), name, int(volume), int(quantity),
                              int(price))
        row_pos = self.main_ui.list_of_materials.currentRow()
        self.main_ui.list_of_materials.item(row_pos, 0).setText(name)
        self.main_ui.list_of_materials.item(row_pos, 1).setText(volume)
        self.main_ui.list_of_materials.item(row_pos, 2).setText(quantity)
        self.main_ui.list_of_materials.item(row_pos, 3).setText(price)
        self.total_storage_update()

    @Slot()
    def add_storage_row(self, name, volume, quantity, price):
        item = Item(name, int(volume), int(quantity), int(price))
        row_pos = self.main_ui.list_of_materials.rowCount()
        self.main_ui.list_of_materials.insertRow(row_pos)
        self.main_ui.list_of_materials.setItem(row_pos, 0, QTableWidgetItem(name))
        self.main_ui.list_of_materials.setItem(row_pos, 1, QTableWidgetItem(volume))
        self.main_ui.list_of_materials.setItem(row_pos, 2, QTableWidgetItem(quantity))
        self.main_ui.list_of_materials.setItem(row_pos, 3, QTableWidgetItem(price))
        self.storage.add_item(item)
        self.total_storage_update()

    def writeSettings(self):
        settings = QSettings()
        settings.beginGroup("MainForm")
        settings.setValue("size", self.size())
        settings.setValue("pos", self.pos())
        self.storage.save_storage()
        settings.endGroup()

    def readSettings(self):
        settings = QSettings()
        settings.beginGroup("MainForm")
        self.resize(settings.value("size", QSize(500, 500)))
        self.move(settings.value("pos", QPoint(int(QApplication.desktop().size().width() / 2),
                                               int(QApplication.desktop().size().height() / 2))))
        self.load_table()
        settings.endGroup()

    def load_table(self):
        self.storage.load_storage()
        self.main_ui.total_list.setItem(0, 1, QTableWidgetItem(f"{self.storage.total_amount} руб"))
        self.main_ui.total_list.resizeColumnsToContents()
        for item in self.storage:
            row_pos = self.main_ui.list_of_materials.rowCount()
            self.main_ui.list_of_materials.insertRow(row_pos)
            self.main_ui.list_of_materials.setItem(row_pos, 0, QTableWidgetItem(item.name))
            self.main_ui.list_of_materials.setItem(row_pos, 1, QTableWidgetItem(str(item.nominal)))
            self.main_ui.list_of_materials.setItem(row_pos, 2, QTableWidgetItem(str(item.quantity)))
            self.main_ui.list_of_materials.setItem(row_pos, 3, QTableWidgetItem(str(item.price)))
        self.main_ui.list_of_materials.resizeColumnToContents(0)

    @Slot()
    def add_service(self):
        self.service_form = self.ServiceForm(self.storage, self.main_ui.list_of_services)
        self.service_form.show()

    @Slot()
    def add_material(self):
        self.create = self.CreateForm(self.storage, self.main_ui.list_of_materials)
        self.create.data_set.connect(self.add_storage_row)
        self.create.show()

    @Slot()
    def edit_storage_item(self):
        try:
            current_name = self.main_ui.list_of_materials.item(self.main_ui.list_of_materials.currentRow(), 0).text()
            current_volume = self.main_ui.list_of_materials.item(self.main_ui.list_of_materials.currentRow(), 1).text()
            current_quantity = self.main_ui.list_of_materials.item(self.main_ui.list_of_materials.currentRow(),
                                                                   2).text()
            current_price = self.main_ui.list_of_materials.item(self.main_ui.list_of_materials.currentRow(), 3).text()
            self.create = self.CreateForm(self.storage, self.main_ui.list_of_materials, "edit", current_name,
                                          current_volume)
            self.create.data_changed.connect(self.edit_storage_row)
            self.create.ui.name_lineedit.setText(current_name)
            self.create.ui.volume_lineedit.setText(current_volume)
            self.create.ui.quantity_lineedit.setText(current_quantity)
            self.create.ui.price_lineedit.setText(current_price)
            self.create.show()
        except AttributeError:
            return

    @Slot()
    def delete_storage_item(self):
        row_now = self.main_ui.list_of_materials.currentRow()
        if row_now != -1:
            current_name = self.main_ui.list_of_materials.item(row_now, 0).text()
            current_volume = int(self.main_ui.list_of_materials.item(row_now, 1).text())
            self.main_ui.list_of_materials.removeRow(row_now)
            self.storage.delete_item(current_name, current_volume)
            self.total_storage_update()
        else:
            return

    def total_storage_update(self):
        self.storage.sum_total_amount()
        self.main_ui.total_list.item(0, 1).setText(f"{self.storage.total_amount} руб")

    def closeEvent(self, event: QCloseEvent):
        self.writeSettings()
        QApplication.quit()


if __name__ == "__main__":
    pass
# s = Storage()
# item1 = Item("Cream", 100, 5, 500)
# item2 = Item("Cream", 50, 3, 200)
# item3 = Item("Something", 150, 105, 700)
# s.add_item(item1)
# s.add_item(item2)
# s.add_item(item3)
# s.save_storage()
# s.load_storage()
# print(s._boxes)

# a = transliterate.translit("Привет", reversed=True)
# print(a)
# b = transliterate.translit(a, "ru")
# print(b)
