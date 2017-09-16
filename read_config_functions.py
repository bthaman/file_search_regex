import configparser
import re


def configsectionmap(fname, section):
    """returns a dictionary of all settings in a configuration file section"""
    dict1 = {}
    config = configparser.RawConfigParser()
    config.optionxform = lambda option: option
    config.read(filenames=fname)
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option, raw=True)
            if dict1[option] == -1:
                print("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1


def update_setting(fname, section, setting, value):
    """creates (if doesn't exist) or updates (if does exist) a setting in an existing section"""
    config = configparser.RawConfigParser()
    config.read(fname)
    config.set(section, setting, value)
    with open(fname, 'w') as configfile:
        config.write(configfile)


def get_expressions(fname):
    """gets all settings in a config file. does not return by section"""
    f = open(fname, 'r')
    dict_expr = {}
    for line in f:
        m = re.match('(.*)=(.*)', line)
        if m:
            dict_expr[m.group(1).strip()] = m.group(2).strip()
    f.close()
    return dict_expr

if __name__ == '__main__':
    import os
    fn = os.path.join(os.getcwd(), 'file_search.config')
    update_setting(fn, 'named expressions', 'any ole file', '.*')
