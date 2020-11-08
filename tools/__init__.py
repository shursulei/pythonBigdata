import platform
import os
if platform.system().lower() == 'windows':
    INPUT_DIR = os.getcwd() + '\\input\\'
    OUTPUT_DIR = os.getcwd() + '\\output\\'
    LOG_DIR = os.getcwd() + '\\log\\'
elif platform.system().lower() == 'linux':
    INPUT_DIR = os.getcwd() + '/input/'
    OUTPUT_DIR = os.getcwd() + '/output/'
    LOG_DIR = os.getcwd() + '/log/'



def set_delimiter(dir, file):
    return os.sep.join([dir, file])