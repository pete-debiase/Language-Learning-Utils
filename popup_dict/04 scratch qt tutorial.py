#!/usr/bin/python

"""
ZetCode PySide tutorial

This program creates a skeleton of
a classic GUI application with a menubar,
toolbar, statusbar and a central widget.

author: Jan Bodnar
website: zetcode.com
"""

from PySide6 import *
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit


class Example(QMainWindow):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):
        textEdit = QTextEdit()
        self.setCentralWidget(textEdit)

        exitAction = QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAction)

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Main window')
        self.show()


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
