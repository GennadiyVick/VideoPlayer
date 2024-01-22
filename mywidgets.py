from PyQt5 import QtCore, QtGui, QtWidgets

class MyLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()

    def __init__(self, styles, parent):
        super(MyLabel, self).__init__(parent)
        self.styles = styles if styles != None else {}
        self.checkable = False
        self.checked = False
        '''self.default_ss = ''
        if len(self.images) == 1:
            self.default_ss = 'QLabel {background:  url("'+self.images[0]+'") no-repeat center center }'
        elif len(self.images) > 1:
            self.default_ss = 'QLabel {background:  url("'+self.images[0]+'") no-repeat center center } QLabel:hover {background:  url("'+self.images[1]+'") no-repeat center center}'
        if len(self.images) == 3:
            self.press_ss = 'QLabel {background:  url("'+self.images[2]+'") no-repeat center center }'
        else:
            self.press_ss = ''
        '''
        if 'default' in self.styles:
            self.setStyleSheet(self.styles['default'])
        self.leftbtn = False

    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.leftbtn = True

            if 'pressed' in self.styles:
                self.setStyleSheet(self.styles['pressed'])
            self.raise_()

    def mouseReleaseEvent(self, event):
        if self.leftbtn:
            self.leftbtn = False

            x, y = event.pos().x(), event.pos().y()
            if x > 0 and y > 0 and x < 60 and y < 45:
                self.clicked.emit()
                if self.checkable:
                    self.checked = not self.checked

            if self.checked and 'checked' in self.styles:
                self.setStyleSheet(self.styles['checked'])
            elif 'default' in self.styles:
                self.setStyleSheet(self.styles['default'])

class MyWidget(QtWidgets.QWidget):
    #onMousePress = QtCore.pyqtSignal(QtGui.QMouseEvent)
    #onMouseRelease = QtCore.pyqtSignal(QtGui.QMouseEvent)
    #onMouseMove = QtCore.pyqtSignal(QtGui.QMouseEvent)

    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)
        self.setMouseTracking(True)
        self.parent = parent
        self.mx = 0
        self.my = 0
        self.mousedown = False
        self.caption = ''

    def mousePressEvent(self, event):
        if self.parent is None:
            return
        if event.buttons() == QtCore.Qt.LeftButton:
            self.mx = event.globalX()
            self.my = event.globalY()
            self.l = self.parent.parent().pos().x()
            self.t = self.parent.parent().pos().y()
            self.mousedown = True
            #self.onMousePress.emit(event)

    def mouseReleaseEvent(self, event):
        self.mousedown = False
        #self.onMouseRelease.emit(event)

    def mouseMoveEvent(self, event):
        if self.mousedown:
            x = event.globalX()
            y = event.globalY()
            t = y-self.my+self.t
            l = x-self.mx+self.l
            self.parent.parent().move(l, t)

    def paintEvent(self, event):
        if len(self.caption) == 0:
            super(MyWidget, self).paintEvent(event)
            return
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QColor(220,220,255))
        painter.drawText(event.rect().adjusted(1,1,1,1), QtCore.Qt.AlignCenter, self.caption)
