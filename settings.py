# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from settingsui import Ui_SettingsDialog
from lang import tr

class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super(SettingsDialog, self).__init__(parent)
        self.ui = Ui_SettingsDialog()
        self.ui.setupUi(self)
        self.setStyleSheet('color: #eee; background: #222;')
        self.ui.cbMonitor.addItem(tr("notspecmonitor"))
        for scr in parent.qApp.screens():
            g = scr.geometry()
            self.ui.cbMonitor.addItem(f'{scr.model()} {g.width()}X{g.height()}')
