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
from stock_analyzer import run_stock_analysis_workflow

class CommandManager(object):
    def __init__(self, cmddir):
        self.def_qc_file = cmddir + "/default.ini"
        self.cmddir = cmddir
        self.commands = []
        self.qcc = QuickCmdColor()
        self.cp = None

    def to_cmds(self, inifile, configs):
        for config in configs:
            section, options = config
            cmd = Command(inifile, section, options)
            self.commands.append(cmd)

    def load_cmds(self):
        if not os.path.exists(self.cmddir):
            return None

        for path, _, files in os.walk(self.cmddir):
            for filename in files:
                if not filename.endswith(".ini"):
                    continue
                inifile = os.path.join(path, filename)
                parser = iniparser.IniParser(inifile)
                configs = parser.all()
                self.to_cmds(inifile, configs)

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
        if self.commands and index is not None and index >= 0 and index < len(self.commands):
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

            cmd_type_prompt = "\n1.command\n2.change directory\n3.tip\n4.ChatGPT\n5.Stock Analysis\nCommand type: "
            cmd_type = self.qcc.green_input(cmd_type_prompt)

            if not cmd_type.isdigit():
                self.qcc.red_print("Invalid selection.")
                continue

            cmd_type = int(cmd_type)

            if cmd_type == 1:
                cmd = self.qcc.green_input("Command: ")
                if not cmd:
                    self.qcc.red_print("Bad command")
                    continue
                config_dict["command"] = cmd
                workdir = self.qcc.green_input("Work Directory: ")
                config_dict["workdir"] = workdir
            elif cmd_type == 2:
                godir = self.qcc.green_input("Directory: ")
                if not godir or not os.path.exists(godir):
                    self.qcc.red_print("Bad or non-existent directory: " + godir)
                    continue
                config_dict["godir"] = godir
            elif cmd_type == 3:
                tip = self.qcc.lines_input("Tip: ")
                if not tip:
                    self.qcc.red_print("Bad Tip")
                    continue
                config_dict["tip"] = tip
            elif cmd_type == 4:
                api_key = self.qcc.green_input("API Key: ")
                if not api_key:
                    self.qcc.red_print("Bad API Key")
                    continue
                config_dict["api_key"] = api_key
                multi_line = self.qcc.green_input("Do you want to enter multiple lines? [Y/N]: ")
                config_dict["multi_line_question"] = multi_line.lower() in ['y', 'yes']
            elif cmd_type == 5:
                config_dict["type"] = "stock"
            else:
                self.qcc.red_print("Invalid command type!")
                continue

            break

        files = [f for f in os.listdir(self.cmddir) if f.endswith(".ini")]
        cmdfile = None
        while True:
            i = 1
            for file in files:
                self.qcc.blue_print("{}: {}".format(i, file))
                i += 1
            self.qcc.red_print("{}: new file".format(i))
            select = self.qcc.green_input("please select: ")
            select = select.strip()

            if select == "":
                cmdfile = self.def_qc_file
                break

            if not select.isdigit():
                self.qcc.red_print("invalid input")
                continue

            select_num = int(select)
            if select_num == i:
                newfn = self.qcc.green_input("input new filename (without .ini): ")
                if newfn:
                    cmdfile = "{}/{}.ini".format(self.cmddir, newfn)
                    break
            elif 0 < select_num < i:
                cmdfile = os.path.join(self.cmddir, files[select_num - 1])
                break
            else:
                self.qcc.red_print("invalid input")

        section, configs = self.gen_config(name, config_dict)
        print("command file: {}".format(cmdfile))
        parser = iniparser.IniParser(cmdfile)
        parser.add(section, configs)
        parser.save()

    def del_cmd(self, cmd):
        cmdfile = cmd.get_file()
        section = cmd.get_name().split(']', 1)[1].replace('-', ' ') # Get original name
        self.qcc.red_print("delete {} from {}".format(section, cmdfile))
        parser = iniparser.IniParser(cmdfile)
        parser.delete(section)
        parser.save_or_remove()

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
            cmd_type = cmd.get_type()
            if cmd_type == "stock":
                run_stock_analysis_workflow()
            elif cmd.complete():
                return cmd.execute()
        elif self.action == "del":
            return self.del_cmd(cmd)
        elif self.action == "mod":
            return self.mod_cmd(cmd)
