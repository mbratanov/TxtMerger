import sys

from PySide6.QtWidgets import QApplication

from txtmerger.ui.main_window import MainWindow


def main():
    app = QApplication()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
