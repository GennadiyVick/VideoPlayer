# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from mslider import MSlider
from mvolume import MVolume
from mywidgets import MyLabel, MyWidget
import sys
import platform
from lang import tr

def labelstyle(images):
    if len(images) == 1:
        return 'QLabel {background:  url("'+images[0]+'") no-repeat center center }'
    elif len(images) == 2:
        return 'QLabel {background:  url("'+images[0]+'") no-repeat center center } QLabel:hover {background:  url("'+images[1]+'") no-repeat center center}'
    else: return ''


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(359, 163)
        MainWindow.setWindowTitle("Video player")
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint) # | QtCore.Qt.Tool
        MainWindow.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet('''QWidget {color: #f0f0f0; background: #202021;} QWidget#centralwidget{border-style: inset;
border-width: 1px;
border-color: #a0404050;
border-radius: 10px;}
QScrollBar {border-radius: 5px;}
QScrollBar:vertical {border-radius: 5px; width: 10px;}
QScrollBar:horizontal {border-top: 1px solid #1c1c1c; height: 10px; }
QScrollBar::handle {margin: -1px; background: #446; border: 1px solid #1c1c1c;}
QScrollBar::handle:vertical {min-height: 10px;}
QScrollBar::handle:horizontal {min-width: 10px;}
QScrollBar::handle:hover {background: #4ab;}
QScrollBar::left-arrow, QScrollBar::right-arrow, QScrollBar::up-arrow,
QScrollBar::down-arrow, QScrollBar::sub-line, QScrollBar::add-line,
QScrollBar::add-page, QScrollBar::sub-page {background: #2e2e3e; height: 0; width: 0; border-radius: 0; border: 0;}''')


        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(4, 4, 4, 4)
        self.hl_top = QtWidgets.QHBoxLayout()
        self.hl_top.setContentsMargins(0, 0, 0, 0)
        self.hl_top.setSpacing(6)
        self.hl_top.setObjectName("hl_top")
        self.caption_widget = MyWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHeightForWidth(self.caption_widget.sizePolicy().hasHeightForWidth())
        self.hl_top.addWidget(self.caption_widget)

        self.l_menu = MyLabel({'default':labelstyle([":/images/menu.png",":/images/menu_over.png"])}, self.centralwidget)
        self.l_menu.setMinimumSize(QtCore.QSize(18, 18))
        self.l_menu.setMaximumSize(QtCore.QSize(18, 18))
        #self.l_menu.setStyleSheet("QLabel  {background:  url(\":/images/settings.png\") } QLabel:hover {background:  url(\":/images/settings_over.png\")}")
        self.l_menu.setText("")
        self.l_menu.setObjectName("l_menu")
        self.hl_top.addWidget(self.l_menu)
        self.lfullscreen = MyLabel({'default':labelstyle([":/images/fullscreen.png", ":/images/fullscreen_over.png"])}, self.centralwidget)
        self.lfullscreen.setMinimumSize(QtCore.QSize(18, 18))
        self.lfullscreen.setMaximumSize(QtCore.QSize(18, 18))
        #self.lfullscreen.setStyleSheet("QLabel  {background:  url(\":/images/fullscreen.png\") } QLabel:hover {background:  url(\":/images/fullscreen_over.png\")}")
        self.lfullscreen.setText("")
        self.lfullscreen.setObjectName("lfullscreen")
        self.hl_top.addWidget(self.lfullscreen)
        self.lclose = MyLabel({'default':labelstyle([":/images/close.png", ":/images/close_h.png"])}, self.centralwidget)
        #MyLabel([':/images/close.png', ':/images/close_h.png'], self.centralwidget)
        self.lclose.setMinimumSize(QtCore.QSize(18, 18))
        self.lclose.setMaximumSize(QtCore.QSize(18, 18))
        #self.lclose.setStyleSheet("QLabel  {background:  url(\":/images/close.png\") } QLabel:hover {background:  url(\":/images/close_h.png\")}")
        self.lclose.setText("")
        self.lclose.setObjectName("lclose")
        self.hl_top.addWidget(self.lclose)
        self.verticalLayout.addLayout(self.hl_top)

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.w_info = QtWidgets.QWidget(self.centralwidget)
        self.w_info.setMinimumSize(QtCore.QSize(0, 60))
        self.w_info.setMaximumSize(QtCore.QSize(374, 60))
        self.w_info.setStyleSheet("QWidget#w_info {\n"
"    background: qlineargradient(\n"
"x1: 0, y1: 0, x2: 0, y2: 1,\n"
"stop: 0 #98000004,stop: 0.1 #8805010a, stop: 0.46 #88303b60,\n"
"stop: 0.54 #88202a3e, stop: 0.9 #88101016, stop: 1.0 #98000009);\n"
"    border-style: inset;\n"
"    border-width: 1px;\n"
"    border-color: #a0404050;\n"
"    border-radius: 10px;}")
        self.w_info.setObjectName("w_info")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.w_info)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(5, 0, 0, 5)
        self.horizontalLayout.setSpacing(0)
        self.lState = QtWidgets.QLabel(self.w_info)
        self.lState.setMinimumSize(QtCore.QSize(24, 24))
        self.lState.setMaximumSize(QtCore.QSize(24, 24))
        self.lState.setStyleSheet("background: #00000000;")
        self.lState.setText("")
        self.lState.setPixmap(QtGui.QPixmap(":/images/stop_state.png"))
        self.lState.setObjectName("lState")
        self.horizontalLayout.addWidget(self.lState)

        self.vl_info_text = QtWidgets.QVBoxLayout()
        self.vl_info_text.setSpacing(0)
        self.vl_info_text.setObjectName("vl_info_text")
        self.vl_info_text.setContentsMargins(0, 0, 0, 0)
        self.vl_info_text.setSpacing(0)
        self.lFilename = QtWidgets.QLabel(self.w_info)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lFilename.sizePolicy().hasHeightForWidth())
        self.lFilename.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.lFilename.setFont(font)
        self.lFilename.setStyleSheet("background: #00000000;")
        self.lFilename.setText("")
        self.lFilename.setWordWrap(True)
        self.lFilename.setObjectName("lFilename")
        self.vl_info_text.addWidget(self.lFilename)
        self.l_time = QtWidgets.QLabel(self.w_info)
        self.l_time.setStyleSheet("color: #b2b2b2;")
        self.l_time.setText("0.00/0.00")
        self.l_time.setObjectName("l_time")
        self.vl_info_text.addWidget(self.l_time)
        self.horizontalLayout.addLayout(self.vl_info_text)
        self.horizontalLayout_2.addWidget(self.w_info)
        self.volume = MVolume(self.centralwidget)
        self.volume.beginUpdate()
        self.volume.setMinimumSize(QtCore.QSize(50, 50))
        self.volume.setMaximumSize(QtCore.QSize(50, 50))
        self.volume.setObjectName("volume")
        self.volume.setKnobBgImage(QtGui.QPixmap(":/images/knob_bg.png"))
        self.volume.setKnobImage(QtGui.QPixmap(":/images/knob_ind.png"))
        self.volume.endUpdate()
        self.horizontalLayout_2.addWidget(self.volume)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.w_track = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.w_track.sizePolicy().hasHeightForWidth())
        self.w_track.setSizePolicy(sizePolicy)
        self.w_track.setMinimumSize(QtCore.QSize(0, 14))
        self.w_track.setMaximumSize(QtCore.QSize(16777215, 14))
        self.w_track.setStyleSheet("QWidget#w_track {\n"
"    background: rgba(0, 0, 0, 60);\n"
"    border-style: inset;\n"
"    border-width: 1px;\n"
"    border-color: #445;\n"
"    border-radius: 7px\n"
"};")
        self.w_track.setObjectName("w_track")
        self.verticalLayout.addWidget(self.w_track)

        self.slider = MSlider()
        w_track_layout = QtWidgets.QHBoxLayout()
        w_track_layout.setContentsMargins(3, 3, 3, 3)
        w_track_layout.setSpacing(0)
        self.slider.fitHeight = True
        self.slider.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        w_track_layout.addWidget(self.slider)
        self.w_track.setLayout(w_track_layout)

        self.lo_buttons = QtWidgets.QHBoxLayout()
        self.lo_buttons.setObjectName("lo_buttons")

        self.lurl = MyLabel({'default':labelstyle([":/images/link.png", ":/images/link_over.png"])}, self.centralwidget)
        self.lurl.setMinimumSize(QtCore.QSize(34, 34))
        self.lurl.setMaximumSize(QtCore.QSize(34, 34))
        #self.lurl.setStyleSheet("QLabel  {background:  url(\":/images/link.png\") }\n"
        #"QLabel:hover {background:  url(\":/images/link_over.png\")}")
        self.lurl.setText("")

        self.lurl.setObjectName("lurl")
        self.lo_buttons.addWidget(self.lurl)

        self.lfolder = MyLabel({'default':labelstyle([':/images/folder.png', ':/images/folder_over.png'])}, self.centralwidget)
        self.lfolder.setMinimumSize(QtCore.QSize(34, 34))
        self.lfolder.setMaximumSize(QtCore.QSize(34, 34))
        #self.lfolder.setStyleSheet("QLabel  {background:  url(\":/images/folder.png\") }\n"
        #"QLabel:hover {background:  url(\":/images/folder_over.png\")}")
        self.lfolder.setText("")
        self.lfolder.setObjectName("lfolder")
        self.lo_buttons.addWidget(self.lfolder)

        self.button_widget = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_widget.sizePolicy().hasHeightForWidth())
        self.button_widget.setSizePolicy(sizePolicy)
        self.button_widget.setMinimumSize(QtCore.QSize(146, 45))
        self.button_widget.setStyleSheet("QWidget#button_widget {\n"
"    background: #131013;\n"
"    border-style: inset;\n"
"    border-width: 1px;\n"
"    border-color: #60404050;\n"
"    border-radius: 10px;}")
        self.button_widget.setObjectName("button_widget")

        self.lplay = MyLabel({'default':labelstyle([':/images/play.png', ':/images/play_over.png']), 'pressed':labelstyle([':/images/play_down.png'])}, self.button_widget)
        self.lplay.setGeometry(QtCore.QRect(0, 0, 60, 45))
        self.lplay.setMinimumSize(QtCore.QSize(60, 45))
        self.lplay.setMaximumSize(QtCore.QSize(1800, 1800))
        #self.lplay.setStyleSheet("QLabel  {background:  url(\":/images/play.png\") no-repeat center center }\n"
        #"QLabel:hover {background:  url(\":/images/play_over.png\") no-repeat center center}")
        self.lplay.setText("")
        self.lplay.setObjectName("lplay")
        self.lpause = MyLabel({'default':labelstyle([':/images/pause.png', ':/images/pause_over.png']), 'pressed':labelstyle([':/images/pause_down.png'])}, self.button_widget)
        self.lpause.setGeometry(QtCore.QRect(43, 0, 60, 45))
        self.lpause.setMinimumSize(QtCore.QSize(60, 45))
        self.lpause.setMaximumSize(QtCore.QSize(1800, 1800))
        #self.lpause.setStyleSheet("QLabel  {background:  url(\":/images/pause.png\") no-repeat center center }\n"
        #"QLabel:hover {background:  url(\":/images/pause_over.png\") no-repeat center center}")
        self.lpause.setText("")
        self.lpause.setObjectName("lpause")
        self.lstop = MyLabel({'default':labelstyle([':/images/stop.png', ':/images/stop_over.png']), 'pressed':labelstyle([':/images/stop_down.png'])}, self.button_widget)
        self.lstop.setGeometry(QtCore.QRect(86, 0, 60, 45))
        self.lstop.setMinimumSize(QtCore.QSize(60, 45))
        self.lstop.setMaximumSize(QtCore.QSize(1800, 1800))
        self.lstop.setStyleSheet("QLabel  {background:  url(\":/images/stop.png\") no-repeat center center }\n"
"QLabel:hover {background:  url(\":/images/stop_over.png\") no-repeat center center}")
        self.lstop.setText("")
        self.lstop.setObjectName("lstop")
        self.lo_buttons.addWidget(self.button_widget)
        self.l_playlist = MyLabel({'default':labelstyle([':/images/playlist_off.png', ':/images/playlist_off_over.png']),'checked':labelstyle([':/images/playlist.png', ':/images/playlist_over.png'])}, self.button_widget)
        self.l_playlist.checkable = True
        self.l_playlist.setMinimumSize(QtCore.QSize(34, 34))
        self.l_playlist.setMaximumSize(QtCore.QSize(34, 34))
        self.l_playlist.setText("")
        self.l_playlist.setObjectName("l_playlist")
        self.lo_buttons.addWidget(self.l_playlist)

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.lo_buttons.addItem(spacerItem)
        self.lo_speed = QtWidgets.QVBoxLayout()
        self.lo_speed.setSpacing(0)
        self.lo_speed.setObjectName("lo_speed")
        self.speed_slider = QtWidgets.QSlider(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.speed_slider.sizePolicy().hasHeightForWidth())
        self.speed_slider.setSizePolicy(sizePolicy)
        self.speed_slider.setMinimumSize(QtCore.QSize(80, 0))
        self.speed_slider.setMinimum(-4)
        self.speed_slider.setMaximum(4)
        self.speed_slider.setPageStep(2)
        self.speed_slider.setOrientation(QtCore.Qt.Horizontal)
        self.speed_slider.setTickInterval(1)
        self.speed_slider.setObjectName("speed_slider")
        if platform.system() == "Windows":
            self.speed_slider.setStyleSheet("QSlider::groove:horizontal {background: #233952;\n"
"    border-style: inset; border-width: 1px; border-color: #80031028; border-radius: 3px;margin: 9px 0px;}\n"
"QSlider::handle:horizontal {background-color: #c05070ff;border-style: inset;border-width: 1px;\n"
"    border-radius: 7px;height: 16px;width: 16px;margin: -6px 0px;}\n"
"QSlider::handle:horizontal:hover {background-color: #f010f5ff;}")

        self.lo_speed.addWidget(self.speed_slider)
        self.lspeed = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.lspeed.setFont(font)
        self.lspeed.setText("Speed: 1.0")
        self.lspeed.setAlignment(QtCore.Qt.AlignCenter)
        self.lspeed.setObjectName("lspeed")
        self.lo_speed.addWidget(self.lspeed)
        self.lo_buttons.addLayout(self.lo_speed)
        self.verticalLayout.addLayout(self.lo_buttons)

        self.playlist_widget = QtWidgets.QWidget(self.centralwidget)
        self.playlist_widget.setMinimumSize(QtCore.QSize(0, 150))
        self.playlist_widget.setStyleSheet("QWidget#playlist_widget {\n"
"    background: qlineargradient(\n"
"x1: 0, y1: 0, x2: 0, y2: 1,\n"
"stop: 0 #68000004,stop: 0.1 #5805010a, stop: 0.46 #88303b40,\n"
"stop: 0.54 #88202a3e, stop: 0.9 #48101016, stop: 1.0 #58000009);\n"
"    border-style: inset;\n"
"    border-width: 1px;\n"
"    border-color: #a0404050;\n"
"    border-radius: 4px;}")
        self.playlist_widget.setObjectName("playlist_widget")
        self.lo_playlist_widget = QtWidgets.QVBoxLayout(self.playlist_widget)
        self.lo_playlist_widget.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.lo_playlist_widget.setContentsMargins(0, 0, 0, 0)
        self.lo_playlist_widget.setSpacing(0)
        self.lo_playlist_widget.setObjectName("lo_playlist_widget")
        self.playlist_padding_widget = QtWidgets.QWidget(self.playlist_widget)
        self.playlist_padding_widget.setMinimumSize(QtCore.QSize(0, 2))
        self.playlist_padding_widget.setMaximumSize(QtCore.QSize(16777215, 2))
        self.playlist_padding_widget.setStyleSheet("background:transparent;")
        self.playlist_padding_widget.setObjectName("playlist_padding_widget")
        self.lo_playlist_widget.addWidget(self.playlist_padding_widget)
        self.hlo_playlist_widget = QtWidgets.QHBoxLayout()
        self.hlo_playlist_widget.setSpacing(4)
        self.hlo_playlist_widget.setObjectName("hlo_playlist_widget")
        self.lw = QtWidgets.QListWidget(self.playlist_widget)
        self.lw.setStyleSheet('''QListWidget {background: transparent; border-style: inset; border-width: 0px; border-radius: 6px;}
QListView::item:selected { background: rgba(0, 0, 0, 60); border-width: 1px; border-style: inset; border-color: #345; border-radius: 6px; color: #fff;}
QListView::item:focus { background: rgba(0, 30, 60, 90); border-width: 1px; border-style: inset; border-color: #345; border-radius: 6px;}
QListView::item:focus:hover { background: rgba(0, 30, 60, 90); color: #fff;}
QListView::item:hover { background: transparent; color: #eee;}
QListView::item:selected:hover {background: rgba(0, 0, 0, 60); color:  aqua;}''')
        self.lw.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.lw.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lw.setIconSize(QtCore.QSize(18, 18))
        self.lw.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.lw.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.lw.setObjectName("lw")
        self.hlo_playlist_widget.addWidget(self.lw)
        self.playlist_buttons_widget = QtWidgets.QWidget(self.playlist_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.playlist_buttons_widget.sizePolicy().hasHeightForWidth())
        self.playlist_buttons_widget.setSizePolicy(sizePolicy)
        self.playlist_buttons_widget.setMinimumSize(QtCore.QSize(26, 0))
        self.playlist_buttons_widget.setStyleSheet("QWidget#playlist_buttons_widget {background: transparent; border-style: inset; border-width: 0px; border-radius: 6px; }")
        self.playlist_buttons_widget.setObjectName("playlist_buttons_widget")
        self.lo_playlist_buttons_widget = QtWidgets.QVBoxLayout(self.playlist_buttons_widget)
        self.lo_playlist_buttons_widget.setContentsMargins(0, 0, 0, 0)
        self.lo_playlist_buttons_widget.setSpacing(2)
        self.lo_playlist_buttons_widget.setObjectName("lo_playlist_buttons_widget")
        self.l_add = MyLabel({'default':labelstyle([':/images/add.png', ':/images/add_h.png'])}, self.playlist_buttons_widget)
        self.l_add.setMinimumSize(QtCore.QSize(24, 24))
        self.l_add.setMaximumSize(QtCore.QSize(24, 24))
        self.l_add.setText("")
        self.l_add.setObjectName("l_add")
        self.lo_playlist_buttons_widget.addWidget(self.l_add)
        self.l_del = MyLabel({'default':labelstyle([':/images/del.png',':/images/del_h.png'])}, self.playlist_buttons_widget)
        self.l_del.setMinimumSize(QtCore.QSize(24, 24))
        self.l_del.setMaximumSize(QtCore.QSize(24, 24))
        self.l_del.setText("")
        self.l_del.setObjectName("l_del")
        self.lo_playlist_buttons_widget.addWidget(self.l_del)
        self.l_clear = MyLabel({'default':labelstyle([':/images/clear.png',':/images/clear_h.png'])}, self.playlist_buttons_widget)
        self.l_clear.setMinimumSize(QtCore.QSize(24, 24))
        self.l_clear.setMaximumSize(QtCore.QSize(24, 24))
        self.l_clear.setText("")
        self.l_clear.setObjectName("l_clear")
        self.lo_playlist_buttons_widget.addWidget(self.l_clear)
        spacerItem2 = QtWidgets.QSpacerItem(20, 43, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.lo_playlist_buttons_widget.addItem(spacerItem2)
        self.l_loop = MyLabel({}, self.playlist_buttons_widget)
        self.l_loop.setMinimumSize(QtCore.QSize(24, 24))
        self.l_loop.setMaximumSize(QtCore.QSize(24, 24))
        self.l_loop.setStyleSheet("QLabel  {background:  url(\":/images/loop_off.png\") center no-repeat ;}\n"
"QLabel:hover {background:  url(\":/images/loop_off_h.png\") center no-repeat;}")
        self.l_loop.setText("")
        self.l_loop.setObjectName("l_loop")
        self.lo_playlist_buttons_widget.addWidget(self.l_loop)
        self.hlo_playlist_widget.addWidget(self.playlist_buttons_widget)
        self.lo_playlist_widget.addLayout(self.hlo_playlist_widget)
        self.playlist_widget.setVisible(False)
        self.verticalLayout.addWidget(self.playlist_widget)


        spacerItem1 = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        self.lurl.setToolTip(tr("playurl"))
        self.lfolder.setToolTip(tr("openfile"))
        self.l_playlist.setToolTip(tr("playlist"))

import images_rc

