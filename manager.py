import transliterate
from PySide2.QtGui import QCloseEvent

from main_form import Ui_MainWindow
from create_form import Ui_Form
from PySide2.QtWidgets import QMainWindow, QWidget, QApplication
from PySide2.QtCore import Slot, QSettings, QSize, QPoint


class Storage:
	def __init__(self):
		self._boxes = dict()

	def add_item(self, name: str, volume: int, quantity: int, price=None):
		try:
			self._boxes[name][f"volume {volume}"]["quantity"] += quantity
			if price:
				self._boxes[name][f"volume {volume}"]["price"] = price
		except KeyError:
			try:
				self._boxes[name][f"volume {volume}"] = {"quantity": quantity, "price": price}
			except KeyError:
				self._boxes[name] = {f"volume {volume}": {"quantity": quantity, "price": price}}

	def delete(self, name: str, volume: int = None):
		if volume:
			del self._boxes[name][f"volume {volume}"]
		else:
			del self._boxes[name]

	def get_item(self, name: str, volume: int):
		try:
			return self._boxes[name][f"volume {volume}"]
		except KeyError:
			print("Not found")


class Service:
	class Item:
		def __init__(self, name: str, nominal_volume: int, current_volume: int, price, rate):
			self.name = name
			self.nominal = nominal_volume
			self.price = price
			self.rate = rate
			self.rate_price = (self.rate / self.nominal) * self.price
			self.current_volume = current_volume

		def one_use(self):
			if self.current_volume > self.rate:
				self.current_volume -= self.rate
			else:
				pass  # забрать со склада новую пачку - обновить объем - в случае чего изменить цену и объем пачки

	def __init__(self, name: str, service_price):
		self.name = name
		self.service_price = service_price
		self.cost_price = None
		self.net_profit = None
		self.service_storage = dict()

	def add_item(self, item: Item):
		self.service_storage[item.name] = item

	def total_amount(self):
		self.cost_price = 0  # себестоимость
		for item in self.service_storage:
			self.cost_price += self.service_storage[item].rate_price
		self.net_profit = self.service_price - self.cost_price


class MainWindow(QMainWindow):
	class CreateForm(QWidget):
		def __init__(self):
			super().__init__()
			self.ui = Ui_Form()
			self.ui.setupUi(self)
			self.ui.applyButton.pressed.connect(self.apply)
			self.ui.cancelButton.pressed.connect(self.cancel)
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
			name = self.ui.name_lineedit.text()
			volume = self.ui.volume_lineedit.text()
			quantity = self.ui.quantity_lineedit.text()
			price = self.ui.price_lineedit.text()

		@Slot()
		def cancel(self):
			self.writeSettings()
			self.close()

	def __init__(self):
		super().__init__()
		self.main_ui = Ui_MainWindow()
		self.main_ui.setupUi(self)
		self.create = None
		self.main_ui.add_materialButton.pressed.connect(self.add_material)
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
		self.create = self.CreateForm()
		self.create.show()

	def closeEvent(self, event: QCloseEvent):
		self.writeSettings()
		QApplication.quit()



# s = Storage()
# s.add_item("a", 10, 50, 100)
# s.add_item("a", 20, 100, 200)
# s.add_item("b", 1, 10, 100)
# # print(s._boxes)
# a = transliterate.translit("Привет", reversed=True)
# print(a)
# b = transliterate.translit(a, "ru")
# print(b)
