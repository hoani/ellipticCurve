import sys, io
from PySide2.QtWidgets import QApplication
from EllipticCurve.ui import uiBase


class UiExecute:
  def __init__(self, ui_file_path):

    app = QApplication(sys.argv)

    window = uiBase.load_from_file(ui_file_path)
    window.load()

    sys.exit(app.exec_())
