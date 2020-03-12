import os

def default_cmddir():
    return os.path.dirname(os.path.realpath(__file__))

print(default_cmddir())