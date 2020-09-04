import os, sys
from PySide2.QtWidgets import QApplication
# from PySide2.QtCore import QTranslator
from manager import MainWindow


def main(argv):
    app = QApplication(argv)
    app.setApplicationName("MyBeauty")
    app.setOrganizationName("Egor_Nezhensky")
    w = MainWindow()
    w.show()
    #
    # t = QTranslator(app)
    # t.load('translations/ru_RU', os.path.dirname(__file__))
    # app.installTranslator(t)

    return app.exec_()


if __name__ == '__main__':
    os.environ['QT_PATH_PLATFORM_PLUGIN_PATH'] = './platforms'
    exit_code = main(sys.argv)
    sys.exit(exit_code)
