#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import optparse
import argparse
from quickcmd_manager import QuickCmdManager
#import quickcmd_manager as qcm

qc_description = """
    description
"""
cmds_file = os.getcwd() + "/cmds.ini"


def is_exist_bin(bin="fzf"):
    if os.system("which " + bin) is 0:
        return True
    return False


def main(args=None):
    # check fzf
    if not is_exist_bin("fzf"):
        print("require fzf, please install")
        exit(0)

    parser = argparse.ArgumentParser(description=qc_description)
    parser.add_argument(
        "-l", "--list",
        dest="list", action="store_true",
        default=False, help="list all commands")

    args = parser.parse_args()
    qcm = QuickCmdManager(cmds_file)
    if args.list:
        qcm.print_config()
        exit(0)

    return qcm.execute()

if __name__ == "__main__":
    exit(main())