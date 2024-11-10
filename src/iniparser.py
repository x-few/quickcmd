# -*- coding: utf-8 -*-

# https://docs.python.org/2/library/configparser.html#rawconfigparser-objects

import sys
import os


class IniParser(object):
    def __init__(self, file):
        # super().__init__()
        if sys.version_info.major == 2:
            import ConfigParser as cp
            self.config = cp.ConfigParser()
        else:
            import configparser as cp
            self.config = cp.ConfigParser()
        self.file = file
        self.read()

    def read(self):
        if not os.path.exists(self.file):
            return

        if sys.version_info.major == 2:
            self.config.read(self.file)
        else:
            self.config.read(self.file, encoding="utf-8")

    def save(self):
        if not self.file:
            print("IniParser append error: ini file is not exist")
            return
        with open(self.file, 'w') as configfile:
            self.config.write(configfile)

    def remove_empty_file(self):
        if os.path.exists(self.file):
            os.remove(self.file)

    def save_or_remove(self):
        sections = self.sections()
        if not sections:
            self.remove_empty_file()
        else:
            self.save()

    def append(self):
        if not self.file:
            print("IniParser append error: ini file is not exist")
            return

        with open(self.file, 'w') as configfile:
            self.config.write(configfile)

    def set_opt(self, name, configs):
        for config in reversed(configs):
            k, v = config
            self.config.set(name, k, str(v))

    def add(self, name, configs):
        self.config.add_section(name)
        self.set_opt(name, configs)
        # self.append()

    def delete(self, name):
        if self.config.has_section(name):
            self.config.remove_section(name)

    def mod(self, old_name, new_name, configs):
        if old_name != new_name:
            # delete old then add new
            if self.config.has_section(old_name):
                self.delete(old_name)
            self.add(new_name, configs)
        else:
            self.set_opt(old_name, configs)

    def items(self, section):
        res = self.config.items(section)
        #print("items: ", res)
        return res

    def options(self, section):
        res = self.config.options(section)
        #print("options: ", res)
        return res

    def sections(self):
        res = self.config.sections()
        #print("sections: ", res)
        return res

    def all(self):
        configs = list()
        sections = self.sections()
        if not sections:
            return configs

        for section in sections:
            items = self.items(section)
            if not items:
                items = []
            configs.append((section, items))
        return configs

    def defaults(self):
        print(self.config.defaults())


if __name__ == "__main__":
    parser = IniParser("./commands/default.ini")
    name = "test"
    configs = [
        ("key1", 123),
        ("key2", "value2"),
        ("key3", "哈哈哈3"),
    ]
    #parser.mod(name, configs)
    # parser.delete(name)
    parser.items("abc")
    parser.options("abc")
    parser.defaults()
    # parser.save()
