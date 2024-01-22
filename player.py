import os
import sys
from PyQt5 import QtCore
import vlc
#этот код надо оптимизировать, здесь есть над чем поработать
class Player(QtCore.QObject):
    #статические параметры
    STATE_STOP  = 0
    STATE_PLAY  = 1
    STATE_PAUSE = 2
    LOOP_TOEND = 0
    LOOP_REPEAT = 1
    #сигналы
    stateChanged = QtCore.pyqtSignal(int)
    volumeChanged = QtCore.pyqtSignal(int)
    positionChanged = QtCore.pyqtSignal(int)
    finished = QtCore.pyqtSignal()

    def __init__(self, maxpos = 1000):
        #maxpos это максимальная позиция контрола управления временем/позицией
        super(Player, self).__init__()
        self.instance = vlc.Instance()
        self.mediaplayer = self.instance.media_player_new()
        self.media = None
        self.state = self.STATE_STOP
        self.maxpos = maxpos
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.onTimer)
        self.volume = 100
        self.current_filename = ''
        self.pos = 0
        self.duration = 0
        self.timeduration = '0:00'

    def play(self, fn):
        if fn == None:
            self.stop()
            return -1
        if self.media != None:
            vlc.libvlc_media_release(self.media)
        self.media = self.instance.media_new(fn)
        self.mediaplayer.set_media(self.media)
        self.media.parse() #for getInfo
        r = self.play_pause()
        #Громкость всегда сбрасывается при создании нового media
        self.mediaplayer.audio_set_volume(self.volume)
        self.duration = self.getLength()
        self.timeduration = self.msecondsToTime(self.duration)
        if r == 1:
            self.current_filename = fn
        return r
        #self.playingFileChanged.emit()

    def getCurrentInfo(self):
        if self.media == None: return None
        return {'title':self.media.get_meta(vlc.Meta.Title),'album':self.media.get_meta(vlc.Meta.Album),'artist':self.media.get_meta(vlc.Meta.Artist)}

    def get_media_title(self):
        return self.media.get_meta(vlc.Meta.Title)

    def play_pause(self):
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()
            self.state = self.STATE_PAUSE
            self.stateChanged.emit(self.state)
            self.timer.stop()
            return 0
        else:
            if self.mediaplayer.play() == -1:
                #self.playCurrent()
                return -1

            self.state = self.STATE_PLAY
            self.stateChanged.emit(self.state)
            self.timer.start()
            return 1

    def stop(self):
        self.mediaplayer.stop()
        self.timer.stop()
        self.duration = 0
        self.timeduration = '0:00'
        if self.state != self.STATE_STOP:
            self.state = self.STATE_STOP
            self.stateChanged.emit(self.state)

    def set_volume(self, volume):
        self.volume = volume
        self.mediaplayer.audio_set_volume(volume)

    def set_position(self, pos):
        if self.state == self.STATE_STOP: return
        self.pos = pos
        #self.timer.stop()
        self.mediaplayer.set_position(pos / self.maxpos)
        #self.timer.start()

    def skip(self, sec):
        if self.state == self.STATE_STOP: return
        self.timer.stop()
        p = self.mediaplayer.get_position()
        l = vlc.libvlc_media_get_duration(self.media)
        p += 1/l*(sec*1000)
        self.mediaplayer.set_position(p)
        self.timer.start()


    def skip_b_min(self):
        self.skip(-15)

    def skip_b_mid(self):
        self.skip(-60)

    def skip_b_max(self):
        self.skip(-300)

    def skip_f_min(self):
        self.skip(15)

    def skip_f_mid(self):
        self.skip(60)

    def skip_f_max(self):
        self.skip(300)

    def onTimer(self):
        v = self.mediaplayer.audio_get_volume()
        if v != -1 and v != self.volume:
            self.volume = v
            self.volumeChanged.emit(v)
        #self.mediaplayer.get_position() =  от 0 до 1
        p = int(self.mediaplayer.get_position() * self.maxpos)
        if p < 0: p = 0
        #if p != self.pos:
        self.pos = p
        self.positionChanged.emit(p)

        if not self.mediaplayer.is_playing():
            self.timer.stop()
            if self.state == self.STATE_PLAY:
                self.stop()
                self.finished.emit()


    def getLength(self):
        return 0 if self.state == self.STATE_STOP else vlc.libvlc_media_get_duration(self.media)

    def msecondsToTime(self, ms):
        s = ms // 1000
        m = s // 60
        h = m // 60
        m %= 60
        s %= 60
        return f'{h:02d}:{m:02d}:{s:02d}' if h > 0 else f'{m:02d}:{s:02d}'

    def getTimePos(self):
        if self.state == self.STATE_STOP: return '0.00'
        p = self.mediaplayer.get_position()
        if p == 0: return '0.00'
        msec = round(p * self.duration)
        return self.msecondsToTime(msec)


    def getTimeDuration(self):
        return self.timeduration

    def getAudioTracks(self):
        if self.state == self.STATE_STOP: return []
        tracks = self.mediaplayer.audio_get_track_description()
        tr_lst = []
        if tracks != None:
            for tr in tracks:
                tr_lst.append((tr[0], tr[1].decode()))
        return tr_lst

    def getCurrentTrack(self):
        if self.state == self.STATE_STOP: return -1
        return self.mediaplayer.audio_get_track()

    def setCurrentTrack(self, track_id):
        if self.state == self.STATE_STOP: return
        self.mediaplayer.audio_set_track(track_id)

    def getSubtitles(self):
        if self.state == self.STATE_STOP: return []
        subtitles = self.mediaplayer.video_get_spu_description()
        st = []
        if subtitles != None:
            for s in subtitles:
                st.append((s[0], s[1].decode()))
        return st

    def getCurrentSubtitle(self):
        if self.state == self.STATE_STOP: return -1
        return self.mediaplayer.video_get_spu()

    def setCurrentSubtitle(self, sid):
        if self.state == self.STATE_STOP: return
        self.mediaplayer.video_set_spu(sid)


