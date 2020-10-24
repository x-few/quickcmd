# -*- coding: utf-8 -*-
import json
import os


class QcConfig(object):
    """
    读写config 目录下的配置文件 config.json
    """

    def __init__(self, file):
        self.config_file = file
        self.config = None

    def parse(self):
        if not self.config_file or not os.path.exists(self.config_file):
            return None

        with open(self.config_file, "r") as f:
            self.config = json.load(self.config_file)

        return self.config


    def get_command_paths(self):
        if self.config and self.config["command_paths"]:
            return self.config["command_paths"]

        return None




