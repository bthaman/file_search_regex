import fnmatch
import file_dir_dialog as fdd
import pandas as pd
import msgbox
import time
from datetime import date
from read_config_functions import *
import os


def find_files(directory, pattern, dt1=None, dt2=None):
    dt1_default = '1900-01-01'
    dt2_default = date.today().strftime('%Y-%m-%d')
    dt1 = dt1_default if dt1 is None else dt1
    dt2 = dt2_default if dt2 is None else dt2
    for root, dirs, files in os.walk(directory):
        # root: current directory, type string
        # dirs: list of directories within root
        # files: list of files within root
        for basename in files:
            # attempt match using regex; if failure, use fnmatch
            # note that case is ignored
            try:
                re_pattern = re.compile(pattern, re.IGNORECASE)
                matched = re_pattern.match(basename)
            except Exception:
                matched = fnmatch.fnmatch(basename, pattern)
            try:
                file = os.path.join(root, basename)
            except TypeError:
                return None
            # get the last modified date. a PermissionError might be thrown; if so, keep going
            try:
                dtmod = time.strftime('%Y-%m-%d', time.localtime(os.path.getmtime(file)))
            except PermissionError:
                dtmod = None
            except FileNotFoundError:
                dtmod = None

            if dtmod and matched and dt1 <= dtmod <= dt2:
                size = os.path.getsize(file)
                extension = os.path.splitext(file)[1][1:]
                lastmod = time.strftime('%Y-%m-%d %H:%M', time.localtime(os.path.getmtime(file)))
                # another way --> lastmod = time.ctime(os.path.getmtime(filename))
                # yield turns the function into a generator (form of iterator)
                yield file, root, basename, extension, size, lastmod


def find_dirs(directory, pattern):
    for root, dirs, files in os.walk(directory):
        # root: current directory, type string
        # dirs: list of directories within root
        # files: list of files within root
        lastdir = root.split('\\')[-1] if '\\' in root else ''
        try:
            re_pattern = re.compile(pattern, re.IGNORECASE)
            matched = re_pattern.match(lastdir)
        except Exception:
            matched = fnmatch.fnmatch(lastdir, pattern)
        if matched:
            yield root


def search_dir_topdown(pattern, filename, dt1=None, dt2=None):
    try:
        fn = os.path.join(os.getcwd(), 'file_search.config')
        last_dir = configsectionmap(fn, 'last path')
        # create dataframe from generator, tweak it, write to excel
        dir_selected = fdd.get_directory(last_dir)
        # be sure directory is not None type, and that it exists before setting last path
        if dir_selected and os.path.isdir(dir_selected):
            update_setting(fn, 'last path', 'last', dir_selected)
        if not dir_selected:
            return
        df = pd.DataFrame(find_files(dir_selected, pattern, dt1, dt2), columns=['file', 'directory', 'filename',
                                                                                'extension', 'file_size', 'lastmod'])
        df['directory'] = '=HYPERLINK("' + df['directory'] + '")'
        df['filename'] = '=HYPERLINK("' + df['file'] + '", "' + df['filename'] + '")'
        df = df[['directory', 'filename', 'extension', 'file_size', 'lastmod']]
        if df.shape[0] == 0:
            msgbox.show_message('Bummer', 'No files found using that expression')
            return
        filename = os.path.splitext(filename)[0]
        df.to_excel(filename + '.xlsx', index=False)
        os.startfile(filename + '.xlsx')
    except PermissionError:
        msgbox.show_error('Permission Error', filename + '.xlsx already open')
    except Exception as e:
        msgbox.show_error('Error', e)


def search_dir_only(pattern, filename):
    try:
        fn = os.path.join(os.getcwd(), 'file_search.config')
        last_dir = configsectionmap(fn, 'last path')
        dir_selected = fdd.get_directory(last_dir)
        if not dir_selected:
            return
        df = pd.DataFrame(find_dirs(dir_selected, pattern), columns=['Directory'])
        df['Directory'] = '=HYPERLINK("' + df['Directory'] + '")'
        if df.shape[0] == 0:
            msgbox.show_message('Bummer', 'No directories found using that expression')
            return
        filename = os.path.splitext(filename)[0]
        df.to_excel(filename + '.xlsx', index=False)
        os.startfile(filename + '.xlsx')
    except PermissionError:
        msgbox.show_error('Permission Error', filename + '.xlsx already open')
    except Exception as e:
        msgbox.show_error('Error', e)


if __name__ == "__main__":
    import sys
    pttn = sys.argv[1] if len(sys.argv) > 1 else '.*proj.*'
    fn = sys.argv[2] if len(sys.argv) > 2 else 'search_results'
    search_dir_topdown(pttn, fn, dt1=None, dt2=None)
