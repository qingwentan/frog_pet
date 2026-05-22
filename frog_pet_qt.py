import sys
import random

from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt, QTimer, QPoint

PIXEL = 8

GREEN = QColor("#57c84d")
DARK = QColor("#2e7d32")
WHITE = QColor("white")
BLACK = QColor("black")
GOLD = QColor("#ffd700")
RED = QColor("#ff4d4d")
BLUE = QColor("#4d94ff")
DIAMOND_GREEN = QColor("#39d98a")
BROWN = QColor("#8b6914")
TV_SCREEN = QColor("#333333")


class FrogPet(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Frog Pet")
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )

        self.setAttribute(Qt.WA_TranslucentBackground)

        self.resize(220, 220)

        self.drag_pos = QPoint()
        self.click_start_pos = QPoint()
        self.is_sleepy = False

        # Create speech bubble
        self.speech_bubble = QLabel(self)
        self.speech_bubble.setStyleSheet(
            "background-color: white; color: black; border: 2px solid black; border-radius: 8px; padding: 5px;"
        )
        self.speech_bubble.setFont(QFont("Arial", 12, QFont.Bold))
        self.speech_bubble.setText("guaguagua")
        self.speech_bubble.adjustSize()
        self.speech_bubble.hide()

        # Timer for hiding speech bubble
        self.bubble_timer = QTimer()
        self.bubble_timer.timeout.connect(self.hide_bubble)

        # Inactivity timer for sleepy state (60 seconds)
        self.inactivity_timer = QTimer()
        self.inactivity_timer.timeout.connect(self.go_sleepy)
        self.inactivity_timer.start(60000)

        self.idle_frame = [
            "...YYY....",
            ".YRYXLY...",
            ".GGGGGGG..",
            "GGGGGGGGGG",
            "GGWWGGWWGG",
            "GGWWGGWWGG",
            "GGGGGGGGGG",
            "GGBGGGGBGG",
            ".GGGGGGG..",
            "..G....G.."
        ]

        self.walk_frame = [
            "...YYY....",
            ".YRYXLY...",
            ".G.GGGG..",
            "GGGGGGGGGG",
            "GGWWGGWWGG",
            "GGWWGGWWGG",
            "GGGGGGGGGG",
            "GGGGGGGGGG",
            ".GGG..GGG.",
            ".G......G."
        ]

        self.couch_frame = [
            "TT........",
            "TT........",
            "TT.GGGG...",
            "TT.GWWG.PK",
            "TT.GGGG.PK",
            "BBBBGGGBBB",
            "BBBBBBBBBB",
            "BBBBBBBBBB",
            "RBRRBRBRBR",
            "RBRRBRBRBR"
        ]

        self.current_frame = self.idle_frame

        self.timer = QTimer()
        self.timer.timeout.connect(self.change_animation)
        self.timer.start(800)

    def change_animation(self):
        if not self.is_sleepy:
            self.current_frame = random.choice([
                self.idle_frame,
                self.walk_frame
            ])
        self.update()

    def go_sleepy(self):
        self.is_sleepy = True
        self.current_frame = self.couch_frame
        self.update()

    def wake_up(self):
        self.is_sleepy = False
        self.current_frame = self.idle_frame
        self.inactivity_timer.stop()
        self.inactivity_timer.start(60000)
        self.update()

    def paintEvent(self, event):

        painter = QPainter(self)

        for y, row in enumerate(self.current_frame):
            for x, char in enumerate(row):

                if char == "G":
                    color = GREEN
                elif char == "B":
                    color = BROWN
                elif char == "W":
                    color = WHITE
                elif char == "Y":
                    color = GOLD
                elif char == "R":
                    color = RED
                elif char == "X":
                    color = BLUE
                elif char == "L":
                    color = DIAMOND_GREEN
                elif char == "T":
                    color = TV_SCREEN
                elif char == "P":
                    color = GOLD
                elif char == "K":
                    color = RED
                else:
                    continue

                painter.fillRect(
                    x * PIXEL + 60,
                    y * PIXEL + 60,
                    PIXEL,
                    PIXEL,
                    color
                )

        # pupil
        painter.fillRect(76, 92, PIXEL // 2, PIXEL // 2, BLACK)
        painter.fillRect(108, 92, PIXEL // 2, PIXEL // 2, BLACK)

        # Draw zzz when sleepy
        if self.is_sleepy:
            painter.setFont(QFont("Arial", 14, QFont.Bold))
            painter.drawText(130, 70, 60, 20, Qt.AlignCenter, "zzz")

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos()
            self.click_start_pos = event.globalPos()
            if self.is_sleepy:
                self.wake_up()

    def mouseMoveEvent(self, event):

        if event.buttons() == Qt.LeftButton:
            delta = event.globalPos() - self.drag_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.drag_pos = event.globalPos()

    def mouseReleaseEvent(self, event):

        if event.button() == Qt.LeftButton:
            if (event.globalPos() - self.click_start_pos).manhattanLength() < 12:
                if not self.is_sleepy:
                    self.show_speech_bubble()

    def show_speech_bubble(self):
        self.speech_bubble.show()
        self.speech_bubble.move(60, 20)
        self.bubble_timer.start(1500)
        # Reset inactivity timer
        self.inactivity_timer.stop()
        self.inactivity_timer.start(60000)

    def hide_bubble(self):
        self.speech_bubble.hide()
        self.bubble_timer.stop()





app = QApplication(sys.argv)

frog = FrogPet()
frog.show()

sys.exit(app.exec_())