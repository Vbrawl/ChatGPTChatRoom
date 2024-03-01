# This Python file uses the following encoding: utf-8

import sys, os



def local_path(path:str):
    return os.path.join(getattr(sys, "_MEIPASS", os.getcwd()), path)
