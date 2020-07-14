import transliterate


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
		def __init__(self, name: str, nominal_volume: int, volume: int, price, rate):
			self.name = name
			self.nominal = nominal_volume
			self.price = price
			self.rate = rate
			self.rate_price = (self.rate / self.nominal) * self.price
			self.volume = volume

		def one_use(self):
			if self.volume > self.rate:
				self.volume -= self.rate
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


s = Storage()
s.add_item("a", 10, 50, 100)
s.add_item("a", 20, 100, 200)
s.add_item("b", 1, 10, 100)
# print(s._boxes)
a = transliterate.translit("Привет", reversed=True)
print(a)
b = transliterate.translit(a, "ru")
print(b)
