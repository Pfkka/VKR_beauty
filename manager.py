import json
from PySide2.QtGui import QCloseEvent
from main_form_1 import Ui_MainWindow
from create_form import Ui_Form
from create_service_form import Ui_Service_form
from PySide2.QtWidgets import QMainWindow, QWidget, QApplication, QTableWidget, QTableWidgetItem, QAbstractItemView
from PySide2.QtCore import Slot, QSettings, QSize, QPoint


class Forms:
	def writeSettings(self):
		pass

	def writeSettings(self):
		pass


class Item:
	def __init__(self, name: str, nominal_volume: int, quantity: int, price: int):
		self.name = name.capitalize()
		self.nominal = nominal_volume
		self.quantity = quantity
		self.price = price
		self.rate = 0
		self.rate_price = (self.rate / self.nominal) * self.price
		self.current_volume = nominal_volume

	def one_use(self):
		if self.current_volume > self.rate:
			self.current_volume -= self.rate
		else:
			pass  # забрать со склада новую пачку - обновить объем - в случае чего изменить цену и объем пачки

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
		with open("storage.json", "rt") as file:
			data = json.load(file)
			for itm in data:
				for nominal in data[itm]:
					item = Item(data[itm][nominal]["name"], data[itm][nominal]["nominal_volume"],
								data[itm][nominal]["quantity"], data[itm][nominal]["price"])
					self.add_item(item)
		self.sum_total_amount()

	def __iter__(self):
		for nominal in self._boxes:
			for item in self._boxes[nominal]:
				yield self._boxes[nominal][item]

	def __str__(self):
		return f"{self._boxes}"


class Service:

	def __init__(self, name: str, service_price: int):
		self.name = name
		self.service_price = service_price
		self.cost_price = 0  # себестоимость
		self.net_profit = 0
		self.service_storage = dict()

	def add_item(self, item: Item, rate):
		item.rate = rate
		self.service_storage[item.name] = item

	def total_amount(self):
		for item in self.service_storage:
			self.cost_price += self.service_storage[item].rate_price
		self.net_profit = self.service_price - self.cost_price


class MainWindow(QMainWindow):
	class ServiceForm(QWidget):
		def __init__(self):
			super().__init__()
			self.service_ui = Ui_Service_form()
			self.service_ui.setupUi(self)
			self.readSettings()

		def writeSettings(self):
			settings = QSettings()
			settings.beginGroup("ServiceForm")
			settings.setValue("size", self.size())
			settings.setValue("pos", self.pos())
			settings.endGroup()

		def readSettings(self):
			settings = QSettings()
			settings.beginGroup("ServiceForm")
			self.resize(settings.value("size", QSize()))
			self.move(settings.value("pos", QPoint()))
			settings.endGroup()

		def closeEvent(self, event: QCloseEvent):
			self.writeSettings()
			self.close()

	class CreateForm(QWidget):
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
			self.resize(settings.value("size", QSize()))
			self.move(settings.value("pos", QPoint()))
			settings.endGroup()

		def closeEvent(self, event: QCloseEvent):
			print("1")
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
			item = Item(name, int(volume), int(quantity), int(price))
			row_pos = self.table.rowCount()
			self.table.insertRow(row_pos)
			self.table.setItem(row_pos, 0, QTableWidgetItem(name))
			self.table.setItem(row_pos, 1, QTableWidgetItem(volume))
			self.table.setItem(row_pos, 2, QTableWidgetItem(quantity))
			self.table.setItem(row_pos, 3, QTableWidgetItem(price))

			self.storage.add_item(item)
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
			self.storage.edit_box(self.current_name, int(self.current_volume), name, int(volume), int(quantity),
								  int(price))
			row_pos = self.table.currentRow()
			self.table.item(row_pos, 0).setText(name)
			self.table.item(row_pos, 1).setText(volume)
			self.table.item(row_pos, 2).setText(quantity)
			self.table.item(row_pos, 3).setText(price)
			self.close()

	def __init__(self):
		super().__init__()
		self.main_ui = Ui_MainWindow()
		self.main_ui.setupUi(self)
		self.storage = Storage()
		self.service_storage = dict()
		self.create = None
		self.service_form =None
		self.main_ui.add_materialButton.pressed.connect(self.add_material)
		self.main_ui.edit_materialButton.pressed.connect(self.edit_item)
		self.main_ui.delete_materialButton.pressed.connect(self.delete_item)
		self.main_ui.list_of_materials.itemDoubleClicked.connect(self.edit_item)

		self.main_ui.add_serviceButton.pressed.connect(self.add_service)

		self.main_ui.list_of_materials.setSortingEnabled(True)
		self.main_ui.list_of_materials.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.main_ui.list_of_materials.setColumnCount(4)
		self.main_ui.list_of_materials.setHorizontalHeaderLabels(["Название", "Объем", "Количество", "Цена"])

		self.main_ui.total_list.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.main_ui.total_list.setColumnCount(2)
		self.main_ui.total_list.setRowCount(1)
		self.main_ui.total_list.horizontalHeader().setVisible(False)
		self.main_ui.total_list.verticalHeader().setVisible(False)
		self.main_ui.total_list.setShowGrid(False)
		self.main_ui.total_list.setItem(0, 0, QTableWidgetItem("Стоимость склада:"))
		self.readSettings()

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
		self.resize(settings.value("size", QSize()))
		self.move(settings.value("pos", QPoint()))
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
		self.service_form = self.ServiceForm()
		self.service_form.show()

	@Slot()
	def add_material(self):
		self.create = self.CreateForm(self.storage, self.main_ui.list_of_materials)
		self.create.show()

	@Slot()
	def edit_item(self):
		try:
			current_name = self.main_ui.list_of_materials.item(self.main_ui.list_of_materials.currentRow(), 0).text()
			current_volume = self.main_ui.list_of_materials.item(self.main_ui.list_of_materials.currentRow(), 1).text()
			current_quantity = self.main_ui.list_of_materials.item(self.main_ui.list_of_materials.currentRow(),
																   2).text()
			current_price = self.main_ui.list_of_materials.item(self.main_ui.list_of_materials.currentRow(), 3).text()
			self.create = self.CreateForm(self.storage, self.main_ui.list_of_materials, "edit", current_name,
										  current_volume)
			self.create.ui.name_lineedit.setText(current_name)
			self.create.ui.volume_lineedit.setText(current_volume)
			self.create.ui.quantity_lineedit.setText(current_quantity)
			self.create.ui.price_lineedit.setText(current_price)
			self.create.show()
		except AttributeError:
			return

	@Slot()
	def delete_item(self):
		row_now = self.main_ui.list_of_materials.currentRow()
		if row_now != -1:
			current_name = self.main_ui.list_of_materials.item(row_now, 0).text()
			current_volume = int(self.main_ui.list_of_materials.item(row_now, 1).text())
			self.main_ui.list_of_materials.removeRow(row_now)
			self.storage.delete_item(current_name, current_volume)
		else:
			return

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
