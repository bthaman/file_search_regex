"""
used this version for py2exe
with this version, a command window does not open when the .exe is executed
to run, in the command window type: python setup.py py2exe

IMPORTANT NOTE:
  changed the openpyxl __init__.py file to work around an error
  location: C:\\Users\\wjt\\AppData\\Local\\Continuum\\Anaconda3\\envs\\python3.4\\Lib\site-packages\\openpyxl
"""
from distutils.core import setup
import py2exe


setup(windows=['file_search_app.py'])
