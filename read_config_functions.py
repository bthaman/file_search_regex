import configparser


def configsectionmap(fname, section):
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


def get_expressions(fname):
    f = open(fname, 'r')
    dict_expr = {}
    for line in f:
        m = re.match('(.*)=(.*)', line)
        if m:
            dict_expr[m.group(1).strip()] = m.group(2).strip()
    f.close()
    return dict_expr
