import ctypes
from os import path

def change_desktop():
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path.abspath("background.jpg"), 0)
