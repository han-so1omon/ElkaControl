# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QDialog

app = QApplication(sys.argv)
window = QDialog()
ui.setupUi(window)

window.show()
sys.exit(app.exec_())
