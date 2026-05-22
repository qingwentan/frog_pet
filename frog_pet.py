import tkinter as tk
import random
import os

# =========================
# 基础设置
# =========================
PIXEL = 8
TRANSPARENT ="#123456"

root = tk.Tk()
root.overrideredirect(True)  # 无边框
root.attributes("-topmost", True)



root.attributes("-transparent", True)
root.configure(bg='systemTransparent')

canvas = tk.Canvas(
    root,
    width=220,
    height=180,
    bg="systemTransparent",
    highlightthickness=0,
    bd=0
)
canvas.pack()

# =========================
# 拖动功能
# =========================
offset_x = 0
offset_y = 0

def start_drag(event):
    global offset_x, offset_y
    offset_x = event.x
    offset_y = event.y

def drag(event):
    x = root.winfo_x() + event.x - offset_x
    y = root.winfo_y() + event.y - offset_y
    root.geometry(f"+{x}+{y}")

canvas.bind("<Button-1>", start_drag)
canvas.bind("<B1-Motion>", drag)

# =========================
# 双击呱呱叫
# =========================
def croak(event):
    os.system('say "gua gua"')

canvas.bind("<Double-Button-1>", croak)

# =========================
# 像素绘制函数
# =========================
def draw_pixel(x, y, color):
    canvas.create_rectangle(
        x * PIXEL,
        y * PIXEL,
        (x + 1) * PIXEL,
        (y + 1) * PIXEL,
        fill=color,
        outline=color
    )

# =========================
# 青蛙像素数据
# =========================

# 颜色
GREEN = "#4CAF50"
DARK = "#2E7D32"
EYE = "white"
PUPIL = "black"
CROWN = "#FFD700"

# 待机状态
frog_idle = [
"....YY....",
"...YYYY...",
"..GGGGGG..",
".GGGGGGGG.",
"GGWWGGWWGG",
"GGWWGGWWGG",
"GGGGGGGGGG",
"GGBGGGGBGG",
".GGGGGGGG.",
"..G....G.."
]

# 走路状态
frog_walk = [
"....YY....",
"...YYYY...",
"..GGGGGG..",
".GGGGGGGG.",
"GGWWGGWWGG",
"GGWWGGWWGG",
"GGGGGGGGGG",
"GGGGGGGGGG",
".GGG..GGG.",
".G......G."
]

# =========================
# 绘制角色
# =========================
current_frame = frog_idle

def draw_frog(frame):
    canvas.delete("all")

    for y, row in enumerate(frame):
        for x, ch in enumerate(row):

            if ch == "G":
                color = GREEN

            elif ch == "B":
                color = DARK

            elif ch == "W":
                color = EYE

            elif ch == "Y":
                color = CROWN

            else:
                continue

            draw_pixel(x + 8, y + 5, color)

    # 眼睛瞳孔
    draw_pixel(10, 9, PUPIL)
    draw_pixel(14, 9, PUPIL)

# =========================
# 动画系统
# =========================
states = [frog_idle, frog_walk]

def animate():
    global current_frame

    current_frame = random.choice(states)
    draw_frog(current_frame)

    delay = random.randint(500, 1200)
    root.after(delay, animate)

# =========================
# 初始位置
# =========================
root.geometry("220x180+500+300")

animate()

root.mainloop()