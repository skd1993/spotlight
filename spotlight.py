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
import requests
import json

SPI_SETDESKWALLPAPER = 20
HORIZONTAL = (1920, 1080)
VERTICAL = (1080, 1920)

def getUserHome():
      path = os.path.expanduser('~')
      return path

WALLPAPERS_PATH = getUserHome() + '\\AppData\\Local\\Packages\\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\\LocalState\\Assets\\'

CLIENT_ID = '429f941696633ae4e621a7cc0c4460fa143cccdaf5db76bee2b3d4b8dbfc6a69'

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
        
def unsplash():
      url = 'https://api.unsplash.com/photos/random/'
      params = dict(
                  orientattion='landscape',
                  client_id=CLIENT_ID
      )
      resp = requests.get(url=url, params=params)
      print('Getting the wallpaper.....')
      data = json.loads(resp.text)
      img_data = requests.get(data['urls']['full']).content
      with open('temp.jpg', 'wb') as handler:
            handler.write(img_data)
      print('Setting now!')
      path = os.path.abspath('temp.jpg')
      change_wallpaper(path)
      print ("The wallpaper has been changed!\n")
      print ("-------------------------------------------")
      os.remove('temp.jpg')
      
def spotlight():
      for fn in file_list :
            im = Image.open(fn)
            if im.size == HORIZONTAL:
      #            print (fn)
                  change_wallpaper(fn)
                  print ("The wallpaper has been changed!\n")
                  print ("-------------------------------------------")
                  break

while(1):
      print('What do you want to set as the background?')
      print('1. Windows Spotlight Image \n2. Random Unsplash Image \n0. Abort')
      usr_inp = input()
      if usr_inp == '1':
            spotlight()
      elif usr_inp == '2':
            unsplash()
      elif usr_inp == '0':
            break
      else:
            print('Please select a valid value')