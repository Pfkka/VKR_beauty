import sys
import unittest
from PySide2.QtWidgets import QApplication
from manager import Service, Storage, Item


class ItemTestCase(unittest.TestCase):
    """
    Тестирование класса Item на корректность: инизиализации, присвоения расхода и списания расхода.
    """
    def test_init_item(self):
        item = Item("Cream", 1000, 3, 2000)
        self.assertEqual(item.nominal, 1000)
        self.assertEqual(item.quantity, 3)
        self.assertEqual(item.price, 2000)
        self.assertEqual(item.rate, 0)
        self.assertEqual(item.rate_price, 0)
        self.assertEqual(item.current_volume, 1000)

    def test_set_rate(self):
        item = Item("Cream", 1000, 3, 2000)
        item.rate = 10
        self.assertEqual(item.rate, 10)
        self.assertEqual(item.rate_price, 20)

    def test_use_func(self):
        item = Item("Cream", 1000, 1, 2000)
        item.rate = 20
        storage = Storage()
        storage.add_item(item)
        item.one_use(True, storage)
        self.assertEqual(item.current_volume, 980)
        item.one_use(False, storage)
        self.assertEqual(item.current_volume, 1000)
        item.rate = 1050
        self.assertEqual(item.one_use(True, storage), item.name)


class StorageTestCase(unittest.TestCase):
    """
    Тестирование класса склада на корректность: добавления, изменнения, удаления предметов и сериализации хранилища.
    """

    def test_add_item(self):
        storage = Storage()
        item = Item("Cream", 1000, 1, 2000)
        self.assertEqual(len(storage), 0)
        storage.add_item(item)
        self.assertEqual(len(storage), 1)
        self.assertIs(item, storage[item.name][item.nominal])

    def test_edit_item(self):
        storage = Storage()
        item = Item("Cream", 1000, 1, 2000)
        storage.add_item(item)
        storage.edit_box("Cream", 1000, "Scrab", 500, 3, 1500)
        self.assertRaises(KeyError, lambda: storage["Cream"][1000])
        self.assertIsInstance(storage["Scrab"][500], Item)
        self.assertEqual(storage["Scrab"][500].name, "Scrab")
        self.assertEqual(storage["Scrab"][500].nominal, 500)
        self.assertEqual(storage["Scrab"][500].quantity, 3)
        self.assertEqual(storage["Scrab"][500].price, 1500)
        storage.add_item(item)
        self.assertEqual(storage.edit_box("Scrab", 500, "Cream", 1000, 1, 2000), "Cream")

    def test_delete_item(self):
        storage = Storage()
        item = Item("Cream", 1000, 1, 2000)
        storage.add_item(item)
        self.assertEqual(storage.delete_item("Smth", 1000), None)
        self.assertEqual(storage.delete_item("Cream", 999), None)
        storage.delete_item(item.name, item.nominal)
        self.assertRaises(KeyError, lambda: storage["Cream"][1000])
        self.assertEqual(len(storage), 0)

    def test_dict_ser(self):
        storage = Storage()
        item = Item("Cream", 1000, 1, 2000)
        test_dict = dict()
        test_dict[f"{item.name}"] = {
            item.nominal: {"name": item.name, "nominal_volume": item.nominal, "quantity": item.quantity,
                           "price": item.price}}
        storage.add_item(item)
        self.assertIsInstance(storage.to_dict(), dict)
        self.assertEqual(storage.to_dict(), test_dict)


class ServiceTestCase(unittest.TestCase):
    """
    Тестирование класса услушги на корректность: инициализации, добавления предмета и списания расходов с предметов.
    """
    APP = QApplication(sys.argv)

    def test_init(self):
        service = Service("Some", 1000, 20.0)
        self.assertEqual(service.name, "Some")
        self.assertEqual(service.service_price, 1000)
        self.assertEqual(service.cost_price, 20.0)
        self.assertEqual(service.used_once, 0)

    def test_add_item_in_service(self):
        service = Service("Some", 1000, 20.0)
        item = Item("Cream", 1000, 1, 2000)
        service.add_item(item)
        service_item = service.service_storage[item.name]
        self.assertIsInstance(service_item, Item)
        self.assertEqual(service_item.name, item.name)
        self.assertEqual(service_item.price, item.price)

    def test_service_use(self):
        service = Service("Some", 1000, 20.0)
        storage = Storage()
        item1 = Item("Cream", 1000, 1, 2000)
        item2 = Item("Scrab", 500, 3, 1500)
        item1.rate = 1001
        item2.rate = 505
        service.add_item(item1)
        service.add_item(item2)
        storage.add_item(item1)
        storage.add_item(item2)
        self.assertIsInstance(service.use(True, storage), list)
        self.assertEqual(len(service.use(True, storage)), 1)
        self.assertEqual(service.used_once, 0)


if __name__ == "__main__":
    unittest.main()
