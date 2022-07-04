from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QTabWidget, QFrame, QGridLayout, QVBoxLayout, QSpacerItem
from PyQt5.QtWidgets import QHBoxLayout, QListWidget, QCommandLinkButton
from PyQt5.QtGui import QIcon, QCursor, QFont, QFontDatabase
from PyQt5.QtCore import Qt, QSize, QTimer
from time import tzname, strftime, timezone
from datetime import date
import sys
import os
from webbrowser import WindowsDefault
from winsound import Beep


def resource_path(path):
    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.abspath('.')

    return os.path.join(base_path, path)


class Timer:
    def __init__(self, time) -> None:
        self.second = time.split(':')[0]
        self.minute = time.split(':')[1]
        self.hour = time.split(':')[2]

    def get_digits(self, number):
        if len(number) == 1:
            return '0' + number
        return number

    def add_second(self):
        if int(self.second) != 59:
            self.second = self.get_digits(str(int(self.second) + 1))
        else:
            if int(self.minute) != 59:
                self.minute = self.get_digits(str(int(self.minute) + 1))
                self.second = '00'
            else:
                self.hour = self.get_digits(str(int(self.hour) + 1))
                self.minute = '00'
                self.second = '00'

    def get_time(self):
        self.add_second()
        return ':'.join([self.hour, self.minute, self.second])

    def __repr__(self) -> str:
        return ':'.join([self.hour, self.minute, self.second])

    def __str__(self) -> str:
        return ':'.join([self.hour, self.minute, self.second])


class CDTimer:
    def __init__(self, time) -> None:
        self.time = list(time)
        self.current_index = -1

        self.time.remove(':')
        self.time.remove(':')

    def get_digits(self, number):
        if len(number) == 1:
            return '0' + number
        return number

    def add_number(self, number):
        if self.current_index > -7:
            for i in range(5):
                self.time[i] = self.time[i+1]
            self.time[-1] = number
            self.current_index -= 1

        result = ''.join(self.time)
        result = result[:2] + ':' + result[2:4] + ':' + result[4:6]
        return result

    def delete_last_number(self):
        for i in range(-1, -7, -1):
            if i == -6:
                self.time[i] = '0'
            else:
                self.time[i] = self.time[i-1]
        self.current_index += 1

        result = ''.join(self.time)
        result = result[:2] + ':' + result[2:4] + ':' + result[4:6]
        return result

    def correct_time(self):
        second = int(''.join(self.time[4:6]))
        minute = int(''.join(self.time[2:4]))
        hour = int(''.join(self.time[0:2]))

        if second > 59:
            second = self.get_digits(str(second - 60))
            self.time[4], self.time[5] = second[0], second[1]

            minute += 1
            minute = self.get_digits(str(minute))
            self.time[2], self.time[3] = minute[0], minute[1]

        minute = int(minute)
        if minute > 59:
            minute = self.get_digits(str(minute - 60))
            self.time[2], self.time[3] = minute[0], minute[1]

            hour += 1
            hour = self.get_digits(str(hour))
            self.time[0], self.time[1] = hour[0], hour[1]

        result = ''.join(self.time)
        result = result[:2] + ':' + result[2:4] + ':' + result[4:6]
        return result

    def reduce_second(self):
        second = ''.join(self.time[4:6])
        minute = ''.join(self.time[2:4])
        hour = ''.join(self.time[0:2])

        if int(second) != 0:
            second = self.get_digits(str(int(second) - 1))
        else:
            if int(minute) != 0:
                minute = self.get_digits(str(int(minute) - 1))
                second = '59'
            else:
                hour = self.get_digits(str(int(hour) - 1))
                minute = '59'
                second = '59'

        self.time[0], self.time[1] = hour[0], hour[1]
        self.time[2], self.time[3] = minute[0], minute[1]
        self.time[4], self.time[5] = second[0], second[1]

        result = ''.join(self.time)
        result = result[:2] + ':' + result[2:4] + ':' + result[4:6]
        return result

    def __str__(self) -> str:
        result = ''.join(self.time)
        result = result[:2] + ':' + result[2:4] + ':' + result[4:6]
        return result

    def __repr__(self) -> str:
        result = ''.join(self.time)
        result = result[:2] + ':' + result[2:4] + ':' + result[4:6]
        return result

    def __sub__(self, other):
        time_first = list(map(int, str(self).split(':')))
        sum_seconds_first = (
            (time_first[0] * 60) + (time_first[1])) * 60 + time_first[2]

        time_last = list(map(int, str(other).split(':')))
        sum_seconds_last = (
            (time_last[0] * 60) + (time_last[1])) * 60 + time_last[2]

        result_by_second = sum_seconds_first - sum_seconds_last

        hour = result_by_second // 3600
        minute = (result_by_second - hour * 3600) // 60
        second = result_by_second - (hour * 3600 + minute * 60)

        return ':'.join([self.get_digits(str(hour)), self.get_digits(str(minute)), self.get_digits(str(second))])


class TimeManager(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.window()
        self.make_tabs()
        self.make_time_frame()
        self.make_timer_frame()
        self.make_cd_timer_frame()

    def window(self):
        self.setFixedSize(600, 600)
        self.setWindowTitle('ART Time Manager')
        self.setWindowIcon(QIcon(resource_path('media/logo.png')))
        self.setStyleSheet(
            'background-color: #181818; font-family: Myriad Pro;')

        self.main_grid = QGridLayout(self)

    def make_tabs(self):
        self.tabs = QTabWidget(self)
        self.tabs.setStyleSheet(
            '''QTabWidget::pane {border: 0px solid gray;}
            QTabBar::Tab {background-color: #303030; min-width: 110px; min-height: 45px;
            padding-left: 78px; border: 1px solid gray;}
            QTabBar::Tab:Hover {background-color: #1f1f1f;}
            QTabBar::Tab:Selected {background-color: #1f1f1f; border-bottom: 0px}''')
        self.tabs.tabBar().setCursor(QCursor(Qt.PointingHandCursor))
        self.tabs.setIconSize(QSize(35, 35))

        frame_style = '''QFrame {background-color: #1f1f1f; font-family: Myriad Pro; border-top: 0px solid gray;
                        border-right: 1px solid gray; border-left: 1px solid gray; border-bottom: 1px solid gray;}'''

        self.timer_frame = QFrame(self)
        self.timer_frame.setFixedSize(570, 520)
        self.timer_frame.setStyleSheet(frame_style)

        self.time_frame = QFrame(self)
        self.time_frame.setFixedSize(570, 520)
        self.time_frame.setStyleSheet(frame_style)

        self.cd_timer_frame = QFrame(self)
        self.cd_timer_frame.setFixedSize(570, 520)
        self.cd_timer_frame.setStyleSheet(frame_style)

        self.tabs.addTab(self.timer_frame, QIcon(
            resource_path('media/timer.png')), '')
        self.tabs.addTab(self.time_frame, QIcon(
            resource_path('media/time.png')), '')
        self.tabs.addTab(self.cd_timer_frame, QIcon(
            resource_path('media/countdown_timer.png')), '')

        self.tabs.setTabToolTip(0, '<b> Timer <\b>')
        self.tabs.setTabToolTip(1, '<b> Now Time <\b>')
        self.tabs.setTabToolTip(2, '<b> CountDown Timer <\b>')

        self.main_grid.addWidget(self.tabs, 0, 0)
        self.tabs.setCurrentIndex(1)

    def make_time_frame(self):
        self.time_frame_grid = QGridLayout(self.time_frame)
        self.time_frame_grid.addItem(QSpacerItem(500, 80), 0, 0)

        vbox = QVBoxLayout(self.time_frame)
        vbox.setAlignment(Qt.AlignCenter)
        vbox.setSpacing(15)

        self.lb_now_time = QLabel(self.time_frame)
        self.lb_now_time.setStyleSheet('''QLabel {border: 0px; background-color: rgba(0, 0, 0, 0); color: white;
                                        font-family: Myriad Pro; font-size: 80px;}''')
        self.lb_now_time.setCursor(QCursor(Qt.IBeamCursor))
        self.lb_now_time.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.lb_now_time.setText(strftime('%H:%M  %p'))
        self.lb_now_time.setToolTip('<b> Now Time <\b>')
        vbox.addWidget(self.lb_now_time, 1, Qt.AlignCenter)

        timer = QTimer(self)
        timer.timeout.connect(
            lambda: self.lb_now_time.setText(strftime('%H:%M  %p')))

        ##########################################################

        self.lb_date = QLabel(self.time_frame)
        self.lb_date.setStyleSheet('''QLabel {border: 0px; background-color: rgba(0, 0, 0, 0); color: white;
                                        font-family: Myriad Pro; font-size: 40px;}''')
        self.lb_date.setText(date.today().strftime('%Y/%m/%d %a'))
        self.lb_date.setCursor(QCursor(Qt.IBeamCursor))
        self.lb_date.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.lb_date.setToolTip('<b> Date <\b>')
        vbox.addWidget(self.lb_date, 1, Qt.AlignCenter)

        self.lb_timezone = QLabel(self.time_frame)
        self.lb_timezone.setStyleSheet('''QLabel {border: 0px; background-color: rgba(0, 0, 0, 0); color: gray;
                                        font-family: Myriad Pro; font-size: 30px;}''')
        self.lb_timezone.setText(
            tzname[0].split(' ')[0] + ' ( ' + str(timezone / 3600) + ' )')
        self.lb_timezone.setCursor(QCursor(Qt.IBeamCursor))
        self.lb_timezone.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.lb_timezone.setToolTip('<b> Your Time Zone <\b>')
        vbox.addWidget(self.lb_timezone, 1, Qt.AlignCenter)

        self.about_btn = QPushButton(self.time_frame)
        self.about_btn.setStyleSheet('''QPushButton {background-color: #232323; color: #fbd0d0;
                                        font-family: Myriad Pro; font-size: 20pt; border-radius: 25px;}
                                        QPushButton::Hover {background-color: #303030;}
                                        QPushButton::Pressed {background-color: #303030;}''')
        self.about_btn.setIcon(QIcon(resource_path('media/about.png')))
        self.about_btn.setIconSize(QSize(50, 50))
        self.about_btn.clicked.connect(self.make_about)
        self.about_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.about_btn.setToolTip('<b> About Us <\b>')

        vbox.addSpacerItem(QSpacerItem(400, 200))
        vbox.addWidget(self.about_btn, 1, Qt.AlignCenter)

        self.time_frame_grid.addLayout(vbox, 1, 0, Qt.AlignCenter)
        timer.start(1000)

    def make_timer_frame(self):
        self.timer_frame_grid = QGridLayout(self.timer_frame)
        self.timer_frame_grid.addItem(
            QSpacerItem(500, 15))

        self.btn_timer = QPushButton(self.timer_frame)
        self.btn_timer.setText('00:00:00')
        self.btn_timer.setMinimumSize(250, 250)
        self.btn_timer.setCursor(Qt.PointingHandCursor)
        self.btn_timer.setToolTip('<b> Click To Start Or Stop <\b>')
        self.btn_timer.setStyleSheet(
            '''QPushButton {background-color: rgba(0,0,0,0); border: 5px solid gray; border-radius: 125px;
                font-family: Myriad Pro; font-size: 35px; color: white;}
                QPushButton::Hover {color: #FF9F9F; border: 5px solid #FF9F9F;}
                QPushButton::pressed {color: #D20000; border: 5px solid #D20000;}''')

        self.time = Timer('00:00:00')
        timer = QTimer(self.timer_frame)
        timer.timeout.connect(
            lambda: self.btn_timer.setText(self.time.get_time() + '\nStop'))
        self.time_enabled = False

        def start_stop_timer():
            if str(self.time) == '00:00:00' or self.time_enabled == False:
                self.btn_timer.setStyleSheet(self.btn_timer.styleSheet() +
                                             'QPushButton {color: white; border: 5px solid gray;}')
                timer.start(1000)
                self.btn_timer.setText(self.btn_timer.text().split('\n')[
                                       0] + '\nStop')
                self.time_enabled = True
            else:
                timer.stop()
                self.btn_timer.setStyleSheet(self.btn_timer.styleSheet() +
                                             'QPushButton {color: #FF9F9F; border: 5px solid #FF9F9F;}')
                self.btn_timer.setText(
                    self.btn_timer.text().split('\n')[0] + '\nStart')
                self.time_enabled = False

        self.btn_timer.clicked.connect(start_stop_timer)

        ###########################################################
        self.records_list = QListWidget()
        self.records_list.setStyleSheet(
            '''QListWidget {background-color: rgba(0,0,0,0); border: 0px;}
                QListWidget::Item {background-color: #303030; color: white; border: 1px solid black;}
                QListWidget::Item:Hover {background-color: white; color: black; font-size: 12pt;}
                QListWidget QScrollBar {background-color: white; width: 7px;}
                QListWidget QScrollBar::Handle {background-color: gray;}''')
        self.records_list.setMinimumSize(200, 110)
        self.records_list.setFont(QFont('Myriad Pro', 10))
        self.records_list.setCursor(Qt.PointingHandCursor)

        btn_style = '''QPushButton {background-color: rgba(0,0,0,0);}
                        QPushButton::Hover {background-color: #181818;}
                        QPushButton::pressed {background-color: #181818;}'''

        def clear():
            timer.stop()
            self.records_list.clear()
            self.time = Timer("00:00:00")
            self.btn_timer.setText("00:00:00")

            self.records_list.hide()
            self.timer_frame_grid.removeWidget(self.records_list)

            self.btn_timer.setStyleSheet(self.btn_timer.styleSheet() +
                                         'QPushButton {color: white; border: 5px solid gray;}')

        def add_record():
            self.records_list.setParent(self.timer_frame)
            self.records_list.show()
            self.timer_frame_grid.addWidget(
                self.records_list, 3, 0, Qt.AlignCenter)

            text = self.btn_timer.text().split('\n')[0]
            number = self.records_list.count() + 1
            self.records_list.addItem('Record ' + str(number) + '\t\t' + text)
            item = self.records_list.item(self.records_list.count()-1)
            item.setToolTip(item.text())

        self.btn_timer_clear = QPushButton(self.timer_frame)
        self.btn_timer_clear.setIcon(
            QIcon(resource_path('media/trash_bin.png')))
        self.btn_timer_clear.setStyleSheet(btn_style)
        self.btn_timer_clear.setIconSize(QSize(50, 50))
        self.btn_timer_clear.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_timer_clear.clicked.connect(clear)
        self.btn_timer_clear.setToolTip('<b> Clear Timer <\b>')

        self.btn_timer_record = QPushButton(self.timer_frame)
        self.btn_timer_record.setIcon(
            QIcon(resource_path('media/time_tracking.png')))
        self.btn_timer_record.setStyleSheet(btn_style)
        self.btn_timer_record.setIconSize(QSize(60, 60))
        self.btn_timer_record.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_timer_record.clicked.connect(add_record)
        self.btn_timer_record.setToolTip('<b> Register Record <\b>')

        hbox = QHBoxLayout(self.timer_frame)
        hbox.addWidget(self.btn_timer_record, 1, Qt.AlignCenter)
        hbox.addWidget(self.btn_timer, 1, Qt.AlignCenter)
        hbox.addWidget(self.btn_timer_clear, 1, Qt.AlignCenter)

        self.timer_frame_grid.addLayout(hbox, 1, 0, Qt.AlignCenter)

    def make_cd_timer_frame(self):
        self.cd_timer_frame_grid = QGridLayout(self.cd_timer_frame)
        self.cd_timer_frame_grid.setVerticalSpacing(5)
        self.cd_timer_frame_grid.setHorizontalSpacing(5)

        btn_style = '''QPushButton {background-color: #232323; color: white; border: 0px;
                        font-family: Myriad Pro; font-size: 30pt; height: 90px;}
                        QPushButton::Hover {background-color: #303030;}
                        QPushButton::pressed {background-color: white; color: black;}'''

        # ===========================Row 1==================================

        self.lb_cd_timer = QLabel(self.cd_timer_frame)
        self.lb_cd_timer.setText('00:00:00')
        self.lb_cd_timer.setStyleSheet(
            '''QLabel {background-color: #303030; color: white; border: 1px solid white;
                font-family: Myriad Pro; font-size: 25pt;}''')
        self.lb_cd_timer.setAlignment(Qt.AlignCenter)
        self.lb_cd_timer.setCursor(QCursor(Qt.IBeamCursor))
        self.lb_cd_timer.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.cd_timer_frame_grid.addWidget(self.lb_cd_timer, 0, 0, 1, 2)

        self.cd_timer = CDTimer('00:00:00')

        delete_btn = QPushButton(self.cd_timer_frame)
        delete_btn.setIcon(QIcon(resource_path('media/delete.png')))
        delete_btn.setIconSize(QSize(60, 60))
        delete_btn.setStyleSheet('''QPushButton {background-color: #232323; border: 0px; height: 90px;}
                            QPushButton::Hover {background-color: #303030;}
                            QPushButton::pressed {background-color: #404040;}''')
        delete_btn.setCursor(QCursor(Qt.PointingHandCursor))
        delete_btn.clicked.connect(lambda: self.lb_cd_timer.setText(
            self.cd_timer.delete_last_number()))
        self.cd_timer_frame_grid.addWidget(delete_btn, 0, 2)

        # ===========================Row 2==================================

        one_btn = QPushButton(self.cd_timer_frame)
        one_btn.setText('1')
        one_btn.setStyleSheet(btn_style)
        one_btn.setCursor(QCursor(Qt.PointingHandCursor))
        one_btn.clicked.connect(lambda: self.lb_cd_timer.setText(
            self.cd_timer.add_number('1')))
        self.cd_timer_frame_grid.addWidget(one_btn, 1, 0)

        two_btn = QPushButton(self.cd_timer_frame)
        two_btn.setText('2')
        two_btn.setStyleSheet(btn_style)
        two_btn.setCursor(QCursor(Qt.PointingHandCursor))
        two_btn.clicked.connect(lambda: self.lb_cd_timer.setText(
            self.cd_timer.add_number('2')))
        self.cd_timer_frame_grid.addWidget(two_btn, 1, 1)

        three_btn = QPushButton(self.cd_timer_frame)
        three_btn.setText('3')
        three_btn.setStyleSheet(btn_style)
        three_btn.setCursor(QCursor(Qt.PointingHandCursor))
        three_btn.clicked.connect(
            lambda: self.lb_cd_timer.setText(self.cd_timer.add_number('3')))
        self.cd_timer_frame_grid.addWidget(three_btn, 1, 2)

        # ===========================Row 3==================================

        four_btn = QPushButton(self.cd_timer_frame)
        four_btn.setText('4')
        four_btn.setStyleSheet(btn_style)
        four_btn.setCursor(QCursor(Qt.PointingHandCursor))
        four_btn.clicked.connect(
            lambda: self.lb_cd_timer.setText(self.cd_timer.add_number('4')))
        self.cd_timer_frame_grid.addWidget(four_btn, 2, 0)

        five_btn = QPushButton(self.cd_timer_frame)
        five_btn.setText('5')
        five_btn.setStyleSheet(btn_style)
        five_btn.setCursor(QCursor(Qt.PointingHandCursor))
        five_btn.clicked.connect(
            lambda: self.lb_cd_timer.setText(self.cd_timer.add_number('5')))
        self.cd_timer_frame_grid.addWidget(five_btn, 2, 1)

        six_btn = QPushButton(self.cd_timer_frame)
        six_btn.setText('6')
        six_btn.setStyleSheet(btn_style)
        six_btn.setCursor(QCursor(Qt.PointingHandCursor))
        six_btn.clicked.connect(lambda: self.lb_cd_timer.setText(
            self.cd_timer.add_number('6')))
        self.cd_timer_frame_grid.addWidget(six_btn, 2, 2)

        # ===========================Row 4==================================

        seven_btn = QPushButton(self.cd_timer_frame)
        seven_btn.setText('7')
        seven_btn.setStyleSheet(btn_style)
        seven_btn.setCursor(QCursor(Qt.PointingHandCursor))
        seven_btn.clicked.connect(
            lambda: self.lb_cd_timer.setText(self.cd_timer.add_number('7')))
        self.cd_timer_frame_grid.addWidget(seven_btn, 3, 0)

        eight_btn = QPushButton(self.cd_timer_frame)
        eight_btn.setText('8')
        eight_btn.setStyleSheet(btn_style)
        eight_btn.setCursor(QCursor(Qt.PointingHandCursor))
        eight_btn.clicked.connect(
            lambda: self.lb_cd_timer.setText(self.cd_timer.add_number('8')))
        self.cd_timer_frame_grid.addWidget(eight_btn, 3, 1)

        nine_btn = QPushButton(self.cd_timer_frame)
        nine_btn.setText('9')
        nine_btn.setStyleSheet(btn_style)
        nine_btn.setCursor(QCursor(Qt.PointingHandCursor))
        nine_btn.clicked.connect(
            lambda: self.lb_cd_timer.setText(self.cd_timer.add_number('9')))
        self.cd_timer_frame_grid.addWidget(nine_btn, 3, 2)

        # ===========================Row 5==================================

        zero_btn = QPushButton(self.cd_timer_frame)
        zero_btn.setText('0')
        zero_btn.setStyleSheet(btn_style)
        zero_btn.setCursor(QCursor(Qt.PointingHandCursor))
        zero_btn.clicked.connect(
            lambda: self.lb_cd_timer.setText(self.cd_timer.add_number('0')))
        self.cd_timer_frame_grid.addWidget(zero_btn, 4, 0, 1, 2)

        start_btn = QPushButton(self.cd_timer_frame)
        start_btn.setText('Start')
        start_btn.setStyleSheet(btn_style)
        start_btn.setCursor(QCursor(Qt.PointingHandCursor))
        start_btn.clicked.connect(self.make_cd_timer_frame2)
        self.cd_timer_frame_grid.addWidget(start_btn, 4, 2)

    def make_cd_timer_frame2(self):
        self.cd_timer_first_number = self.lb_cd_timer.text()

        for i in reversed(range(self.cd_timer_frame_grid.count())):
            self.cd_timer_frame_grid.itemAt(i).widget().setParent(None)

        self.cd_timer_frame_grid.addItem(
            QSpacerItem(500, 20), 0, 0)

        self.btn_cd_timer = QPushButton(self.cd_timer_frame)
        self.btn_cd_timer.setMinimumSize(250, 250)
        self.btn_cd_timer.setCursor(Qt.PointingHandCursor)
        self.btn_cd_timer.setToolTip('<b> Click To Start Or Stop <\b>')
        self.btn_cd_timer.setStyleSheet(
            '''QPushButton {background-color: rgba(0,0,0,0); border: 5px solid gray; border-radius: 125px;
                font-family: Myriad Pro; font-size: 35px; color: white;}
                QPushButton::Hover {color: #FF9F9F; border: 5px solid #FF9F9F;}
                QPushButton::pressed {color: #D20000; border: 5px solid #D20000;}''')

        self.cd_time = CDTimer(self.cd_timer_first_number)
        self.cd_time.correct_time()
        self.btn_cd_timer.setText(str(self.cd_time))

        def timeout(timer):
            current_time = self.btn_cd_timer.text().split('\n')[0]
            if current_time in ['00:00:05', '00:00:04', '00:00:03', '00:00:02', '00:00:01']:
                self.tabs.setCurrentIndex(2)
                if int(current_time.split(':')[2]) % 2 == 1:
                    Beep(1500, 300)
                    self.btn_cd_timer.setStyleSheet(
                        self.btn_cd_timer.styleSheet() + 'QPushButton {color: red; border: 5px solid red}')
                else:
                    self.btn_cd_timer.setStyleSheet(
                        self.btn_cd_timer.styleSheet() + 'QPushButton {color: white; border: 5px solid white}')
            if current_time == '00:00:00':
                self.cd_time_enabled = False
                self.btn_cd_timer.setText('00:00:00\nStart Again')
                timer.stop()
            else:
                new_time = self.cd_time.reduce_second()
                self.btn_cd_timer.setText(new_time + '\nStop')

        def start_stop_timer():
            if self.cd_time_enabled == False:
                if self.btn_cd_timer.text() == '00:00:00\nStart Again':
                    self.btn_cd_timer.setStyleSheet(
                        self.btn_cd_timer.styleSheet() + 'QPushButton {color: white; border: 5px solid white}')
                    self.cd_time = CDTimer(self.cd_timer_first_number)
                    self.cd_time.correct_time()
                    self.btn_cd_timer.setText(str(self.cd_time))

                    timer.start(1000)
                    self.cd_time_enabled = True
                    self.cd_records_list.clear()
                    self.cd_timer_frame_grid.removeWidget(self.cd_records_list)
                else:
                    self.btn_cd_timer.setStyleSheet(self.btn_cd_timer.styleSheet() +
                                                    'QPushButton {color: white; border: 5px solid gray;}')
                    timer.start(1000)
                    self.btn_cd_timer.setText(self.btn_cd_timer.text().split('\n')[
                        0] + '\nStop')
                    self.cd_time_enabled = True
            else:
                timer.stop()
                self.btn_cd_timer.setStyleSheet(self.btn_cd_timer.styleSheet() +
                                                'QPushButton {color: #FF9F9F; border: 5px solid #FF9F9F;}')
                self.btn_cd_timer.setText(
                    self.btn_cd_timer.text().split('\n')[0] + '\nStart')
                self.cd_time_enabled = False

        timer = QTimer(self.cd_timer_frame)
        timer.timeout.connect(lambda: timeout(timer))
        timer.start(1000)
        self.cd_time_enabled = True
        self.btn_cd_timer.clicked.connect(start_stop_timer)

        ###########################################################
        self.cd_records_list = QListWidget()
        self.cd_records_list.setStyleSheet(
            '''QListWidget {background-color: rgba(0,0,0,0); border: 0px;}
                QListWidget::Item {background-color: #303030; color: white; border: 1px solid black}
                QListWidget::Item:Hover {background-color: white; color: black;}
                QListWidget QScrollBar {background-color: white; width: 7px}
                QListWidget QScrollBar::Handle {background-color: gray;}''')
        self.cd_records_list.setMinimumSize(400, 110)
        self.cd_records_list.setFont(QFont('Myriad Pro', 10))
        self.cd_records_list.setCursor(Qt.PointingHandCursor)

        btn_style = '''QPushButton {background-color: rgba(0,0,0,0);}
                        QPushButton::Hover {background-color: #181818;}
                        QPushButton::pressed {background-color: #181818;}'''

        def clear():
            timer.stop()
            self.cd_records_list.clear()
            self.tabs.removeTab(2)
            self.cd_timer_frame.hide()
            self.cd_timer_frame.close()

            self.cd_timer_frame = QFrame(self)
            self.cd_timer_frame.setFixedSize(570, 520)
            self.cd_timer_frame.setStyleSheet('''QFrame {background-color: #1f1f1f; font-family: Myriad Pro; border-top: 0px solid gray;
                                            border-right: 1px solid gray; border-left: 1px solid gray; border-bottom: 1px solid gray;}''')
            self.tabs.addTab(self.cd_timer_frame, QIcon(
                resource_path('media/countdown_timer.png')), '')
            self.tabs.setCurrentIndex(2)

            self.make_cd_timer_frame()

        def add_record():
            self.cd_records_list.setParent(self.cd_timer_frame)
            self.cd_records_list.show()
            self.cd_timer_frame_grid.addWidget(
                self.cd_records_list, 2, 0, Qt.AlignCenter)

            number = self.cd_records_list.count() + 1
            remaining = self.btn_cd_timer.text().split('\n')[0]
            passed = CDTimer(self.cd_timer_first_number) - CDTimer(remaining)
            self.cd_records_list.addItem(
                'Record ' + str(number) + '    ' + passed + ' passed    ' + remaining + ' leftovers')

            item = self.cd_records_list.item(self.cd_records_list.count()-1)
            item.setToolTip(item.text())

        self.btn_cd_timer_clear = QPushButton(self.cd_timer_frame)
        self.btn_cd_timer_clear.setIcon(
            QIcon(resource_path('media/trash_bin.png')))
        self.btn_cd_timer_clear.setStyleSheet(btn_style)
        self.btn_cd_timer_clear.setIconSize(QSize(50, 50))
        self.btn_cd_timer_clear.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_cd_timer_clear.clicked.connect(clear)
        self.btn_cd_timer_clear.setToolTip('<b> Clear CountDown Timer <\b>')

        self.btn_cd_timer_record = QPushButton(self.cd_timer_frame)
        self.btn_cd_timer_record.setIcon(
            QIcon(resource_path('media/time_tracking.png')))
        self.btn_cd_timer_record.setStyleSheet(btn_style)
        self.btn_cd_timer_record.setIconSize(QSize(60, 60))
        self.btn_cd_timer_record.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_cd_timer_record.clicked.connect(add_record)
        self.btn_cd_timer_record.setToolTip('<b> Register Record <\b>')

        hbox = QHBoxLayout(self.cd_timer_frame)
        hbox.addWidget(self.btn_cd_timer_record, 1, Qt.AlignCenter)
        hbox.addWidget(self.btn_cd_timer, 1, Qt.AlignCenter)
        hbox.addWidget(self.btn_cd_timer_clear, 1, Qt.AlignCenter)

        self.cd_timer_frame_grid.addLayout(hbox, 1, 0, Qt.AlignCenter)

    def make_about(self):
        self.about_win = QWidget()
        self.about_win.setGeometry(700, 400, 450, 380)
        self.about_win.setFixedSize(450, 380)
        self.about_win.setWindowIcon(QIcon(resource_path('media/logo.png')))
        self.about_win.setWindowTitle('About Us')
        self.about_win.setStyleSheet('background-color: #303030')

        about_grid = QGridLayout(self.about_win)

        lb_about = QLabel(self.about_win)
        lb_about.setWordWrap(True)
        with open(resource_path('media/about.txt'), 'r') as file:
            text = file.read()
        lb_about.setText(text)
        lb_about.setStyleSheet(
            'color: white; font-family: Myriad Pro; font-size: 15pt;')
        lb_about.setAlignment(Qt.AlignLeft)

        ##############################################################

        link_github = QCommandLinkButton(
            "Open The Developer's GitHub Account", self.about_win)
        link_github.setStyleSheet(
            'QCommandLinkButton {background-color: rgba(0,0,0,0); color: white; font-family: Myriad Pro; font-size: 10pt;}')
        link_github.setCursor(QCursor(Qt.PointingHandCursor))
        browser = WindowsDefault()
        link_github.clicked.connect(lambda: browser.open_new_tab(
            'https://github.com/AR-Tavallaei'))
        link_github.setToolTip('<b> Click To Open Link <\b>')

        lb_logo = QPushButton(self.about_win)
        lb_logo.setIcon(QIcon(resource_path('media/logo.png')))
        lb_logo.setIconSize(QSize(50, 50))
        lb_logo.setFlat(True)

        about_grid.addWidget(lb_about, 0, 0, Qt.AlignCenter)
        about_grid.addWidget(lb_logo, 2, 0, Qt.AlignCenter)
        about_grid.addWidget(link_github, 1, 0, Qt.AlignLeft)
        self.about_win.show()


app = QApplication([])
win = TimeManager()
fonts = QFontDatabase()
fonts.addApplicationFont(resource_path('media/MyriadPro_Semibold.otf'))
win.show()
sys.exit(app.exec())
