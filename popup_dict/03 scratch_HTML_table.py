#!/usr/bin/env python3
"""Table"""

import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel

app = QApplication(sys.argv)
#label = QLabel("Hello World!")
label = QLabel("<table><tr><td>残り香</td><td>のこりが<br>のこりか</td><td><ol><li>lingering scent/lingering fragrance/residual aroma</li></ol></td></tr></table>")
label.setAlignment(Qt.AlignCenter)
label.show()
app.exec_()
