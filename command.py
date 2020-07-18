#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re
from quickcmd_color import QuickCmdColor


class Command(object):
    def __init__(self, file="", name="", items=[]):
        infos = {k: v for (k, v) in items}
        self.command = infos.get("command", "")
        self.set_workdir(infos.get("workdir", ""))
        self.godir = infos.get("godir", "")
        self.desc = infos.get("desc", "")
        self.file = file
        self.name = name
        self.qcc = QuickCmdColor()

    def abs_path(self, path):
        if path and path.startswith("~"):
            # os.path.join(os.path.expanduser("~"), path[1:])
            return os.path.expanduser("~") + path[1:]
        return path

    def script_path(self):
        return os.path.dirname(os.path.realpath(__file__))

    def set_field(self, key, value):
        if key == "name":
            self.name = value
        elif key == "command":
            self.command = value
        elif key == "workdir":
            self.workdir = self.abs_path(value)
        elif key == "godir":
            self.godir = self.abs_path(value)

    def get_file(self):
        return self.file

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def set_cmd(self, command):
        self.command = command

    def set_workdir(self, workdir):
        self.workdir = self.abs_path(workdir)

    def set_godir(self, godir):
        self.godir = godir

    def complete(self):
        if not self.command:
            return True

        pt = re.compile(r'\${\w+}')
        variables = pt.findall(self.command)
        variables = set(variables)

        for variable in variables:
            m = re.match(r'^\${(\w+)}$', variable)
            name = m.group(1)
            try:
                self.qcc.purple_print(self.command)
                value = self.qcc.green_input(r"input %s:" % (name))
                self.command = self.command.replace(variable, value)
            except KeyboardInterrupt:
                return False
        return True

    def execute(self):
        self.qcc.purple_print(self.tostring())
        if self.command:
            if self.workdir and os.path.exists(self.workdir):
                os.chdir(self.workdir)
            os.system(self.command)

        if self.godir:
            godir = self.abs_path(self.godir)
            os.system("echo '%s' > %s/.qc.cd.path" %
                      (godir, self.script_path()))

    def tostring(self):
        s = "[%s]" % (self.name)
        if self.command:
            s = "%s\n[+] command = %s" % (s, self.command)
        if self.workdir:
            s = "%s\n[+] workdir = %s" % (s, self.workdir)
        if self.godir:
            s = "%s\n[+] godir   = %s" % (s, self.godir)
        if self.file:
            s = "%s\n[+] in file = %s" %(s, self.file)
        return s

    def fzf_str(self, index):
        res = "{:0>3}:{}".format(index, self.name)
        if self.command:
            res = "{}: {}".format(res, self.command)
        elif self.godir:
            res = "{}; cd {}".format(res, self.godir)
        res = "{}\r\n".format(res)
        return res

