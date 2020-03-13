#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import codecs
import tempfile
import shutil

class Command(object):
    def __init__(self, name="", cmd="", workdir="", godir=""):
        self.name = name
        self.cmd = cmd
        self.workdir = workdir
        self.godir = godir

    def abs_path(self, path):
        if path and path.startswith("~"):
            # os.path.join(os.path.expanduser("~"), path[1:])
            return os.path.expanduser("~") + path[1:]
        return path

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

    def execute(self):
        print("running: ", self.tostring())
        if self.cmd:
            if self.workdir and os.path.exists(self.workdir):
                os.chdir(self.workdir)
            os.system(self.cmd)
        
        if self.godir:
            os.system("echo '%s' > /tmp/.qc_cd_path"%(self.godir))

    def tostring(self):
        s = """[ %s ]
[+] command = %s
[+] workdir = %s
[+] godir   = %s
"""%(self.name, self.cmd, self.workdir, self.godir)

        return s