#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re
from quickcmd_color import QuickCmdColor

class Command(object):
    def __init__(self, name="", cmd="", workdir="", godir=""):
        self.name = name
        self.cmd = cmd
        self.workdir = workdir
        self.godir = godir
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
            self.cmd = value
        elif key == "workdir":
            self.workdir = self.abs_path(value)
        elif key == "godir":
            self.godir = self.abs_path(value)

    def set_name(self, name):
        self.name = name
    
    def set_cmd(self, cmd):
        self.cmd = cmd

    def set_workdir(self, workdir):
        self.workdir = workdir

    def set_godir(self, godir):
        self.godir = godir

    def complete(self):
        if not self.cmd:
            return None

        pt = re.compile(r'\${\w+}')
        variables = pt.findall(self.cmd)
        variables_map = {}

        for variable in variables:
            if variable in variables_map:
                continue
            name = re.match(r'^\${(\w+)}$', variable)
            variables_map[variable] = name.group(1)

        for key, name in variables_map.items():
            value = self.qcc.green_input(r"input %s:" % (name))
            #value = value.decode('utf-8')
            self.cmd = self.cmd.replace(key, value)

    def execute(self):
        self.qcc.purple_print(self.tostring())
        if self.cmd:
            if self.workdir and os.path.exists(self.workdir):
                os.chdir(self.workdir)
            os.system(self.cmd)
        
        if self.godir:
            os.system("echo '%s' > %s/.qc_cd_path"%(self.godir, self.script_path()))

    def tostring(self):
        s = "[%s]"%(self.name)
        if self.cmd:
            s = "%s\n[+] command = %s"%(s, self.cmd)
        if self.workdir:
            s = "%s\n[+] workdir = %s"%(s, self.workdir)
        if self.godir:
            s = "%s\n[+] godir   = %s"%(s, self.godir)
        return s