#!/usr/bin/python3
#https://videolan.videolan.me/vlc/group__libvlc__video.html
import os
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from mainwindowui import Ui_MainWindow
from player import Player
from videowindow import DisplayWindow
from settings import SettingsDialog
from lang import tr

speed_values = [0.125, 0.25, 0.5, 0.75, 1, 1.5, 2, 4, 8]
LOOP_NONE = 0
LOOP_ONE = 1
LOOP_LOOP = 2

class Action(QtWidgets.QAction):
    action_triggered = QtCore.pyqtSignal(QtWidgets.QAction)

    def __init__(self, title, track_id):
        super(Action, self).__init__(title)
        self.track_id = track_id
        self.triggered.connect(self.clicked)

    def clicked(self):
        self.action_triggered.emit(self)


class VideoPlayer(QtWidgets.QMainWindow):
    def __init__(self, qApp):
        super(VideoPlayer, self).__init__()
        self.qApp = qApp
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        sets = QtCore.QSettings(os.path.join('RoganovSoft', 'VideoPlayer'),'config')
        sets.beginGroup('mainwindow')
        x = int(sets.value('pos.x', '-1'))
        y = int(sets.value('pos.y', '-1'))
        sets.endGroup()
        self.lastdir = os.path.expanduser('~')
        if x > -1 and y > -1:
            self.move(x, y)
        else:
            rect = QtWidgets.QApplication.desktop().screen().rect()
            x = (rect.width() - self.width()) // 2
            y = (rect.height() - self.height()) // 2
            self.move(x, y)

        self.ui.lclose.clicked.connect(self.close)
        self.ui.caption_widget.caption = 'VIDEO PLAYER'
        self.vol = self.ui.volume
        self.vol.setPos(int(sets.value("AUDIO/volume", 100)))
        self.slider = self.ui.slider
        self.display_index = int(sets.value('VIDEO/display_index', '-1'))
        #print('dislplay index', self.display_index)
        self.full_screen = sets.value('VIDEO/full_screen', '0') == '1'
        #print('full_screen', self.full_screen)
        if self.display_index >= len(qApp.screens()):
            self.display_index = 0
        #for scr in qApp.screens():
        #    g = scr.geometry()
        #    print(scr.model(), f'{g.width()}X{g.height()}')
        self.videowindow = None
        #DisplayWindow(qApp,  self.display_index)

        self.player = Player()
        self.player.stateChanged.connect(self.onPlayerStateChanged)
        self.player.volumeChanged.connect(self.vol.setPos)
        self.player.positionChanged.connect(self.playerPosChanged)
        self.player.finished.connect(self.playerfinished)
        self.player.set_volume(self.vol.position)

        #self.videowindow.setPlayer(self.player)
        #self.setVideoWindow()

        self.vol.posChanged.connect(self.player.set_volume)
        self.slider.posChanged.connect(self.onSliderPosChanged)
        self.ui.lplay.clicked.connect(self.playclick)
        self.ui.lstop.clicked.connect(self.player.stop)
        self.ui.lpause.clicked.connect(self.pauseclick)
        self.ui.lfolder.clicked.connect(self.openfile)
        self.ui.lurl.clicked.connect(self.openurl)
        self.ui.lfullscreen.clicked.connect(self.fullscreenchange)# self.videowindow.fullscreenchange)
        #self.ui.lsettings.clicked.connect(self.showsettings)
        self.ui.l_menu.clicked.connect(self.showmenu)
        self.ui.l_playlist.clicked.connect(self.showplaylist)
        self.ui.l_loop.clicked.connect(self.set_loop)
        self.ui.l_add.clicked.connect(self.add_filename)
        self.ui.lw.doubleClicked.connect(self.lwdoubleclick)
        self.ui.l_clear.clicked.connect(self.ui.lw.clear)
        self.ui.l_del.clicked.connect(self.del_filename)

        self.ui.speed_slider.valueChanged.connect(self.set_speed)
        self.ui.speed_slider.setFocusPolicy(QtCore.Qt.NoFocus)
        self.looping = LOOP_NONE
        #self.ui.speed_slider.setStyleSheet('background: border: 3px solid #fff;')
        if len(sys.argv) > 1:
            if os.path.isfile(sys.argv[1]):
                item = QtWidgets.QListWidgetItem(os.path.basename(sys.argv[1]))
                item.filename = sys.argv[1]
                self.ui.lw.addItem(item)
                self.playfile(sys.argv[1])

    def fullscreenchange(self):
        if self.videowindow != None and self.player.state != Player.STATE_STOP:
            self.full_screen = not self.videowindow.isfullscreen
            self.videowindow.fullscreenchange()


    def onPlayerStateChanged(self, state):
        if state == Player.STATE_STOP:
            self.ui.lState.setPixmap(QtGui.QPixmap(':/images/stop_state.png'))
            self.slider.posChange(0)
            self.timeChange()
            self.duration = 0
            if self.videowindow != None:
                self.full_screen = self.videowindow.isfullscreen
                self.videowindow.close()
                self.videowindow = None
        elif state == Player.STATE_PLAY:
            self.ui.lState.setPixmap(QtGui.QPixmap(':/images/play_state.png'))
        elif state == Player.STATE_PAUSE:
            self.ui.lState.setPixmap(QtGui.QPixmap(':/images/pause_state.png'))

    def playerPosChanged(self, pos):
        self.slider.posChange(pos)
        self.timeChange()

    def onSliderPosChanged(self, pos):
        self.player.set_position(pos)
        self.timeChange()

    def timeChange(self):
        self.ui.l_time.setText(self.player.getTimePos()+' / '+self.player.getTimeDuration())

    def playclick(self):
        if self.player.media == None:
            return
        if self.player.state == Player.STATE_STOP:
            if self.videowindow != None:
                self.videowindow.close()
            self.videowindow = DisplayWindow(self.qApp, self.player, self.display_index)
            if self.player.play_pause() == 1:
                self.videowindow.showvideowindow(self.full_screen, self.display_index)

        elif self.player.state == Player.STATE_PAUSE:
            self.player.play_pause()


    def pauseclick(self):
        if self.player.mediaplayer.is_playing():
            self.player.play_pause()

    def playfile(self, fn):
        self.ui.speed_slider.setValue(0)
        if self.videowindow != None:
            self.videowindow.close()
        self.videowindow = DisplayWindow(self.qApp, self.player, self.display_index)
        if self.player.play(fn) == 1:
            self.videowindow.showvideowindow(self.full_screen, self.display_index)
        self.ui.lFilename.setText(self.player.get_media_title())

    def openfile(self):

        fn, ext = QtWidgets.QFileDialog.getOpenFileName(self, tr('openvideofile'), self.lastdir, filter='Video files (*.avi *.mkv *.mp4 *.flv *.mov *.wmv *.3gp *.webm);;Playlist (*.m3u)')
        if len(fn) == 0:
            return
        self.lastdir = os.path.dirname(fn)
        if 'Playlist' in ext:
            lines = []
            self.ui.lw.clear()
            with open(fn) as f:
                lines = f.readlines()
            if lines[0].replace('\n','') == '#EXTM3U':
                i = 1
                while i < len(lines):
                    line = lines[i]
                    if line[:8] == '#EXTINF:':
                        p = line.index(',')
                        if p > 0:
                            title = line[p+1:].replace('\n','')
                            if len(title) < 2:
                                title = lines[i+1].replace('\n','')
                            fn = lines[i+1].replace('\n','')
                            i += 1
                            item = QtWidgets.QListWidgetItem(title)
                            item.filename = fn
                            self.ui.lw.addItem(item)

                    i += 1
        else:
            item = QtWidgets.QListWidgetItem(os.path.basename(fn))
            item.filename = fn
            self.ui.lw.clear()
            self.ui.lw.addItem(item)
            self.playfile(fn)

    def openurl(self):
        text, ok = QtWidgets.QInputDialog.getText(self,tr('playurl'), tr('enterlink'))
        if ok and len(text) > 3:
            self.playfile(text)

    def showsettings(self):
        dlg = SettingsDialog(self)
        dlg.ui.cbMonitor.setCurrentIndex(self.display_index+1)
        dlg.ui.cb_fullscreen.setChecked(self.full_screen)
        if dlg.exec() == 1:
            self.display_index = dlg.ui.cbMonitor.currentIndex()-1
            self.full_screen = dlg.ui.cb_fullscreen.isChecked()

    def showmenu(self):
        menu = QtWidgets.QMenu(self)
        settings_action = QtWidgets.QAction(tr("settings"))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/settings.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        settings_action.setIcon(icon)
        settings_action.triggered.connect(self.showsettings)
        if self.player.state != Player.STATE_STOP:
            tracks = self.player.getAudioTracks()
            current = self.player.getCurrentTrack()
            track_menu = menu.addMenu(tr('audiotrack'))
            trackicon = QtGui.QIcon()
            trackicon.addPixmap(QtGui.QPixmap(":/images/audiotrack.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            track_menu.setIcon(trackicon)
            track_actions = []
            for track in tracks:
                track_actions.append(Action(track[1], track[0]))
                i = len(track_actions)-1
                track_actions[i].setCheckable(True)
                if track[0] == current:
                    track_actions[i].setChecked(True)
                track_actions[i].action_triggered.connect(self.setAudioTrack)
                track_menu.addAction(track_actions[i])
            subtitles = self.player.getSubtitles()
            if len(subtitles) > 0:
                currentsubtitle = self.player.getCurrentSubtitle()
                subtitles_menu =  menu.addMenu(tr("subtitles"))
                subtitlesicon = QtGui.QIcon()
                subtitlesicon.addPixmap(QtGui.QPixmap(":/images/subtitles.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                subtitles_menu.setIcon(subtitlesicon)
                s_acts = []
                for sub in subtitles:
                    s_acts.append(Action(sub[1], sub[0]))
                    i = len(s_acts)-1
                    s_acts[i].setCheckable(True)
                    if sub[0] == currentsubtitle:
                        s_acts[i].setChecked(True)
                    s_acts[i].action_triggered.connect(self.setSubtitle)
                    subtitles_menu.addAction(s_acts[i])

                menu.addMenu(subtitles_menu)
            menu.addSection("")
        menu.addAction(settings_action)
        menu.exec_(self.ui.l_menu.mapToGlobal(QtCore.QPoint(-120,20)))


    def setSubtitle(self, action):
        self.player.setCurrentSubtitle(action.track_id)

    def setAudioTrack(self, action):
        self.player.setCurrentTrack(action.track_id)

    def set_speed(self, value):
        if self.player.media == None: return None
        pos = value+4
        self.player.mediaplayer.set_rate(speed_values[pos])
        self.ui.lspeed.setText(f'Speed: {speed_values[pos]}')

    def showplaylist(self):
        if self.ui.playlist_widget.isVisible():
            self.ui.playlist_widget.setVisible(False)
            QtCore.QTimer.singleShot(10, lambda:self.resize(359, 163))
        else:
            self.resize(359, 314)
            self.ui.playlist_widget.setVisible(True)

    def set_loop(self):
        if self.looping == LOOP_NONE:
            self.looping = LOOP_ONE
            self.ui.l_loop.setStyleSheet("QLabel  {background:  url(\":/images/loop_one.png\") center no-repeat ;}\n"
"QLabel:hover {background:  url(\":/images/loop_one_h.png\") center no-repeat;}")
        elif self.looping == LOOP_ONE:
            self.looping = LOOP_LOOP
            self.ui.l_loop.setStyleSheet("QLabel  {background:  url(\":/images/loop.png\") center no-repeat ;}\n"
"QLabel:hover {background:  url(\":/images/loop_h.png\") center no-repeat;}")
        else:
            self.ui.l_loop.setStyleSheet("QLabel  {background:  url(\":/images/loop_off.png\") center no-repeat ;}\n"
"QLabel:hover {background:  url(\":/images/loop_off_h.png\") center no-repeat;}")
            self.looping = LOOP_NONE

    def lwdoubleclick(self):
        i = self.ui.lw.currentRow()
        if i < 0: return
        fn = self.ui.lw.item(i).filename
        self.playfile(fn)

    def playerfinished(self):
        if self.looping == LOOP_NONE: return
        fn = self.player.current_filename
        if self.ui.lw.count() > 0:
            for i in range(self.ui.lw.count()):
                if self.ui.lw.item(i).filename == fn:
                    if i < self.ui.lw.count() -1:
                        y = i+1
                    elif self.looping == LOOP_ONE:
                        return
                    else:
                        y = 0
                    fn = self.ui.lw.item(y).filename
                    self.ui.lw.setCurrentRow(y)
                    self.playfile(fn)
                    return
            if self.looping == LOOP_ONE:
                return
            else:
                fn = self.ui.lw.item(0).filename
        self.playfile(fn)

    def add_filename(self):
        files, ext = QtWidgets.QFileDialog.getOpenFileNames(self, tr('openvideofiles'), self.lastdir, filter='Video files (*.avi *.mkv *.mp4 *.flv *.mov *.wmv *.3gp *.webm)')
        if len(files) == 0: return
        self.lastdir = os.path.dirname(files[0])
        for fn in files:
            item = QtWidgets.QListWidgetItem(os.path.basename(fn))
            item.filename = fn
            self.ui.lw.addItem(item)

    def del_filename(self):
        i = self.ui.lw.currentRow()
        if i >= 0:
            it = self.ui.lw.takeItem(i)
            del it

    def closeEvent(self, event):
        sets = QtCore.QSettings(os.path.join('RoganovSoft', 'VideoPlayer'),'config')
        sets.beginGroup('mainwindow')
        sets.setValue('pos.x',self.pos().x())
        sets.setValue('pos.y',self.pos().y())
        sets.endGroup()
        sets.setValue("AUDIO/volume", self.vol.position)
        sets.setValue('VIDEO/display_index', self.display_index)
        sets.setValue('VIDEO/full_screen', '1' if self.full_screen else '0')
        if self.videowindow != None:
            self.videowindow.close()
        if __name__ == '__main__':
            self.qApp.quit()

def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(":/images/icon.png"))
    #app.setDesktopSettingsAware(False)
    #themedir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'darktheme')
    #fn = os.path.join(themedir,'theme.qrc')
    #if os.path.isfile(fn):
    #    with open(fn, 'r') as f:
    #        theme = f.read()
    #    theme = theme.replace('current_directory',themedir)
    #    app.setStyleSheet(theme)
    mainwindow = VideoPlayer(app)
    app.mainwindow = mainwindow
    mainwindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
