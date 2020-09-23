import sys
import unittest
from PySide2.QtWidgets import QApplication
from manager import Service, Storage, Item, MainWindow


class ItemTestCase(unittest.TestCase):

    def test_create_item(self):
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


class ServiceTestcase(unittest.TestCase):

    def test_init(self):
        service = Service("Some", 1000, 20.0)
        self.assertEqual(service.name, "Some")
        self.assertEqual(service.service_price, 1000)
        self.assertEqual(service.cost_price, 20.0)
        self.assertEqual(service.used_once, 0)


def main(argv):
    app = QApplication(argv)
    unittest.main()
    return app.exec_()


if __name__ == "__main__":
    main(sys.argv)