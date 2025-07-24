from get_pos import MinecraftCoordinateReader
from json import loads
from blessed import Terminal
import time

got_mc = False
try:
    reader = MinecraftCoordinateReader()
    got_mc = True
except Exception:
    got_mc = False


setting = loads(open("config.json", "r", encoding="utf-8").read())['settings']
float_num = setting['float_num']
term = Terminal()
x_text,y_text,z_text = "X: ", "Y: ", "Z: "
if setting['reverse_y_z']:
    y_text, z_text = z_text, y_text
with term.fullscreen():
    while True:
        
        if not got_mc:
            try:
                reader = MinecraftCoordinateReader()
                got_mc = True
            except Exception as e:
                got_mc = False


        try:
            if got_mc:
                
                x, y, z = reader.get_pos()
                if setting['reverse_y_z']:
                    y, z = z, y
                print(term.move_yx(0, 0) + f"\033[K{x_text}: {round(x, float_num)}")
                print(term.move_yx(1, 0) + f"\033[K{y_text}: {round(y, float_num)}")
                print(term.move_yx(2, 0) + f"\033[K{z_text}: {round(z, float_num)}")
                time.sleep(0.1)
        except Exception as e:
            got_mc = False
            print(term.move_yx(0, 0) + f"\033[K未开启游戏")
            print(term.move_yx(1, 0) + f"\033[K未开启游戏")
            print(term.move_yx(2, 0) + f"\033[K未开启游戏")
        





        