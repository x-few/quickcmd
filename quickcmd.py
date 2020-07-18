#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import optparse
import argparse
from fzf import FuzzyFinder
from command_manager import CommandManager

qc_description = "Quickly select and execute your command."


def get_script_path():
    basedir = os.path.dirname(os.path.realpath(__file__))
    return basedir


def get_def_cmd_path():
    basedir = get_script_path()
    return basedir + "/commands"


def print_details():
    print("version: V1.0.0")
    print("commands directory: {}".format(get_def_cmd_path()))
    print("install directory: {}".format(get_script_path()))


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
    parser.add_argument("-f", "--fix", dest="fix", action="store_true", default=False, 
                        help="fix myself: install fzf...")

    cmddir = get_def_cmd_path()
    cmdmgr = CommandManager(cmddir)

    args = parser.parse_args()
    if args.list:
        cmdmgr.load_cmds()
        cmdmgr.print_cmds()
        return 0
    if args.verbose:
        print_details()
        return 0
    if args.addcmd:
        cmdmgr.add_cmd()
        return 0
    if args.delcmd:
        cmdmgr.set_action_del()
    if args.modcmd:
        cmdmgr.set_action_mod()
    if args.fix:
        # TODO
        return 0

    cmdmgr.load_cmds()
    cmds = cmdmgr.get_cmds()

    fzf.prepare_files(cmds)
    fzf.run()
    index = fzf.parse_output()
    cmd = cmdmgr.get_cmd(index)
    if cmd:
        cmdmgr.do_action(cmd)


if __name__ == "__main__":
    exit(main())
