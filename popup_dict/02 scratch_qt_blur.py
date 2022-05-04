#!/usr/bin/env python3
"""Testing"""

import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget

from blurWindow import GlobalBlur


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(1000, 700)
        self.setWindowFlags(Qt.CustomizeWindowHint)
        # self.setWindowIcon(QIcon(r'C:\Users\pete\ALL\DV\Aesthetics\Avatars\T-Rex\t-rex_profile_clear.png'))

        GlobalBlur(self.winId(), hexColor='#272822EA', Dark=True, QWidget=self)

        self.setStyleSheet('background-color: rgba(256, 256, 256, 256)')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())
