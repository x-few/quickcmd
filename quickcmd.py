#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import optparse
import argparse
from fzf import FuzzyFinder
from command_manager import CommandManager
from quickcmd_config import QcConfig

qc_description = "Quickly select and execute your command."
qcdir = ".quickcmd"


def get_script_path():
    basedir = os.path.dirname(os.path.realpath(__file__))
    return basedir

def get_config_file():
    basedir = get_script_path()
    return basedir + "/config/config.json"

def get_def_cmd_path():
    basedir = get_script_path()
    return basedir + "/commands"


def print_details():
    print("version: V1.0.0")
    print("commands directory: {}".format(get_def_cmd_path()))
    print("install directory: {}".format(get_script_path()))


def install_quickcmd():
    userpath = os.path.expanduser("~")
    if not userpath:
        print("Error: get user path failed")
        return False
    script_path = get_script_path()
    cmd = "cp -r {} {}/{}".format(script_path, userpath, qcdir)
    ret = os.system(cmd)
    if ret != 0:
        print("Error: {}", cmd)
        return False
    qcfile = "{}/{}/quickcmd.sh".format(userpath, qcdir)
    zshfile = "{}/.zshrc".format(userpath)
    bashfile = "{}/.bashrc".format(userpath)
    if os.path.exists(zshfile):
        cmd = 'echo "source {}" >> {}'.format(qcfile, zshfile)
        os.system(cmd)
    if os.path.exists(bashfile):
        cmd = 'echo "source {}" >> {}'.format(qcfile, bashfile)
        os.system(cmd)
    return True

def uninstall_quickmd():
    userpath = os.path.expanduser("~")
    if not userpath:
        print("Error: get user path failed")
        return False
    qcpath = "{}/{}".format(userpath, qcdir)
    if os.path.exists(qcpath):
        cmd = "rm -rf {}".format(qcpath)
        os.system(cmd)
    zshfile = "{}/.zshrc".format(userpath)
    bashfile = "{}/.bashrc".format(userpath)
    if os.path.exists(zshfile):
        cmd = "sed '/{0}/d' {1} > /tmp/.quick.rc; cp /tmp/.quick.rc {1}".format(qcdir, zshfile)
        os.system(cmd)
    if os.path.exists(bashfile):
        cmd = "sed '/{0}/d' {1} > /tmp/.quick.rc; cp /tmp/.quick.rc {1}".format(qcdir, bashfile)
        os.system(cmd)

def update_quickcmd():
    # 进入安装目录，进行 git pull
    userpath = os.path.expanduser("~")
    inspath = '{}/{}'.format(userpath, qcdir)
    cmd = "cd {}; git pull origin master".format(inspath)
    os.system(cmd)

def main(args=None):
    reload(sys)
    sys.setdefaultencoding('utf-8')

    # check fzf
    fzf = FuzzyFinder()
    if fzf.is_exist() is False:
        print("require fzf, please install")
        return 0

    parser = argparse.ArgumentParser(description=qc_description)
    parser.add_argument("-l", "--list", dest="list", action="store_true", default=False,
                        help="list all commands")
    parser.add_argument("-v", "--verbose", dest="verbose", action="store_true", default=False,
                        help="get details")
    parser.add_argument("-a", "--addcmd", dest="addcmd", action="store_true", default=False,
                        help="add a quick command")
    parser.add_argument("-d", "--delcmd", dest="delcmd", action="store_true", default=False,
                        help="delete a quick command")
    parser.add_argument("-m", "--modcmd", dest="modcmd", action="store_true", default=False,
                        help="modify a quick command")
    parser.add_argument("-p", "--update", dest="update", action="store_true", default=False,
                        help="update quickcmd")
    parser.add_argument("-i", "--install", dest="install", action="store_true", default=False,
                        help="install quickcmd")
    parser.add_argument("-u", "--uninstall", dest="uninstall", action="store_true", default=False,
                        help="uninstall quickcmd")

    ex_cmd_dirs = None
    config = QcConfig(get_config_file())
    if config.parse() :
        ex_cmd_dirs = config.get_command_paths()

    def_cmd_path = get_def_cmd_path()
    cmd_mgr = CommandManager(ex_cmd_dirs, def_cmd_path)

    args = parser.parse_args()
    if args.list:
        cmd_mgr.load_cmds()
        cmd_mgr.print_cmds()
        return 0
    if args.verbose:
        print_details()
        return 0
    if args.addcmd:
        cmd_mgr.add_cmd()
        return 0
    if args.delcmd:
        cmd_mgr.set_action_del()
    if args.modcmd:
        cmd_mgr.set_action_mod()
    if args.update:
        update_quickcmd()
        return 0
    if args.install:
        install_quickcmd()
        return 0
    if args.uninstall:
        uninstall_quickmd()
        return 0

    cmd_mgr.load_cmds()
    cmds = cmd_mgr.get_cmds()

    fzf.prepare_files(cmds)
    fzf.run()
    index = fzf.parse_output()
    cmd = cmd_mgr.get_cmd(index)
    if cmd:
        cmd_mgr.do_action(cmd)


if __name__ == "__main__":
    exit(main())
