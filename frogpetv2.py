import sys
import math
import random
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QBrush
from PyQt5.QtCore import Qt, QRectF, QPoint, QTimer

PIXEL = 6 

# 调色盘
LIME = QColor("#76de33"); DARK_GREEN = QColor("#2d8a4e"); BLACK = QColor("#000000")
GOLD = QColor("#ffd700"); WHITE = QColor("white"); CHIP_RED = QColor("#e74c3c")
HEART_RED = QColor("#ff4757"); TONGUE_RED = QColor("#ff6b81")

class DesktopFrog(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.NoDropShadowWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        # 针对 macOS 的输入法报错尝试优化
        self.setAttribute(Qt.WA_InputMethodEnabled, False)
        
        self.resize(400, 350)
        self.drag_pos = QPoint()

        # 状态数据
        self.lines = ["哈！我是瓜瓜罗！", "guaguagua", "wow大西瓜罗！", "嗝~", "嘿咻！", "捉不到我~"]
        self.current_line_index = 0
        self.y_offset, self.jump_step, self.jump_count = 0, 0, 0
        self.is_jumping, self.is_sleeping = False, False
        self.zzz_frame, self.idle_timer = 0, 0
        self.party_mode = None 
        # 新增 action_state: dance, catch
        self.action_state = "normal" 
        self.action_frame = 0 # 用于复杂动作的内部计时

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(50) 

        # --- 像素矩阵图库 ---
        self.frog_map = ["......YYY......", "......Y.Y......", "....KKKKKKK....", "..KKGGGGGGGKK..", ".KGGKGGGGGKGGK.", ".KGGGGGGGGGGGK.", "KGGGGKKKKKGGGGK", "KGGGGGGGGGGGGGK", "KKGGGGGGGGGGGKK", ".KGGGGGGGGGGGK.", ".KGGGGGGGGGGGK.", ".KKGGGGGGGGGKK.", "..KKKKKKKKKKK..", "...K.......K..."]
        self.sleep_map = ["...............................", "........YYY....................", "........Y.Y....................", "......KK...KK..................", "....KKGGKKKGGKK................", "..KKGGGGGGGGGGGKKKKKK..........", ".KGGKGGGGGGKGGGGGGGGGK.........", "KGGGGKKKKKKGGGGGGGGGGGK........", "KGGGGWGGGGGGGGGGGGGGGGGK.......", ".KKKKKKKKKKKKKKKKKKKKKK........"]
        self.beer_map = ["..WWWWW...", "..WWWWW...", "..KYYYK...", "K.KYYYK...", "KKYYYYK...", "K.KYYYK...", "..KYYYK...", "..KKKKK..."]
        self.chips_map = [".KKKKKKK.", "KRRRRRRRK", "KRRGRRRRK", "KRRGGRRRK", "KRRRRRRRK", ".KKKKKKK."]
        self.heart_pixel = [".RR.RR.", "RRRRRRR", "RRRRRRR", ".RRRRR.", "..RRR..", "...R..."]

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            self.action_state = "normal" 
            self.action_frame = 0
            
            if self.is_sleeping:
                self.is_sleeping, self.party_mode, self.jump_count = False, None, 0
            elif not self.is_jumping:
                self.jump_count += 1
                choice = random.random()
                if choice < 0.2: self.party_mode = "beer"
                elif choice < 0.4: self.party_mode = "chips"
                else: self.party_mode = None

                if self.jump_count >= 10:
                    self.is_sleeping, self.party_mode = True, None
                else:
                    self.is_jumping, self.jump_step = True, 0
                    self.current_line_index = random.randint(0, len(self.lines)-1)
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_pos)
            event.accept()

    def contextMenuEvent(self, event):
        sys.exit()

    def animate(self):
        # 1. 跳跃逻辑
        if self.is_jumping:
            self.jump_step += 0.25
            self.y_offset = -abs(math.sin(self.jump_step) * 50)
            if self.jump_step >= math.pi: self.is_jumping, self.y_offset = False, 0
        
        # 2. 睡眠逻辑
        if self.is_sleeping:
            self.zzz_frame = (self.zzz_frame + 1) % 60
        
        # 3. 闲置动作控制
        if not self.is_jumping and not self.is_sleeping:
            self.idle_timer += 1
            if self.idle_timer > 60: # 降低一点触发间隔
                self.idle_timer = 0
                r = random.random()
                if r < 0.1: self.action_state = "tilt_left"
                elif r < 0.2: self.action_state = "tilt_right"
                elif r < 0.3: self.action_state = "sneak"
                elif r < 0.4: self.action_state = "heart"
                elif r < 0.5: self.action_state = "dance" # 新增跳舞
                elif r < 0.6: self.action_state = "catch" # 新增抓苍蝇
                else: self.action_state = "normal"
                self.action_frame = 0

            if self.action_state in ["dance", "catch"]:
                self.action_frame += 1
                if self.action_frame > 30: # 动作持续约1.5秒
                    self.action_state = "normal"
        self.update()

    def draw_pixel_art(self, painter, p_map, ox, oy, color_dict, angle=0, sy=1.0):
        painter.save()
        painter.translate(ox + 40, oy + 80) 
        painter.rotate(angle)
        painter.scale(1.0, sy)
        for y, row in enumerate(p_map):
            for x, char in enumerate(row):
                if char in color_dict:
                    painter.fillRect(int(x * PIXEL - 40), int(y * PIXEL - 80), PIXEL, PIXEL, color_dict[char])
        painter.restore()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 1))
        painter.setRenderHint(QPainter.Antialiasing)

        if self.is_sleeping:
            painter.setBrush(QBrush(DARK_GREEN)); painter.setPen(QPen(BLACK, 1))
            painter.drawEllipse(QRectF(30, 210, 340, 80))

        active_map = self.sleep_map if self.is_sleeping else self.frog_map
        ox, oy = (90, 210) if self.is_sleeping else (150, 180 + self.y_offset)
        
        angle, sy = 0, 1.0
        
        # --- 动作逻辑应用 ---
        if self.action_state == "tilt_left": angle = -12
        elif self.action_state == "tilt_right": angle = 12
        elif self.action_state == "sneak": sy = 0.5; oy += 40
        elif self.action_state == "dance":
            angle = math.sin(self.action_frame * 0.8) * 20 # 快速摇摆
            oy += math.sin(self.action_frame * 0.8) * 10  # 颠簸
        
        # 绘制主体
        self.draw_pixel_art(painter, active_map, ox, oy, {"G": LIME, "K": BLACK, "Y": GOLD, "W": WHITE}, angle, sy)

        # --- 特殊动作层 ---
        if not self.is_sleeping:
            # 1. 抓苍蝇 (舌头)
            if self.action_state == "catch":
                tongue_len = math.sin(self.action_frame * 0.1) * 80
                painter.setPen(QPen(TONGUE_RED, 6, Qt.SolidLine, Qt.RoundCap))
                painter.drawLine(int(ox + 45), int(oy + 40), int(ox + 45 - tongue_len), int(oy + 30))
                # 苍蝇 (小黑点)
                if tongue_len > 10:
                    painter.setBrush(BLACK); painter.setPen(Qt.NoPen)
                    painter.drawEllipse(int(ox + 45 - tongue_len - 5), int(oy + 30 - 5), 4, 4)

            # 2. 道具层
            if self.party_mode == "beer":
                self.draw_pixel_art(painter, self.beer_map, ox + 100, oy + 25, {"W": WHITE, "Y": GOLD, "K": BLACK})
            elif self.party_mode == "chips":
                self.draw_pixel_art(painter, self.chips_map, ox - 50, oy + 40, {"R": CHIP_RED, "G": GOLD, "K": BLACK})
            
            if self.action_state == "heart":
                self.draw_pixel_art(painter, self.heart_pixel, ox + 35, oy - 45, {"R": HEART_RED})

        # 气泡与文字
        if self.is_sleeping:
            painter.setPen(BLACK); painter.setFont(QFont("Arial", 14, QFont.Bold))
            for i in range(3):
                z_y = 190 - (i * 25) - (self.zzz_frame // 2)
                z_x = 130 + (i * 15)
                painter.drawText(z_x, int(z_y), "Z")
        else:
            if self.is_jumping or self.action_state != "normal" or self.party_mode:
                bubble_rect = QRectF(100, 50, 200, 50)
                painter.setBrush(WHITE); painter.setPen(QPen(BLACK, 2))
                painter.drawRoundedRect(bubble_rect, 10, 10)
                painter.setPen(BLACK); painter.setFont(QFont("Arial", 10, QFont.Bold))
                
                text = self.lines[self.current_line_index]
                if self.action_state == "dance": text = "不如跳舞！"
                elif self.action_state == "catch": text = "好大一只苍蝇！"
                elif self.action_state == "heart": text = "爱你哦~"
                elif self.action_state == "sneak": text = "嘿，看不见我..."
                
                painter.drawText(bubble_rect, Qt.AlignCenter, text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DesktopFrog()
    window.show()
    sys.exit(app.exec_())