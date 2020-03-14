import os
import sys


class QuickCmdColor(object):
    def __init__ (self):
        self.black = '\033[30m'
        self.red = '\033[31m'
        self.green = '\033[32m'
        self.yellow = '\033[33m'
        self.blue = '\033[34m'
        self.purple = '\033[35m'
        self.skyblue = '\033[36m'
        self.white = '\033[37m'
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
    def yellow_print(self, msg):
        self.color_print(self.yellow, msg)
    def blue_print(self, msg):
        self.color_print(self.blue, msg)
    def purple_print(self, msg):
        self.color_print(self.purple, msg)
    def skyblue_print(self, msg):
        self.color_print(self.skyblue, msg)
    def white_print(self, msg):
        self.color_print(self.white, msg)

    def color_input(self, color, msg):
        return raw_input(color + msg + self.end)

    def purple_input(self, msg):
        return self.color_input(self.purple, msg)

    def blue_input(self, msg):
        return self.color_input(self.blue, msg)

    def green_input(self, msg):
        return self.color_input(self.green, msg)