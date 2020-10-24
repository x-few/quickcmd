#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import codecs
import tempfile
import shutil
from command import Command
from quickcmd_color import QuickCmdColor
import platform
import iniparser
# import ConfigParser


class CommandManager(object):
    def __init__(self, ex_cmd_dirs, def_cmd_dir):
        self.def_qc_file = def_cmd_dir + "/default.ini"
        self.def_cmd_dir = def_cmd_dir
        self.ex_cmd_dirs = ex_cmd_dirs
        self.commands = []
        self.qcc = QuickCmdColor()
        self.cp = None
        self.set_action_run()

    def to_cmds(self, inifile, configs):
        #self.commands = []
        for config in configs:
            section, options = config
            cmd = Command(inifile, section, options)
            self.commands.append(cmd)

    def load_cmds(self):
        if not os.path.exists(self.def_cmd_dir):
            return None

        #all_config = []
        for path, _, files in os.walk(self.def_cmd_dir):
            for filename in files:
                # 跳过非 ini 文件
                if not filename.endswith(".ini"):
                    continue
                inifile = os.path.join(path, filename)
                parser = iniparser.IniParser(inifile)
                configs = parser.all()
                #all_config += configs
                self.to_cmds(inifile, configs)

        #self.to_cmds(inifile, all_config)
        # return self.commands

    def get_cmds(self):
        return self.commands

    def print_cmds(self):
        if self.commands:
            i = 0
            for cmd in self.commands:
                i = i + 1
                if i % 2 == 0:
                    self.qcc.orange_print(cmd.tostring())
                else:
                    self.qcc.light_green_print(cmd.tostring())

    def get_cmd(self, index):
        if self.commands and index >= 0:
            return self.commands[index]
        return None

    def gen_config(self, name, cmd, godir):
        configs = list()
        if cmd:
            configs.append(("command", cmd))
        if godir:
            configs.append(("godir", godir))
        return name, configs

    def add_cmd(self):
        while True:
            name = self.qcc.green_input("command name: ")
            if not name:
                self.qcc.red_print("invalid command name!")
                continue
            cmd = self.qcc.green_input("command: ")
            godir = self.qcc.green_input("cd directory: ")
            if not (cmd or godir):
                self.qcc.red_print("both command and godir empty")
                continue
            break
        # print cmd file
        print(name)
        files = os.listdir(self.def_cmd_dir)
        cmdfiles = []
        for file in files:
            if file.endswith(".ini"):
                cmdfiles.append(file)

        cmdfile = None
        while True:
            i = 1
            for file in cmdfiles:
                self.qcc.blue_print("{}: {}".format(i, file))
                i += 1
            self.qcc.red_print("{}: new file".format(i))
            select = self.qcc.green_input("please select: ")     # 直接回车就是默认文件
            select = select.strip()
            # 生成命令
            if select == "":
                # default file
                cmdfile = self.def_qc_file
                break

            if not select.isdigit():
                self.qcc.red_print("invalid input")
                continue

            select_num = int(select)
            if select_num == i:
                # new file
                while True:
                    newfn = None
                    while True:
                        newfn = self.qcc.green_input("input new filename: ")
                        if newfn:
                            break
                    cmdfile = "{}/{}".format(self.def_cmd_dir, newfn)
                    if not newfn.endswith(".ini"):
                        cmdfile = "{}.ini".format(cmdfile)
                    if not os.path.exists(cmdfile):
                        break
                break
            elif select_num > 0 and select_num < i:
                # select file
                cmdfile = "{}/{}".format(self.def_cmd_dir,
                                        cmdfiles[select_num - 1])
                break
            else:
                # invalid select
                self.qcc.red_print("invalid input")

        section, configs = self.gen_config(name, cmd, godir)
        print("command file: {}".format(cmdfile))
        parser = iniparser.IniParser(cmdfile)
        parser.add(section, configs)
        parser.save()

    def del_cmd(self, cmd):
        cmdfile = cmd.get_file()
        section = cmd.get_name()
        self.qcc.red_print("delete {} from {}".format(section, cmdfile))
        parser = iniparser.IniParser(cmdfile)
        parser.delete(section)
        parser.save_or_remove()
        pass

    def mod_cmd(self, cmd):
        cmdfile = cmd.get_file()
        old_section = cmd.get_name()
        new_configs = []
        while True:
            name = self.qcc.green_input("command name('n/N' not): ")
            cmd = self.qcc.green_input("command: ")
            godir = self.qcc.green_input("cd directory: ")
            if not (cmd or godir):
                self.qcc.red_print("both command and godir empty")
                continue
            break
        if not name:
            name = old_section
        new_section, new_configs = self.gen_config(name, cmd, godir)
        self.qcc.red_print("modify {} to {} in {}".format(old_section, new_section, cmdfile))
        parser = iniparser.IniParser(cmdfile)
        parser.mod(old_section, new_section, new_configs)
        parser.save()

    def set_action_del(self):
        self.action = "del"

    def set_action_run(self):
        self.action = "run"

    def set_action_mod(self):
        self.action = "mod"

    def do_action(self, cmd):
        if self.action == "run":
            if cmd.complete():
                return cmd.execute()
        elif self.action == "del":
            return self.del_cmd(cmd)
        elif self.action == "mod":
            return self.mod_cmd(cmd)
