#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import codecs
import tempfile
import shutil

class FuzzyFinder(object):
    def __init__(self):
        self.tmpdir = tempfile.mkdtemp('quickcmd')
        self.fzf_input = os.path.join(self.tmpdir, 'fzf-input.txt')
        self.fzf_output = os.path.join(self.tmpdir, 'fzf-output.txt')

    def is_exist(self):
        # TODO
        return True

    def input_is_changed(self):
        # TODO
        return True

    def prepare_files(self, cmds):
        if os.path.exists(self.fzf_output):
            os.remove(self.fzf_output)

        if self.input_is_changed():
            with codecs.open(self.fzf_input, 'w', encoding='utf-8') as fp:
                i = 1
                for cmd in cmds:
                    if cmd.cmd:
                        fp.write('%d:%s: %s\r\n'%(i, cmd.name, cmd.cmd))
                    elif cmd.godir:
                        fp.write('%d:%s: cd %s\r\n'%(i, cmd.name, cmd.godir))
                    else:
                        fp.write('%d:%s: %s\r\n'%(i, cmd.name, "-"))
                    i = i + 1

    def run(self):
        cmd = 'fzf --nth 1 --reverse --inline-info --tac +s --height 35%'
        cmd = cmd + ' < "' + self.fzf_input + '"'
        cmd = cmd + ' > "' + self.fzf_output + '"'
        #print("cmd = %s"%(cmd))
        return os.system(cmd)

    def parse_output(self):
        output = ''
        with codecs.open(self.fzf_output, 'r', encoding='utf-8') as fp:
            output = fp.read()
        # TODO rmdir
        if self.tmpdir:
            shutil.rmtree(self.tmpdir)
        output = output.strip('\r\n\t ')
        pos = output.find(':')
        if (pos < 0):
            return None
        output = output[:pos].rstrip('\r\n\t ')
        if not output:
            return None
        return (int(output) - 1)