from get_pos import MinecraftCoordinateReader
from json import loads
import tkinter as tk
from tkinter import font
import time
import threading

# 加载配置
setting = loads(open("config.json", "r", encoding="utf-8").read())['settings']
float_num = setting['float_num']
x_text, y_text, z_text = "X: ", "Y: ", "Z: "
if setting['reverse_y_z']:
    y_text, z_text = z_text, y_text

# 创建主窗口
root = tk.Tk()
root.title("Minecraft坐标追踪")
root.geometry("300x150")
root.attributes("-topmost", True)  # 永远置顶
root.resizable(False, False)       # 禁止调整窗口大小

# 自定义字体
custom_font = font.Font(family="Consolas", size=14)

# 坐标显示标签
label_x = tk.Label(root, text=f"{x_text}等待连接...", font=custom_font, anchor="w")
label_y = tk.Label(root, text=f"{y_text}等待连接...", font=custom_font, anchor="w")
label_z = tk.Label(root, text=f"{z_text}等待连接...", font=custom_font, anchor="w")
label_x.pack(fill="x", padx=10, pady=2)
label_y.pack(fill="x", padx=10, pady=2)
label_z.pack(fill="x", padx=10, pady=2)

# 坐标更新函数
def update_coordinates():
    got_mc = False
    reader = None
    
    while True:
        # 尝试连接游戏
        if not got_mc:
            try:
                reader = MinecraftCoordinateReader()
                got_mc = True
            except Exception:
                got_mc = False
                update_labels("未开启游戏", "", "")
        
        # 获取坐标
        if got_mc:
            try:
                x, y, z = reader.get_pos()
                if setting['reverse_y_z']:
                    y, z = z, y
                update_labels(
                    f"{x_text}{round(x, float_num)}",
                    f"{y_text}{round(y, float_num)}",
                    f"{z_text}{round(z, float_num)}"
                )
            except Exception:
                got_mc = False
                update_labels("连接丢失", "连接丢失", "连接丢失")
        
        time.sleep(0.1)

# 安全更新UI的函数
def update_labels(x_str, y_str, z_str):
    label_x.config(text=x_str)
    label_y.config(text=y_str)
    label_z.config(text=z_str)

# 启动坐标更新线程
thread = threading.Thread(target=update_coordinates, daemon=True)
thread.start()

# 运行主循环
root.mainloop()