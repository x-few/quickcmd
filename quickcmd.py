#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import optparse
import argparse
from fzf import FuzzyFinder
from command_manager import CommandManager

qc_description = "Quickly select and execute your command."

def default_cmddir():
    basedir = os.path.dirname(os.path.realpath(__file__))
    return basedir + "/commands"

def main(args=None):
    reload(sys)
    sys.setdefaultencoding('utf-8')

    # check fzf
    fzf = FuzzyFinder()
    if fzf.is_exist() is False:
        print("require fzf, please install")
        return 0

    parser = argparse.ArgumentParser(description=qc_description)
    parser.add_argument(
        "-l", "--list",
        dest="list", action="store_true",
        default=False, help="list all commands")
    parser.add_argument(
        "-c", "--cmddir", dest="cmddir",
        help="specify the command directory")
    args = parser.parse_args()
    cmddir = default_cmddir()
    if args.cmddir:
        cmddir = args.cmddir
    cmdmgr = CommandManager(cmddir)
    cmds = cmdmgr.load_commands()
    if args.list:
        cmdmgr.print_commands()
        return 0

    fzf.prepare_files(cmds)
    fzf.run()
    index = fzf.parse_output()
    cmd = cmdmgr.get_command(index)
    if cmd:
        cmd.complete()
        cmd.execute()

if __name__ == "__main__":
    exit(main())
