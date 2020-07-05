class Storage:
	def __init__(self):
		self._boxes = dict()

	def add_item(self, name: str, quantity: int, volume: int = None, price=None):
		if volume:
			try:
				if self._boxes[name][f"volume {volume}"]:
					self._boxes[name][f"volume {volume}"]["quantity"] += quantity
					if price:
						self._boxes[name][f"volume {volume}"]["price"] = price
				else:
					self._boxes[name][f"volume {volume}"]["quantity"] = quantity
					self._boxes[name][f"volume {volume}"]["price"] = price
			except KeyError:
				try:
					self._boxes[name][f"volume {volume}"] = {"quantity": quantity, "price": price}
				except KeyError:
					self._boxes[name] = {f"volume {volume}": {"quantity": quantity, "price": price}}
		else:
			try:
				self._boxes[name]["quantity"] += quantity
				if price:
					self._boxes[name]["price"] = price
			except KeyError:
				self._boxes[name] = {"quantity": quantity, "price": price}

	def delete(self, name: str, volume: int = None):
		if volume:
			del self._boxes[name][f"volume {volume}"]
		else:
			del self._boxes[name]

	def get_item(self, name: str, volume: int = None):
		try:
			return self._boxes[name][f"volume {volume}"] if volume else self._boxes[name]
		except KeyError:
			print("Not found")


class Service:
	def __init__(self, name: str):
		self._name = name


s = Storage()
s.add_item("a", 10, 50, 100)
s.add_item("a", 20, 100, 200)
s.add_item("b", 10, price=100)
print(s._boxes)
