# Author: Hoani Bryson
#
# UI Base - Binds UI control to a QT mainWindow object
#  from a configuration map

from PySide2.QtWidgets import QApplication
from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from EllipticCurve.utilities import vect
from EllipticCurve.utilities import vect
from EllipticCurve.ui import plotCanvas, extraConsole
import sys, os
import datetime
import math
import numpy as np
try:
  import qdarkstyle
except:
  pass


def load_from_file(filepath):
  ui_file = QFile(filepath)
  ui_file.open(QFile.ReadOnly)
  loader = QUiLoader()
  loader.registerCustomWidget(MainWindow)
  window = loader.load(ui_file)
  ui_file.close()
  return window


class MainWindow(QtWidgets.QMainWindow):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.show()
    self.t_start = datetime.datetime.now().timestamp()
    self.command_queue = None
    self.upkeep_timer = []
    try:
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())
    except:
        pass

    self.key_value_map = {}


  def load(self):
    self.lineEdit_equation = self.findChild(QtWidgets.QLineEdit, "LineEdit_equation")
    self.lineEdit_a = self.findChild(QtWidgets.QLineEdit, "LineEdit_a")
    self.lineEdit_b = self.findChild(QtWidgets.QLineEdit, "LineEdit_b")
    self.pushButton_plot = self.findChild(QtWidgets.QPushButton, "PushButton_plot")

    self.pushButton_plot.pressed.connect(self.plot_elliptic_curve)

    box = self.findChild(QtWidgets.QBoxLayout, "BoxLayout_plot")
    self.plot = plotCanvas.PlotCanvas(['b', 'b'], title="Elliptic Curve")
    box.addWidget(self.plot)


  def add_upkeep(self, period_ms, callback):
    timer = QtCore.QTimer(self)
    self.upkeep_timer.append(timer)
    timer.start(period_ms)
    timer.timeout.connect(callback)
    return timer


  def plot_elliptic_curve(self):
    a = float(self.lineEdit_a.text())
    b = float(self.lineEdit_b.text())
    self.lineEdit_equation.setText("y^2 = x^3 + {}x + {}".format(
      self.lineEdit_a.text(),
      self.lineEdit_b.text()
    ))

    x_min = self.brute_search_x_min(a,b)
    x_values = np.array(np.arange(x_min,10,0.001))
    y_values = np.zeros(len(x_values))
    for idx, x in enumerate(x_values):
      y_values[idx] = np.sqrt(x**3 + a*x + b)

    self.plot.set_data(x_values, [y_values, -y_values])

  def brute_search_x_min(self, a, b):
    x_min = 0
    while True:
      y = np.sqrt(x_min**3 + a*x_min + b)
      if y > 0.1:
        x_min -= 0.1
      else:
        return x_min


    
    


