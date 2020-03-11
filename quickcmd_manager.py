#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import codecs
import tempfile
import shutil

class QuickCmdManager(object):
    def __init__ (self, filename):
        self.filename = filename
        self.load_config()
        self.tmpdir = 'quickcmd'
        self.input_name = 'fzf-input.txt'
        self.output_name = 'fzf-output.txt'

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

    def parse_config(self, ctx):
        config = []
        single = {}
        for line in ctx.split('\n'):
            line = line.strip('\r\n\t ')
            if not line:
                continue
            if line[:1] in ('#', ';'):    # ignore comment
                continue
            if line.startswith('[') and line.endswith(']'):
                    qc_name = line[1:-1].strip('\r\n\t ')
                    if len(single) > 0:
                        config.append(single)
                        single = {}
                    single['name'] = qc_name
            else:
                pos = line.find('=')
                if pos >= 0:
                    key = line[:pos].rstrip('\r\n\t ')
                    val = line[pos + 1:].lstrip('\r\n\t ')
                    single[key] = val
        if len(single) > 0:
            config.append(single)
            single = {}
        return config

    def load_config(self):
        if not self.filename:
            return False
        if not os.path.exists(self.filename):
            return False
        try:
            fd = open(self.filename, 'rb')
            ctx = fd.read()
            fd.close()
        except IOError as e:
            print(e)
        
        dectx = self.decode_content(ctx)
        self.config = self.parse_config(dectx)
        return self.config

    def print_config(self):
        print(self.config)
        # TODO

    def is_changed_config(self):
        # 比较一下配置和fzfinput文件的修改时间，就能知道是否变更
        return True

    def fzf_file_prepare(self):
        self.tmpdir = tempfile.mkdtemp('quickcmd')
        self.fzf_input = os.path.join(self.tmpdir, 'fzf-input.txt')
        self.fzf_output = os.path.join(self.tmpdir, 'fzf-output.txt')
        if os.path.exists(self.fzf_output):
            os.remove(self.fzf_output)

        if self.is_changed_config():
            with codecs.open(self.fzf_input, 'w', encoding='utf-8') as fp:
                i = 1
                for info in self.config:
                    fp.write('%d:%s: %s\r\n'%(i, info['name'], info['command']))
                    i = i + 1

    def fzf_cmd_generate(self):
        cmd = 'fzf --nth 1 --reverse --inline-info --tac +s --height 35%'
        cmd = cmd + ' < "' + self.fzf_input + '"'
        cmd = cmd + ' > "' + self.fzf_output + '"'
        #print("cmd = %s"%(cmd))
        return cmd
    
    def fzf_output_cmd_get(self):
        output = ''
        with codecs.open(self.fzf_output, 'r', encoding='utf-8') as fp:
            output = fp.read()
        # TODO rmdir
        if self.tmpdir:
            shutil.rmtree(self.tmpdir)
        output = output.strip('\r\n\t ')
        pos = output.find(':')
        if (pos < 0):
            return 0
        output = output[:pos].rstrip('\r\n\t ')
        if not output:
            return 0
        output = int(output) - 1
        info = self.config[output]
        return info

    def run(self, info):
        if "command" in info:
            if "workdir" in info:
                os.chdir(info["workdir"])
            os.system(info["command"])
        if "godir" in info:
            print(info["godir"])
            #os.chdir(info["godir"])

    def execute(self):
        self.fzf_file_prepare()
        cmd = self.fzf_cmd_generate()
        code = os.system(cmd)
        if code != 0:
            #print("execute fzf cmd failed, code = %d"%(code))
            return code
        info = self.fzf_output_cmd_get()
        self.run(info)


if __name__ == "__main__":
    filename = os.getcwd() + "/cmds.ini"
    #print(filename)
    qcconf = QuickCmdManager(filename)
    #qcconf.load_config()
    qcconf.print_config()