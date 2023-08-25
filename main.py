from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QUrl, QTimer
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5 import QtGui, QtCore,QtTest
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from desktop_wid import Ui_Form as desktop_wid
import sys,os,random
from PyQt5.QtGui import QIcon
import eyed3



class Anaekran(QWidget):
        def __init__(self) -> None:
            super().__init__()
            self.ui = desktop_wid()
            self.ui.setupUi(self)
            width = 800
            height = 600
            screen = QApplication.primaryScreen()
            
            if screen is not None:
                screen_geometry = screen.geometry()
                x = screen_geometry.width() - width
                y = 0
                self.setGeometry(x, y, width, height)


            self.like_status = True
            self.shuffle_status = True
            self.stop_status = False

            self.player = QMediaPlayer(self)
            self.fayl_yolu = r'C:\Users\quliy\Documents\MusicLy\Defkhan-Esra-Yangin.mp3'
            file_name = os.path.basename(self.fayl_yolu)
            self.file_name = os.path.splitext(file_name)[0]

            if len(self.file_name) > 24:
                self.ui.music_name_max_24.setText(f'{self.file_name[:20]}..')
            else:
                self.ui.music_name_max_24.setText(self.file_name)

            print(self.fayl_yolu)
            print(self.uzunluq_al(self.fayl_yolu))

            self.ui.end_duration.setText(str(self.format_seconds(self.uzunluq_al(self.fayl_yolu))))
            
        
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.fayl_yolu)))

            self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnBottomHint)
            self.setAttribute(Qt.WA_TranslucentBackground)
            self.background_timer = QTimer(self)
            self.background_timer.timeout.connect(self.bg_change)
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_current_time)
            self.ui.music_slider.setMaximum(int(self.uzunluq_al(self.fayl_yolu)))
            self.ui.sag_btn.pressed.connect(self.sag_icon_tiklanma)
            self.ui.sol_btn.pressed.connect(self.sol_icon_tiklanma)
            self.ui.like_btn.pressed.connect(self.like_tiklanma)
            self.ui.random_shuffle_btn.pressed.connect(self.shuffle_tiklanma)
            self.ui.pause_stop_btn.pressed.connect(self.pause_stop_tiklanma)
            self.ui.exit_button.clicked.connect(self.exitApplication)
            self.ui.music_slider.valueChanged.connect(self.slider_value_changed)
            

        def bg_change(self):
            bgs = [':/images/main/img1.png',':/images/main/img2.jpg',':/images/main/img2.png']
            self.ui.background_label.setStyleSheet(f'border-image: url({random.choice(bgs)});\nborder-radius:30px;')
        def uzunluq_al(self,file_path):
            audiofile = eyed3.load(file_path)
            if audiofile is not None and audiofile.info.time_secs:
                return int(audiofile.info.time_secs)
            else:
                return None

        def format_seconds(self,seconds):
            minutes = seconds // 60
            seconds %= 60
            return f"{minutes:02d}:{seconds:02d}"
        

        def slider_value_changed(self):
            self.sld_value = int(self.ui.music_slider.value())
            if self.sld_value - self.old_sld_value > 1:
                self.player.setPosition(self.sld_value*1000)
            elif self.sld_value - self.old_sld_value < -1:
                negative_interval = int(self.sld_value - self.old_sld_value)
                print(negative_interval)
                self.player.setPosition(abs((self.sld_value + negative_interval)*1000))



        
        def exitApplication(self):
            QApplication.quit()


        def update_current_time(self):
            if self.player.state() == QMediaPlayer.PlayingState:
                current_seconds = self.player.position() / 1000
                update_sec = str(self.format_seconds(int(current_seconds)))
                print(update_sec)
                self.ui.current_duration.setText(update_sec)
                self.ui.music_slider.setValue(int(current_seconds))
                self.old_sld_value = int(current_seconds)



        def sag_icon_tiklanma(self):
            self.ui.sag_btn.setIcon(QIcon(':/icons/main/back_icon_clicked.png'))
            QtTest.QTest.qWait(50)
            self.ui.sag_btn.setIcon(QIcon(':/icons/main/next_icon.png'))





        def sol_icon_tiklanma(self):
            self.ui.sol_btn.setIcon(QIcon(':/icons/main/next_icon_clicked.png'))
            QtTest.QTest.qWait(50)
            self.ui.sol_btn.setIcon(QIcon(':/icons/main/back_icon.png'))





        def pause_stop_tiklanma(self):
            if self.player.state() == QMediaPlayer.PlayingState:
                self.ui.pause_stop_btn.setIcon(QIcon(':/icons/main/play_button.png'))
                self.player.pause()
                self.timer.stop()
            else:
                self.ui.pause_stop_btn.setIcon(QIcon(':/icons/main/stop_button.png'))
                self.player.play()
                self.timer.start(1000)
                self.background_timer.start(3000)




        def like_tiklanma(self):
            if self.like_status:
                  self.like_status = False
                  self.ui.like_btn.setIcon(QIcon(':/icons/main/heart_clicked.png'))
            else:
                self.like_status = True
                self.ui.like_btn.setIcon(QIcon(':/icons/main/heart_icon.png'))
        
        
        



        def shuffle_tiklanma(self):
            if self.shuffle_status:
                self.shuffle_status = False
                self.ui.random_shuffle_btn.setIcon(QIcon(':/icons/main/repeat_icon.png'))
            else:
                self.shuffle_status = True
                self.ui.random_shuffle_btn.setIcon(QIcon(':/icons/main/shuffle_icon.png'))
       
        



app = QApplication([])
ekran = Anaekran()
ekran.show()
app.exec_()