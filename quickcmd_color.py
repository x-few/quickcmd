import os
import sys


class QuickCmdColor(object):
    def __init__ (self):
        """
        Black        0;30     Dark Gray     1;30
        Red          0;31     Light Red     1;31
        Green        0;32     Light Green   1;32
        Brown/Orange 0;33     Yellow        1;33
        Blue         0;34     Light Blue    1;34
        Purple       0;35     Light Purple  1;35
        Cyan         0;36     Light Cyan    1;36
        Light Gray   0;37     White         1;37
        """
        self.black = '\033[0;30m'
        self.red = '\033[0;31m'
        self.green = '\033[0;32m'
        self.orange = '\033[0;33m'
        self.blue = '\033[0;34m'
        self.purple = '\033[0;35m'
        self.cyan = '\033[0;36m'
        self.light_gray = '\033[0;37m'
        self.dark_gray = '\033[1;30m'
        self.light_red = '\033[1;31m'
        self.light_green = '\033[1;32m'
        self.yellow = '\033[1;33m'
        self.light_blue = '\033[1;34m'
        self.light_purple = '\033[1;35m'
        self.light_cyan = '\033[1;36m'
        self.white = '\033[1;37m'
        self.underline = '\033[4m'
        self.bold = '\033[1m'
        self.end = '\033[0m'

    def color_print(self, color, msg):
        print(color + msg + self.end)

    def black_print(self, msg):
        self.color_print(self.black, msg)
    def red_print(self, msg):
        self.color_print(self.red, msg)
    def green_print(self, msg):
        self.color_print(self.green, msg)
    def orange_print(self, msg):
        self.color_print(self.yellow, msg)
    def blue_print(self, msg):
        self.color_print(self.blue, msg)
    def purple_print(self, msg):
        self.color_print(self.purple, msg)
    def cyan_print(self, msg):
        self.color_print(self.cyan, msg)
    def light_gray_print(self, msg):
        self.color_print(self.light_gray, msg)
    def dark_gray_print(self, msg):
        self.color_print(self.dark_gray, msg)
    def light_red_print(self, msg):
        self.color_print(self.light_red, msg)
    def light_green_print(self, msg):
        self.color_print(self.light_green, msg)
    def yellow_print(self, msg):
        self.color_print(self.yellow, msg)
    def light_blue_print(self, msg):
        self.color_print(self.light_blue, msg)
    def light_perple_print(self, msg):
        self.color_print(self.light_purple, msg)
    def light_cyan_print(self, msg):
        self.color_print(self.light_cyan, msg)
    def white_print(self, msg):
        self.color_print(self.white, msg)

    def color_input(self, color, msg):
        try:
            if sys.version_info.major == 2:
                return raw_input(color + msg + self.end)
            else:
                return input(color + msg + self.end)
        except KeyboardInterrupt:
            sys.exit(0)

    def purple_input(self, msg):
        return self.color_input(self.purple, msg)

    def blue_input(self, msg):
        return self.color_input(self.blue, msg)

    def green_input(self, msg):
        return self.color_input(self.green, msg)