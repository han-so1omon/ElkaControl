# -*- coding: utf-8 -*-
import sys,os
sys.path.append(os.getcwd())
from PyQt5.QtWidgets import QApplication,QDialog,QMainWindow
#TODO change this to dynamic import
from elkamainwindow import Ui_ElkaMainWindow

class MyApp(QMainWindow, Ui_ElkaMainWindow):
  def __init__(self):
    QMainWindow.__init__(self)
    Ui_ElkaMainWindow.__init__(self)
    self.setupUi(self)

if __name__ == "__main__":
  print str(sys.argv)
  app = QApplication(sys.argv)
  window = MyApp()
  window.show()
  sys.exit(app.exec_())
