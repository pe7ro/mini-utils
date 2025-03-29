#!/usr/bin/env python3

import collections
import logging
import pathlib
import datetime
import sys
import time

import psutil
from PyQt5.QtCore import QTimer, Qt, QUrl
from PyQt5.QtGui import QFont, QColor, QPainter, QBrush
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent


class PeeperApp(QWidget):
    def __init__(self):
        super().__init__()

        size = 400, 240
        # self.setGeometry(100, 100, *size)
        self.setFixedSize(*size)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        self.main_colors = ('#222222', '#dddddd', '#dd0000')
        self.bars_colors = ('#005533', '#aa0000', '#552211')
        self.bar_height = 5
        self.cpu_usage_queue = collections.deque(maxlen=20)
        self.state = -1
        self.last_update_second = 0

        # QSound can only play wav files
        # self.sound = QSound('/usr/share/sounds/freedesktop/stereo/service-login.oga')
        self.sound = QMediaPlayer()
        url = QUrl.fromLocalFile('/usr/share/sounds/freedesktop/stereo/service-login.oga')
        content = QMediaContent(url)
        self.sound.setMedia(content)

        self.time_label = QLabel(self)
        self.time_label.setFont(QFont('FreeSans', 42, QFont.Bold))
        self.time_label.setStyleSheet(f"background-color: {self.main_colors[0]}; color: {self.main_colors[1]}")
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setGeometry(0, 0, *size)

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.update)
        self.timer.start(100)

    def mousePressEvent(self, event):
        x = event.globalX() - self.width() // 2
        y = event.globalY() - self.height() // 2
        self.move(x, y)

    def mouseMoveEvent(self, event):
        x = event.globalX() - self.width() // 2
        y = event.globalY() - self.height() // 2
        self.move(x, y)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_X:
            self.close()

    def update(self):
        dt = datetime.datetime.now()
        self.time_label.setText('{:02}:{:02}:{:02}'.format(dt.hour, dt.minute, dt.second))
        if dt.minute % 15 == 0:
            if self.state != 1:
                self.state = 1
                self.sound.play()
                self.time_label.setStyleSheet(f"background-color: {self.main_colors[2]}; color: {self.main_colors[0]}")
        else:
            if self.state != 0:
                self.state = 0
                # self.sound.play()
                self.time_label.setStyleSheet(f"background-color: {self.main_colors[0]}; color: {self.main_colors[1]}")

        size = self.time_label.width(), self.time_label.height()
        perwid = size[0] / 100.0
        self.cpu_usage_queue.append(psutil.cpu_percent())
        cpu_usage = sum(self.cpu_usage_queue) / len(self.cpu_usage_queue)
        ram = psutil.virtual_memory()
        ram_usage = ram.percent
        ram_cached = ram.cached / ram.total * 100
        cpu_bar_width = int(cpu_usage * perwid)
        ram_bar_width = int(ram_usage * perwid), int(ram_cached * perwid)

        pixmap = self.time_label.grab()
        painter = QPainter(pixmap)
        painter.setPen(Qt.NoPen)
        # painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor(self.bars_colors[0])))
        painter.drawRect(0, size[1] - self.bar_height * 2, cpu_bar_width, self.bar_height)
        painter.setBrush(QBrush(QColor(self.bars_colors[1])))
        painter.drawRect(0, size[1] - self.bar_height, ram_bar_width[0], self.bar_height)
        painter.setBrush(QBrush(QColor(self.bars_colors[2])))
        painter.drawRect(ram_bar_width[0], size[1] - self.bar_height, ram_bar_width[1], self.bar_height)
        painter.end()
        self.time_label.setPixmap(pixmap)
        ct = time.time_ns()
        ctm = ct // 1_000_000
        if self.last_update_second + 1 < ctm // 1000:
            self.last_update_second = ctm // 1000
            self.timer.start(100)
        else:
            self.last_update_second = ctm // 1000
            self.timer.start(1000 - (ctm % 1000))


def configure_logging(log_file=None, level=logging.INFO):
    if log_file is not None:
        handlers = [
            logging.FileHandler(log_file),
            logging.StreamHandler(),
        ]
    else:
        handlers = [
            logging.StreamHandler(),
        ]
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=handlers,
    )
    logging.info('logging started: %s => %s', pathlib.Path(__file__).name, log_file)


if __name__ == "__main__":
    configure_logging(level=logging.INFO)
    app = QApplication(sys.argv)
    window = PeeperApp()
    window.show()
    sys.exit(app.exec_())
