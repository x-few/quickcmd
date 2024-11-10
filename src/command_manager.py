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
    def __init__(self, cmddir):
        self.def_qc_file = cmddir + "/default.ini"
        self.cmddir = cmddir
        self.commands = []
        self.qcc = QuickCmdColor()
        self.cp = None

    def to_cmds(self, inifile, configs):
        #self.commands = []
        for config in configs:
            section, options = config
            cmd = Command(inifile, section, options)
            self.commands.append(cmd)

    def load_cmds(self):
        if not os.path.exists(self.cmddir):
            return None

        #all_config = []
        for path, _, files in os.walk(self.cmddir):
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
        if self.commands and index is not None and index >= 0:
            return self.commands[index]
        return None

    def gen_config(self, name, config_dict):
        configs = list()

        for key, value in config_dict.items():
            configs.append((key, value))

        return name, configs

    def add_cmd(self):
        config_dict = None

        while True:
            config_dict = dict()

            name = self.qcc.green_input("Command name: ")
            if not name:
                self.qcc.red_print("invalid command name!")
                continue

            cmd_type = self.qcc.green_input("\n1.command\n2.change directory\n3.tip\n4.ChatGPT\nCommand type: ")
            if int(cmd_type) == 1:
                cmd = self.qcc.green_input("Command: ")
                if not cmd:
                    self.qcc.red_print("Bad command")
                    continue

                config_dict["command"] = cmd

                workdir = self.qcc.green_input("Work Directory: ")
                config_dict["workdir"] = workdir

            elif int(cmd_type) == 2:
                godir = self.qcc.green_input("Directory: ")
                if not godir:
                    self.qcc.red_print("Bad directory " + godir)
                    continue

                if not os.path.exists(godir):
                    self.qcc.red_print("Directory not found: " + godir)
                    continue

                config_dict["godir"] = godir

            elif int(cmd_type) == 3:
                tip = self.qcc.lines_input("Tip: ")
                if not tip:
                    self.qcc.red_print("Bad Tip")
                    continue

                config_dict["tip"] = tip

            elif int(cmd_type) == 4:
                api_key = self.qcc.green_input("API Key: ")
                if not api_key:
                    self.qcc.red_print("Bad API Key")
                    continue

                config_dict["api_key"] = api_key

                multi_line = self.qcc.green_input("Do you want to enter multiple lines? [Y/N]: ")
                if multi_line and (multi_line == "Yes" or multi_line == "YES" or multi_line == "Y" or multi_line == "y"):
                    multi_line = True

                else:
                    multi_line = False

                config_dict["multi_line_question"] = multi_line

                # TODO try to ask a question to check if the API key is valid

            break

        # print cmd file
        print(name)
        files = os.listdir(self.cmddir)
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
                    cmdfile = "{}/{}".format(self.cmddir, newfn)
                    if not newfn.endswith(".ini"):
                        cmdfile = "{}.ini".format(cmdfile)
                    if not os.path.exists(cmdfile):
                        break
                break
            elif select_num > 0 and select_num < i:
                # select file
                cmdfile = "{}/{}".format(self.cmddir,
                                        cmdfiles[select_num - 1])
                break
            else:
                # invalid select
                self.qcc.red_print("invalid input")

        section, configs = self.gen_config(name, config_dict)
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

    def mod_cmd(self, cmd_obj):
        cmdfile = cmd_obj.get_file()
        old_name = cmd_obj.get_name()
        old_cmd = cmd_obj.get_cmd()
        old_godir = cmd_obj.get_godir()
        old_tip = cmd_obj.get_tip()
        new_configs = []

        while True:
            name = self.qcc.green_input("command name: ")
            cmd = self.qcc.green_input("command: ")
            godir = self.qcc.green_input("cd directory: ")
            tip = self.qcc.lines_input("tip: ")

        if not name:
            name = old_name

        if not cmd:
            cmd = old_cmd

        if not godir:
            godir = old_godir

        if not tip:
            tip = old_tip

        new_section, new_configs = self.gen_config(name, cmd, godir, tip)
        self.qcc.red_print("modify {} to {} in {}".format(old_name, new_section, cmdfile))
        parser = iniparser.IniParser(cmdfile)
        parser.mod(old_name, new_section, new_configs)
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
