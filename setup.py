"""
used this version for py2exe
with this version, a command window does not open when the .exe is executed

IMPORTANT NOTE:
  changed the openpyxl __init__.py file to work around an error
  location: C:\Users\wjt\AppData\Local\Continuum\Anaconda3\envs\python3.4\Lib\site-packages\openpyxl
  changed to below:

    import json
    import os


    __author__ = "See AUTHORS",
    __author_email__ = "eric.gazoni@gmail.com",
    __license__ = "MIT/Expat",
    __maintainer_email__ = "openpyxl-users@googlegroups.com",
    __url__ = "http://openpyxl.readthedocs.org",
    __version__ = "2.3.2"

    # Imports for the openpyxl package.
    from openpyxl.xml import LXML

    from openpyxl.workbook import Workbook
    from openpyxl.reader.excel import load_workbook
"""
from distutils.core import setup
import py2exe


setup(windows=['file_search_app.py'])
