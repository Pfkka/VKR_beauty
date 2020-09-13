import json
from copy import copy
from PySide2.QtGui import QCloseEvent
from main_form_1 import Ui_MainWindow
from create_form import Ui_Form
from create_service_form import Ui_Service_form
from PySide2.QtWidgets import QMainWindow, QWidget, QApplication, QTableWidget, QTableWidgetItem, QAbstractItemView, \
    QHeaderView, QPushButton, QMessageBox
from PySide2.QtCore import Slot, QSettings, QSize, QPoint, Qt, Signal


class Item:
    def __init__(self, name: str, nominal_volume: int, quantity: int, price: int, rate=0, rate_price=None,
                 current_volume=None):
        self.name = name.capitalize()
        self.nominal = nominal_volume
        self.quantity = quantity
        self.price = price
        self.rt = rate
        self.rate_price = rate_price if rate_price is not None else 0
        self.current_volume = nominal_volume if not current_volume else current_volume

    def one_use(self, flag: bool, storage):
        if self.quantity != storage[self.name][self.nominal].quantity:
            self.quantity = storage[self.name][self.nominal].quantity
        if flag:
            if self.current_volume > self.rate:
                self.current_volume -= self.rate
            else:
                rng = self.current_volume - self.rate
                if self.quantity > 1:
                    self.current_volume = self.nominal + rng  # rng < 0
                    self.quantity -= 1
                    storage[self.name][self.nominal].quantity -= 1
                else:
                    return self.name
        else:
            if self.rate + self.current_volume <= self.nominal:
                self.current_volume += self.rate
            else:
                rng = self.rate + self.current_volume - self.nominal  # rng >0
                self.current_volume = rng
                self.quantity += 1
                storage[self.name][self.nominal].quantity += 1

    @property
    def rate(self):
        return self.rt

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
                return item.name
        except KeyError:
            try:
                self._boxes[item.name].update({item.nominal: item})
            except KeyError:
                self._boxes[item.name] = {item.nominal: item}

    def edit_box(self, current_name: str, current_nominal_volume: int, name: str, nominal_volume: int, quantity: int,
                 price: int):
        del self._boxes[current_name][current_nominal_volume]
        is_exist = self.add_item(Item(name, nominal_volume, quantity, price))
        return is_exist

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
        self.plus_button = QPushButton("Plus")
        self.minus_button = QPushButton("Minus")
        self.used_times = 0

    def add_item(self, item: Item):
        self.service_storage[item.name] = copy(item)
        # item = self.service_storage[item.name]
        # if item.quantity == 0:
        #     print(f"{item.name} is empty !!!")

    def use(self, flag: bool, storage):
        empty_items = []
        for item in self.service_storage:
            empty_item = self.service_storage[item].one_use(flag, storage)
            if isinstance(empty_item, str):
                empty_items.append(empty_item)
        self.used_times += 1 if flag else (-1)
        return empty_items

    def service_to_dict(self):
        dict_sevice = dict()
        dict_sevice["cost_price"] = self.cost_price
        dict_sevice["service_price"] = self.service_price
        dict_sevice["service_use"] = self.used_times
        dict_sevice["items"] = dict()
        for item in self.service_storage:
            dict_sevice["items"][item] = {"name": self.service_storage[item].name,
                                          "nominal_volume": self.service_storage[item].nominal,
                                          "quantity": self.service_storage[item].quantity,
                                          "price": self.service_storage[item].price,
                                          "rate": self.service_storage[item].rate,
                                          "rate_price": self.service_storage[item].rate_price,
                                          "current_volume": self.service_storage[item].current_volume}
        return dict_sevice


class MainWindow(QMainWindow):
    class ServiceForm(QWidget):
        data_set = Signal(str, float, dict, float)
        data_change = Signal(str, float, dict, float, int)

        def __init__(self, storage, service_list, service: Service = None, current_row=None, total=0):
            super().__init__()
            self.service_ui = Ui_Service_form()
            self.service_ui.setupUi(self)
            self.right_storage = storage
            self.list_of_services = service_list
            self.current_row = current_row

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
            if service is not None:
                self.service_storage = service.service_storage
                self.service_ui.service_name_lineEdit.setText(service.name)
                self.service_ui.service_price_lineEdit.setText(str(int(service.service_price)))
                for item in self.service_storage:
                    self.add_item(item=self.service_storage[item])
                self.set_total()
            else:
                self.service_storage = dict()
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
            service_name = self.service_ui.service_name_lineEdit.text().capitalize()
            service_price = self.service_ui.service_price_lineEdit.text()
            if not service_price.isdigit():
                return
            service_price = float(service_price)
            cost_price = float(self.service_ui.left_table.item(self.service_ui.left_table.rowCount() - 1, 3).text())
            if self.current_row is not None:
                self.data_change.emit(service_name, service_price, self.service_storage, cost_price, self.current_row)
            else:
                self.data_set.emit(service_name, service_price, self.service_storage, cost_price)
            self.close()

        @Slot()
        def add_item(self, q=None, item=None):
            if item is None:
                current_name = self.service_ui.right_table.item(self.service_ui.right_table.currentRow(), 0).text()
                volume = int(self.service_ui.right_table.item(self.service_ui.right_table.currentRow(), 1).text())

                item = self.right_storage[current_name][volume]
                if item.name in self.service_storage:
                    return
                self.service_storage[item.name] = item
            names = {0: item.name, 1: f"{item.nominal}/{item.current_volume}", 2: item.rate, 3: item.rate_price}
            row_pos = self.service_ui.left_table.rowCount() - 1
            self.service_ui.left_table.insertRow(row_pos)
            for i in range(4):
                qitem = QTableWidgetItem(str(names[i]))
                if i != 2:
                    qitem.setFlags(Qt.ItemIsEnabled)
                self.service_ui.left_table.setItem(row_pos, i, qitem)
            total = self.service_ui.left_table.item(self.service_ui.left_table.rowCount() - 1, 3)
            amount = float(total.text())
            amount += item.rate_price
            total.setText(str(int(amount)))

        @Slot()
        def delete_row(self):
            current_row = self.service_ui.left_table.currentRow()
            if self.service_ui.left_table.currentColumn() != 2 and current_row != self.service_ui.left_table.rowCount() - 1:
                item = self.service_storage[self.service_ui.left_table.item(current_row, 0).text()]
                total = self.service_ui.left_table.item(self.service_ui.left_table.rowCount() - 1, 3)
                amount = float(total.text())
                amount -= item.rate_price
                total.setText(str(amount))
                del self.service_storage[self.service_ui.left_table.item(current_row, 0).text()]
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

                total = self.service_ui.left_table.item(self.service_ui.left_table.rowCount() - 1, 3)
                amount = float(total.text())
                amount -= storage_item.rate_price
                storage_item.rate = rate
                cost = self.service_ui.left_table.item(item.row(), 3)
                cost.setText(str(storage_item.rate_price))
                amount += storage_item.rate_price
                total.setText(str(amount))

        def set_total(self):
            total = 0
            for item in self.service_storage:
                total += self.service_storage[item].rate_price
            qitem = self.service_ui.left_table.item(self.service_ui.left_table.rowCount() - 1, 3)
            qitem.setText(f"{total}")

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
        self.services = dict()
        self.create = None
        self.service_form = None
        self.main_ui.add_materialButton.pressed.connect(self.add_material)
        self.main_ui.edit_materialButton.pressed.connect(self.edit_storage_item)
        self.main_ui.delete_materialButton.pressed.connect(self.delete_storage_item)
        self.main_ui.list_of_materials.itemDoubleClicked.connect(self.edit_storage_item)
        self.main_ui.delete_serviceButton.pressed.connect(self.delete_service)
        self.main_ui.add_serviceButton.pressed.connect(self.add_service)
        self.main_ui.edit_serviceButton.pressed.connect(self.edit_service)
        self.main_ui.list_of_services.itemDoubleClicked.connect(self.edit_service)

        self.main_ui.list_of_materials.setSortingEnabled(True)
        self.main_ui.list_of_materials.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.main_ui.list_of_materials.setColumnCount(4)
        self.main_ui.list_of_materials.setHorizontalHeaderLabels(["Название", "Объем", "Количество", "Цена"])

        header = self.main_ui.list_of_materials.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setSectionResizeMode(0, QHeaderView.Stretch)

        self.main_ui.list_of_services.setSortingEnabled(True)
        self.main_ui.list_of_services.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.main_ui.list_of_services.setColumnCount(6)
        self.main_ui.list_of_services.setHorizontalHeaderLabels(["Название", "Цена", "Себестоимость", "+1", "-1",
                                                                 "Сделано раз"])
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
    def plus(self):
        service_table = self.main_ui.list_of_services
        current_row = service_table.currentRow()
        service = self.services[service_table.item(current_row, 0).text()]
        empty = service.use(True, self.storage)
        if empty:
            self.msg(empty)
            return
        item = self.main_ui.list_of_services.item(current_row, 5)
        item.setText(f"{service.used_times}")
        self.update_list_storage()

    @Slot()
    def minus(self):
        service_table = self.main_ui.list_of_services
        current_row = service_table.currentRow()
        service = self.services[service_table.item(current_row, 0).text()]
        service.use(False, self.storage)
        self.main_ui.list_of_services.item(current_row, 5).setText(f"{service.used_times}")
        self.update_list_storage()

    @Slot()
    def edit_storage_row(self, current_name, current_volume, name, volume, quantity, price):
        is_exist = self.storage.edit_box(current_name, int(current_volume), name, int(volume), int(quantity),
                                         int(price))
        if isinstance(is_exist, str):
            self.msg(is_exist)
            return
        row_pos = self.main_ui.list_of_materials.currentRow()
        self.main_ui.list_of_materials.item(row_pos, 0).setText(name)
        self.main_ui.list_of_materials.item(row_pos, 1).setText(volume)
        self.main_ui.list_of_materials.item(row_pos, 2).setText(quantity)
        self.main_ui.list_of_materials.item(row_pos, 3).setText(price)
        self.total_storage_update()

    @Slot()
    def add_storage_row(self, name, volume, quantity, price):
        item = Item(name, int(volume), int(quantity), int(price))
        is_exist = self.storage.add_item(item)
        if isinstance(is_exist, str):
            self.msg(is_exist)
            return
        row_pos = self.main_ui.list_of_materials.rowCount()
        self.main_ui.list_of_materials.insertRow(row_pos)
        self.main_ui.list_of_materials.setItem(row_pos, 0, QTableWidgetItem(name))
        self.main_ui.list_of_materials.setItem(row_pos, 1, QTableWidgetItem(volume))
        self.main_ui.list_of_materials.setItem(row_pos, 2, QTableWidgetItem(quantity))
        self.main_ui.list_of_materials.setItem(row_pos, 3, QTableWidgetItem(price))
        self.total_storage_update()

    def writeSettings(self):
        settings = QSettings()
        settings.beginGroup("MainForm")
        settings.setValue("size", self.size())
        settings.setValue("pos", self.pos())
        self.storage.save_storage()
        self.save_services()
        settings.endGroup()

    def readSettings(self):
        settings = QSettings()
        settings.beginGroup("MainForm")
        self.resize(settings.value("size", QSize(500, 500)))
        self.move(settings.value("pos", QPoint(int(QApplication.desktop().size().width() / 2),
                                               int(QApplication.desktop().size().height() / 2))))
        self.load_table()
        self.load_services()
        settings.endGroup()

    def load_table(self):
        self.storage.load_storage()
        self.main_ui.total_list.setItem(0, 1, QTableWidgetItem(f"{self.storage.total_amount} руб"))
        self.main_ui.total_list.resizeColumnsToContents()
        table = self.main_ui.list_of_materials
        for item in self.storage:
            row_pos = table.rowCount()
            table.insertRow(row_pos)
            table.setItem(row_pos, 0, QTableWidgetItem(item.name))
            table.setItem(row_pos, 1, QTableWidgetItem(str(item.nominal)))
            table.setItem(row_pos, 2, QTableWidgetItem(str(item.quantity)))
            table.setItem(row_pos, 3, QTableWidgetItem(str(item.price)))
        table.resizeColumnToContents(0)

    def save_services(self):
        with open("services.json", "wt") as file:
            services_dct = dict()
            for service in self.services:
                services_dct[service] = self.services[service].service_to_dict()
            json.dump(services_dct, file)

    def load_services(self):
        try:
            with open("services.json", "rt") as file:
                data = json.load(file)
                for service in data:
                    service_name = service
                    service_price = data[service]["service_price"]
                    service_cost_price = data[service]["cost_price"]
                    service_used_times = data[service]["service_use"]
                    items = dict()
                    for item in data[service]["items"]:
                        current_item = data[service]["items"][item]
                        itm = Item(current_item["name"], current_item["nominal_volume"], current_item["quantity"],
                                   current_item["price"], current_item["rate"], current_item["rate_price"],
                                   current_item["current_volume"])
                        items[itm.name] = itm
                    self.create_service(service_name, service_price, items, service_cost_price, service_used_times)

        except FileNotFoundError:
            with open("services.json", "wt") as file:
                pass

    @Slot()
    def add_service(self):
        self.service_form = self.ServiceForm(self.storage, self.main_ui.list_of_services)
        self.service_form.data_set.connect(self.create_service)
        self.service_form.show()

    @Slot()
    def create_service(self, name: str, service_price: int, service_storage: dict, cost_price: float,
                       service_used_times: int):
        service = Service(name, service_price, cost_price)
        service.used_times = service_used_times
        service.plus_button.pressed.connect(self.plus)
        service.minus_button.pressed.connect(self.minus)
        for item in service_storage:
            service.add_item(service_storage[item])
        self.services[service.name] = service
        self.update_list_storage()
        self.total_storage_update()
        table_services = self.main_ui.list_of_services
        row_pos = table_services.rowCount()
        table_services.insertRow(row_pos)
        table_services.setItem(row_pos, 0, QTableWidgetItem(service.name))
        table_services.setItem(row_pos, 1, QTableWidgetItem(str(service.service_price)))
        table_services.setItem(row_pos, 2, QTableWidgetItem(str(service.cost_price)))
        table_services.setCellWidget(row_pos, 3, service.plus_button)
        table_services.setCellWidget(row_pos, 4, service.minus_button)
        table_services.setItem(row_pos, 5, QTableWidgetItem(str(service.used_times)))

    @Slot()
    def edit_service(self):
        current_row = self.main_ui.list_of_services.currentRow()
        service = self.services[self.main_ui.list_of_services.item(current_row, 0).text()]
        self.service_form = self.ServiceForm(self.storage, self.main_ui.list_of_services, service, current_row)
        self.service_form.data_change.connect(self.edit_service_row)
        self.service_form.show()

    @Slot()
    def edit_service_row(self, name: str, service_price: int, service_storage: dict, cost_price: float, current_row):
        self.delete_service(current_row)
        self.create_service(name, service_price, service_storage, cost_price)

    @Slot()
    def delete_service(self, current_row=None):
        table = self.main_ui.list_of_services
        current_row = table.currentRow() if current_row is None else current_row
        service_name = table.item(current_row, 0).text()
        del self.services[service_name]
        table.removeRow(current_row)

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

    def msg(self, items):
        if isinstance(items, str):
            msg = QMessageBox.warning(self, "Предупреждение", f"{items} уже существуют !")
        elif isinstance(items, list):
            msg = QMessageBox.warning(self, "Предупреждение", f"Недостаточно {items} !")

    def update_list_storage(self):
        for item in self.storage:
            row = self.main_ui.list_of_materials.findItems(item.name, Qt.MatchFixedString)[0].row()
            self.main_ui.list_of_materials.item(row, 2).setText(f"{item.quantity}")
        self.total_storage_update()

    def total_storage_update(self):
        self.storage.sum_total_amount()
        item = self.main_ui.total_list.item(0, 1)
        item.setText(f"{self.storage.total_amount} руб")
        header = self.main_ui.total_list.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)

    def closeEvent(self, event: QCloseEvent):
        self.writeSettings()
        QApplication.quit()


if __name__ == "__main__":
    pass
