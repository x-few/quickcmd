#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re
from quickcmd_color import QuickCmdColor
from chatgpt import ChatGPT

class Command(object):
    def __init__(self, file="", name="", items=[]):
        infos = {k: v for (k, v) in items}
        self.command = infos.get("command", "")
        self.set_workdir(infos.get("workdir", ""))
        self.godir = infos.get("godir", "")
        self.desc = infos.get("desc", "")
        self.tip = infos.get("tip", "")
        self.api_key = infos.get("api_key", "")
        self.multi_line_question = infos.get("multi_line_question", False)
        self.file = file

        if self.command:
            prefix = "[CMD] "
            self.cmd_type = "cmd"

        elif self.godir:
            self.cmd_type = "cd"
            prefix = "[GOTO] "

        elif self.tip:
            self.cmd_type = "tip"
            prefix = "[TIP] "

        elif self.api_key:
            self.cmd_type = "chatgpt"
            prefix = "[ChatGPT] "

        else:
            sys.exit("Unknown command")

        self.name = prefix + name
        self.name = self.name.replace(" ", "-")

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
        elif key == "tip":
            self.tip = value

    def get_file(self):
        return self.file

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def set_cmd(self, command):
        self.command = command

    def get_cmd(self):
        return self.command

    def set_workdir(self, workdir):
        self.workdir = self.abs_path(workdir)

    def set_godir(self, godir):
        self.godir = godir

    def get_godir(self):
        return self.godir

    def set_tip(self, tip):
        self.tip = tip

    def get_tip(self):
        return self.tip

    def complete(self):
        """
        Completing the command
        """
        if not self.command:
            # not a command
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
        self.qcc.light_blue_print(self.tostring())
        if self.cmd_type == "cmd":
            if self.workdir and os.path.exists(self.workdir):
                os.chdir(self.workdir)
            os.system(self.command)

        elif self.cmd_type == "cd":
            godir = self.abs_path(self.godir)
            os.system("echo '%s' > %s/../.qc.cd.path" %
                    (godir, self.script_path()))

        elif self.cmd_type == "chatgpt":
            if self.multi_line_question:
                s = "[!] Please enter your question, ending with a new line containing only \"\F\": "
            else:
                s = "[!] Please enter your question: "

            lines = []
            while True:
                line = self.qcc.yellow_input(s)

                if not self.multi_line_question:
                    lines.append(line)
                    break

                if s is not None:
                    s = None

                if line == "\F" or line == "\\f":
                    break

                lines.append(line)

            self.chatgpt = ChatGPT(self.api_key)

            self.qcc.yellow_print("[!] Sending Request to ChatGPT ...")

            choices, total_tokens = self.chatgpt.ask_question("\n".join(lines))

            i = 1
            for answer in choices:
                self.qcc.yellow_print("[+] Answer " + str(i) + ":")
                message = answer.get('message', {})
                content = message.get('content', None)
                if content:
                    print(content)

                i = i + 1

            self.qcc.yellow_print("[!] Spent tokens: " + str(total_tokens))

    def tostring(self):
        s = "[%s]" % (self.name)

        if self.cmd_type == "cmd":
            s = "%s\n[+] Command = %s" % (s, self.command)
            if self.workdir:
                s = "%s\n[+] Workdir: %s" % (s, self.workdir)

        elif self.cmd_type == "cd":
            s = "%s\n[+] Goto: %s" % (s, self.godir)

        elif self.cmd_type == "tip":
            s = "%s\n[+] Tip = %s" % (s, self.tip)

        if self.file:
            s = "%s\n[+] In file = %s" %(s, self.file)

        return s

    def fzf_str(self, index):
        res = "{:0>3}:{}".format(index, self.name)
        if self.command:
            res = "{}: {}".format(res, self.command)
        elif self.godir:
            res = "{}; cd {}".format(res, self.godir)
        elif self.tip:
            res = "{}; tip: {}".format(res, self.tip)

        res = "{}\r\n".format(res)
        return res

