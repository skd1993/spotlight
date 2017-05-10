# -*- coding: utf-8 -*-
"""
Author: Shobhit Kumar Deepanker

Date: 10th May 2017

Description: A simple python script to set the most recent Windows Spotlight picture as the desktop Wallpaper on Windows 10

"""
import struct
import ctypes
from PIL import Image
import os
import glob

SPI_SETDESKWALLPAPER = 20
HORIZONTAL = (1920, 1080)
VERTICAL = (1080, 1920)

def getUserHome():
      path = os.path.expanduser('~')
      return path

WALLPAPERS_PATH = getUserHome() + '\\AppData\\Local\\Packages\\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\\LocalState\\Assets\\'

file_list = (sorted(glob.glob(WALLPAPERS_PATH + "\\*"), key=os.path.getmtime, reverse=True))

def is_64_windows():
    """Find out how many bits is OS. """
    return struct.calcsize('P') * 8 == 64


def get_sys_parameters_info():
    """Based on if this is 32bit or 64bit returns correct version of SystemParametersInfo function. """
    return ctypes.windll.user32.SystemParametersInfoW if is_64_windows() \
        else ctypes.windll.user32.SystemParametersInfoA


def change_wallpaper(path):
    sys_parameters_info = get_sys_parameters_info()
    r = sys_parameters_info(SPI_SETDESKWALLPAPER, 0, path, 3)

    # When the SPI_SETDESKWALLPAPER flag is used,
    # SystemParametersInfo returns TRUE
    # unless there is an error (like when the specified file doesn't exist).
    if not r:
        print(ctypes.WinError())

for fn in file_list :
      im = Image.open(fn)
      if im.size == HORIZONTAL:
#            print (fn)
            change_wallpaper(fn)
            print ("The wallpaper has been changed!")
            break
