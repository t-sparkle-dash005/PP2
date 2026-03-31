from configparser import ConfigParser  # <--- This line is mandatory

def load_config(filename='database.ini', section='postgresql'):
    # Now ConfigParser() will work
    parser = ConfigParser()
    parser.read(filename, encoding='utf-8')
    
    # ... rest of your code

    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return config