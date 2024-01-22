import os
import sys
import platform
from PyQt5 import QtWidgets, QtGui, QtCore


class Frame(QtWidgets.QFrame):
    mouseMoved = QtCore.pyqtSignal()

    def mousePressEvent(self, event):
        self.mouseMoved.emit()


class DisplayWindow(QtWidgets.QWidget):
    def __init__(self, qApp, player, display_index=0):
        super(DisplayWindow, self).__init__()
        if platform.system() == "Darwin": # for MacOS
            self.videoframe = QtWidgets.QMacCocoaViewContainer(0)
        else:
            self.videoframe = Frame()
            self.videoframe.mouseMoved.connect(self.onMouseMove)
        self.palette = self.videoframe.palette()
        self.palette.setColor(QtGui.QPalette.Window, QtGui.QColor(0, 0, 15))
        self.videoframe.setPalette(self.palette)
        self.videoframe.setAutoFillBackground(True)
        #self.videoframe.setStyleSheet('background: #083;')

        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.addWidget(self.videoframe)
        self.qApp = qApp
        self.display_index = display_index
        self.doclose = False
        sets = QtCore.QSettings(os.path.join('RoganovSoft', 'VideoPlayer'),'config')
        sets.beginGroup('videowindow')
        self.mW = int(sets.value('width', '1066'))
        self.mH = int(sets.value('height', '600'))
        self.mX = int(sets.value('left', '9999'))
        self.mY = int(sets.value('top', '9999'))
        if self.mX == 9999 or self.mY == 9999:
            screenres = self.qApp.desktop().screenGeometry(self.display_index)
            self.mX = (screenres.width() - self.mW) // 2 + screenres.x()
            self.mY = (screenres.height() - self.mH) // 2 + screenres.y()
        self.isfullscreen = False
        sets.endGroup()

        self.resize(self.mW, self.mH)
        self.move(self.mX, self.mY)
        self.esc_sc = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape), self)
        self.esc_sc.activated.connect(self.close)
        self.fs_sc = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F), self)
        self.fs_sc.activated.connect(self.fullscreenchange)
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.onTimer)
        self.cursor_pos = QtGui.QCursor.pos()
        self.cursor_visible = True
        self.timer.start()
        self.setPlayer(player)
        self.setVideoWindow()


    def onMouseMove(self):
        if self.isfullscreen:
            if not self.cursor_visible:
                self.qApp.setOverrideCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
                self.cursor_visible = True


    def onTimer(self):
        if not self.isfullscreen: return
        pos = QtGui.QCursor.pos()
        if pos.x() == self.cursor_pos.x() and pos.y() == self.cursor_pos.y():
            if self.cursor_visible:
                self.qApp.setOverrideCursor(QtGui.QCursor(QtCore.Qt.BlankCursor))
                self.cursor_visible = False
        else:
            if not self.cursor_visible:
                self.qApp.setOverrideCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
                self.cursor_visible = True
        self.cursor_pos = pos

    def setPlayer(self, player):
        self.player = player
        self.pause_sc = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Space), self)
        self.pause_sc.activated.connect(self.player.play_pause)
        self.skip_b_min_sc = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Left), self)
        self.skip_b_min_sc.activated.connect(self.player.skip_b_min)
        self.skip_f_min_sc = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Right), self)
        self.skip_f_min_sc.activated.connect(self.player.skip_f_min)
        self.skip_f_mid_sc = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Up), self)
        self.skip_f_mid_sc.activated.connect(self.player.skip_f_mid)
        self.skip_b_mid_sc = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Down), self)
        self.skip_b_mid_sc.activated.connect(self.player.skip_b_mid)
        self.skip_b_max_sc = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_PageDown), self)
        self.skip_b_max_sc.activated.connect(self.player.skip_b_max)
        self.skip_f_max_sc = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_PageUp), self)
        self.skip_f_max_sc.activated.connect(self.player.skip_f_max)
        self.volume_up_sc = QtWidgets.QShortcut(QtGui.QKeySequence(42), self)
        self.volume_up_sc.activated.connect(self.volume_up)
        self.volume_down_sc = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Slash), self)
        self.volume_down_sc.activated.connect(self.volume_down)
        #self.skip_b_sub_en = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_V), self)
        #self.skip_b_sun_en.activated.connect(self.sub_vkl)

    def volume_up(self):
        v = self.player.volume
        if v < 100:
            v += 10
            if v > 100: v = 100
            self.player.set_volume(v)
            self.player.volumeChanged.emit(v)


    def volume_down(self):
        v = self.player.volume
        if v > 0:
            v -= 10
            if v < 0: v = 0
            self.player.set_volume(v)
            self.player.volumeChanged.emit(v)

    def setVideoWindow(self):
        if platform.system() == "Linux": # for Linux using the X Server
            self.player.mediaplayer.set_xwindow(int(self.videoframe.winId()))
        elif platform.system() == "Windows": # for Windows
            self.player.mediaplayer.set_hwnd(int(self.videoframe.winId()))
        elif platform.system() == "Darwin": # for MacOS
            self.player.mediaplayer.set_nsobject(int(self.videoframe.winId()))

    def fullscreenchange(self):
        self.set_FullScreen(not self.isfullscreen)

    def showFullScreen(self):
        self.mX = self.pos().x()
        self.mY = self.pos().y()
        self.mW = self.width()
        self.mH = self.height()
        self.isfullscreen = True
        super(DisplayWindow, self).showFullScreen()

    def set_FullScreen(self, isfullscreen):
        if isfullscreen:
            if not self.isfullscreen:
                self.mX = self.pos().x()
                self.mY = self.pos().y()
                self.mW = self.width()
                self.mH = self.height()
            self.isfullscreen = True
            self.setWindowState(QtCore.Qt.WindowFullScreen)
        else:
            self.isfullscreen = False
            self.setWindowState(QtCore.Qt.WindowNoState)
            super(DisplayWindow, self).show()
            if not self.cursor_visible:
                self.qApp.setOverrideCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
                self.cursor_visible = True


    def showvideowindow(self, fullscreen, displayindex=-1):
        if fullscreen:
            self.isfullscreen = True
            if displayindex >= 0 and displayindex < len(self.qApp.screens()) :
                self.display_index = displayindex
                screenres = self.qApp.desktop().screenGeometry(self.display_index)
                self.move(QtCore.QPoint(screenres.x(), screenres.y()))
                self.resize(screenres.width(), screenres.height())
            super(DisplayWindow, self).showFullScreen()
        else:
            self.set_FullScreen(False)


    def closeEvent(self, event):
        self.player.stop()
        self.timer.stop()
        if not self.cursor_visible:
            self.qApp.setOverrideCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
            self.cursor_visible = True
        sets = QtCore.QSettings(os.path.join('RoganovSoft', 'VideoPlayer'),'config')
        sets.beginGroup('videowindow')
        sets.setValue('width', self.mW)
        sets.setValue('height', self.mH)
        if self.isfullscreen:
            sets.setValue('left', self.mX)
            sets.setValue('top', self.mY)
        else:
            sets.setValue('left', self.pos().x())
            sets.setValue('top', self.pos().y())
            self.mX = self.pos().x()
            self.mY = self.pos().y()
            self.mW = self.width()
            self.mH = self.height()
            sets.setValue('width', self.mW)
            sets.setValue('height', self.mH)
        sets.endGroup()
        super(DisplayWindow, self).closeEvent(event)


