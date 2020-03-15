#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import codecs
import tempfile
import shutil
from command import Command
from quickcmd_color import QuickCmdColor

class CommandManager(object):
    def __init__ (self, cmddir):
        self.cmddir = cmddir
        self.commands = []
        self.qcc = QuickCmdColor()
        # self.load_commands()

    def decode_content(self, ctx, codec=None):
        dectx = ""
        if ctx[:3] == b'\xef\xbb\xbf':
            dectx = ctx[3:].decode('utf-8')
        elif codec is not None:
            dectx = ctx.decode(codec, 'ignore')
        else:
            codec = sys.getdefaultencoding()
            dectx = None
            for name in [codec, 'gbk', 'utf-8']:
                try:
                    dectx = ctx.decode(name)
                    break
                except:
                    pass
            if dectx is None:
                dectx = ctx.decode('utf-8', 'ignore')
        return dectx

    def parse_commands(self, ctx):
        cmd = None
        for line in ctx.split('\n'):
            line = line.strip('\r\n\t ')
            if not line:
                continue
            if line[:1] in ('#', ';'):    # ignore comment
                continue
            if line.startswith('[') and line.endswith(']'):
                name = line[1:-1].strip('\r\n\t ')
                if cmd:
                    self.commands.append(cmd)
                cmd = Command(name)
            else:
                pos = line.find('=')
                if pos >= 0:
                    key = line[:pos].rstrip('\r\n\t ')
                    val = line[pos + 1:].lstrip('\r\n\t ')
                    #single[key] = val
                    cmd.set_field(key, val)
        if cmd:
            self.commands.append(cmd)

    def load_commands(self):
        if not os.path.exists(self.cmddir):
            return None
        cdw = os.walk(self.cmddir)
        for path, _, files in cdw:
            for file in files:
                filename = os.path.join(path, file)
                try:
                    fd = open(filename, 'rb')
                    ctx = fd.read()
                    fd.close()
                except IOError as e:
                    self.qcc.red_print(e)
        
                dectx = self.decode_content(ctx)
                self.parse_commands(dectx)

        return self.commands

    def get_commands(self):
        return self.commands

    def print_commands(self):
        if self.commands:
            i = 0
            for cmd in self.commands:
                i = i + 1
                if i % 2 == 0:
                    self.qcc.blue_print(cmd.tostring())
                else:
                    self.qcc.skyblue_print(cmd.tostring())

    def get_command(self, index):
        if self.commands and index:
            return self.commands[index]
        return None
