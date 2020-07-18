

import platform
import sys

# import ConfigParser

class Test(object):
    def __init__(self):
        self.cp = None
        if sys.version_info.major == 2:
            import ConfigParser as cp
            self.cp = cp.ConfigParser()
        else:
            import configparser as cp
            self.cp = cp.ConfigParser()

    def get_version(self):
        version = sys.version_info
        print(version.major)
        if sys.version_info.major == 2:
            self.cp.read("../commands/cmds.ini")
        else:
            self.cp.read("../commands/cmds.ini", encoding="utf-8")
        sections = self.cp.sections()
        print(sections)

        
if __name__ == "__main__":
    t = Test()
    t.get_version()