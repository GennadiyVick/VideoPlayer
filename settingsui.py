# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settingsui.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from lang import tr

class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        SettingsDialog.setObjectName("SettingsDialog")
        SettingsDialog.resize(400, 167)
        SettingsDialog.setWindowTitle(tr("settings"))
        self.mainlayout = QtWidgets.QVBoxLayout(SettingsDialog)
        self.mainlayout.setObjectName("mainlayout")
        self.gb_videowindowsettings = QtWidgets.QGroupBox(SettingsDialog)
        self.gb_videowindowsettings.setTitle(tr("videowindowsets"))
        self.gb_videowindowsettings.setObjectName("gb_videowindowsettings")
        self.lo_videosettings = QtWidgets.QVBoxLayout(self.gb_videowindowsettings)
        self.lo_videosettings.setContentsMargins(-1, -1, 0, 0)
        self.lo_videosettings.setObjectName("lo_videosettings")
        self.cb_fullscreen = QtWidgets.QCheckBox(self.gb_videowindowsettings)
        self.cb_fullscreen.setText(tr("playfullscreen"))
        self.cb_fullscreen.setObjectName("cb_fullscreen")
        self.lo_videosettings.addWidget(self.cb_fullscreen)
        self.l_monitor = QtWidgets.QLabel(self.gb_videowindowsettings)
        self.l_monitor.setText(tr("choosemonitor"))
        self.l_monitor.setObjectName("l_monitor")
        self.lo_videosettings.addWidget(self.l_monitor)
        self.cbMonitor = QtWidgets.QComboBox(self.gb_videowindowsettings)
        self.cbMonitor.setCurrentText("")
        self.cbMonitor.setMaxVisibleItems(4)
        self.cbMonitor.setObjectName("cbMonitor")
        self.lo_videosettings.addWidget(self.cbMonitor)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.lo_videosettings.addItem(spacerItem)
        self.mainlayout.addWidget(self.gb_videowindowsettings)
        self.buttonBox = QtWidgets.QDialogButtonBox(SettingsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.mainlayout.addWidget(self.buttonBox)

        self.retranslateUi(SettingsDialog)
        self.buttonBox.accepted.connect(SettingsDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(SettingsDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(SettingsDialog)

    def retranslateUi(self, SettingsDialog):
        pass