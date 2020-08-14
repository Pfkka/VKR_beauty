import transliterate
from PySide2.QtGui import QCloseEvent

from main_form import Ui_MainWindow
from create_form import Ui_Form
from PySide2.QtWidgets import QMainWindow, QWidget, QApplication, QTableWidget, QTableWidgetItem, QAbstractItemView
from PySide2.QtCore import Slot, QSettings, QSize, QPoint


class Item:
	def __init__(self, name: str, nominal_volume: int, quantity: int, price: int):
		self.name = name
		self.nominal = nominal_volume
		self.price = price
		self.rate = 0
		self.quantity = quantity
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

	def add_item(self, item: Item):
		try:
			if self._boxes[item.name][item.nominal].nominal == item.nominal:
				print("Item is exist")
		except KeyError:
			try:
				self._boxes[item.name].update({item.nominal: item})
			except KeyError:
				self._boxes[item.name] = {item.nominal: item}

	def delete(self, name: str, volume: int):
		try:
			del self._boxes[name][volume]
		except KeyError:
			print("Item not found")

	def get_item(self, name: str, volume: int):
		try:
			return self._boxes[name][volume]
		except KeyError:
			print("Not found")

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
	class CreateForm(QWidget):
		def __init__(self, storage, table: QTableWidget):
			super().__init__()
			self.ui = Ui_Form()
			self.ui.setupUi(self)
			self.ui.applyButton.pressed.connect(self.apply)
			self.ui.cancelButton.pressed.connect(self.cancel)

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
			self.cancel()

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
		def cancel(self):
			self.writeSettings()
			self.close()

	def __init__(self):
		super().__init__()
		self.main_ui = Ui_MainWindow()
		self.main_ui.setupUi(self)
		self.storage = Storage()
		self.create = None
		self.main_ui.add_materialButton.pressed.connect(self.add_material)

		self.main_ui.list_of_materials.setSortingEnabled(True)
		self.main_ui.list_of_materials.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.main_ui.list_of_materials.setColumnCount(4)
		self.main_ui.list_of_materials.setHorizontalHeaderLabels(["Название", "Объем", "Количество", "Цена"])
		self.readSettings()

	def writeSettings(self):
		settings = QSettings()
		settings.beginGroup("MainForm")
		settings.setValue("size", self.size())
		settings.setValue("pos", self.pos())
		settings.endGroup()

	def readSettings(self):
		settings = QSettings()
		settings.beginGroup("MainForm")
		self.resize(settings.value("size", QSize()))
		self.move(settings.value("pos", QPoint()))
		settings.endGroup()

	@Slot()
	def add_material(self):
		self.create = self.CreateForm(self.storage, self.main_ui.list_of_materials)
		print(self.main_ui.list_of_materials)
		self.create.show()

	def closeEvent(self, event: QCloseEvent):
		self.writeSettings()
		QApplication.quit()


if __name__ == "__main__":
	pass
	# s = Storage()
	# item1 = Item("Cream", 100, 5, 500)
	# item2 = Item("Cream", 50, 3, 200)
	# item3 = Item("Something", 150,105, 700)
	# s.add_item(item1)
	# s.add_item(item2)
	# s.add_item(item3)
	# print(s)


	# a = transliterate.translit("Привет", reversed=True)
	# print(a)
	# b = transliterate.translit(a, "ru")
	# print(b)
