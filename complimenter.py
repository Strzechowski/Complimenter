#!/usr/bin/env python3

import sys
import requests
import json

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from functools import partial

class ComplimenterUi(QMainWindow):
    """Complimenter's View (GUI)."""
    def __init__(self, resolution):
        super().__init__()
        # Set main window's properties
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        self.setWindowTitle('Complimenter!')
        self.setWindowIcon(QIcon("icon.png"))
        self.resolution = resolution
        self.sizeX = 320
        self.sizeY = 240
        self._placeWindowInTheMiddle()

        # Set the central widget
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        # Set display and button
        self._createButton()
        self._createDisplay()


    def _placeWindowInTheMiddle(self):
        X = (self.resolution.width() - self.sizeX) / 2
        Y = (self.resolution.height() - self.sizeY) / 2
        self.setGeometry(X, Y, self.sizeX, self.sizeY)
        self.setMaximumSize(2*self.sizeX, self.sizeY)


    def _createButton(self):
        self.mainButton = QPushButton('Give me compliment!')

        # Palette set-up
        p = self.mainButton.palette()
        p.setColor(self.mainButton.backgroundRole(), Qt.red)
        self.mainButton.setPalette(p)

        self.mainButton.setFixedHeight(60)
        self.generalLayout.addWidget(self.mainButton)


    def _createDisplay(self):
        # Create the display widget
        self.display = QLabel()
        self.display.setFixedHeight(80)
        self.display.setAlignment(Qt.AlignCenter)

        # Add the display to the general layout
        self.generalLayout.addWidget(self.display)

        self.display.setStyleSheet('background-color: pink')


    def setDisplayText(self, text):
        self.display.setText(text)
        self.display.setFocus()



class ComplimenterCtrl:
    def __init__(self, view):
        self._view = view
        self._connectSignals()


    def _buildCompliment(self):
        try:
            response = requests.get("https://complimentr.com/api")
            json_compliment = response.json()
            self._view.setDisplayText(json_compliment["compliment"].capitalize())
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.HTTPError):
            self._view.setDisplayText("Something is wrong with connection!")


    def _connectSignals(self):
        self._view.mainButton.clicked.connect(partial(self._buildCompliment))


def main():
    # Create an instance of QApplication
    complimenter = QApplication(sys.argv)
    resolution = complimenter.desktop().screenGeometry()
    view = ComplimenterUi(resolution)
    view.show()

    ComplimenterCtrl(view=view)
    sys.exit(complimenter.exec_())

if __name__ == '__main__':
    main()
