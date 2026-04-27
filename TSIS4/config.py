# config.py
from configparser import ConfigParser

def load_config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    
    # Using utf-8-sig handles hidden Windows characters and encoding issues
    try:
        with open(filename, 'r', encoding='utf-8',errors='replace') as f:
            parser.read_file(f)
    except FileNotFoundError:
        raise Exception(f"{filename} not found. Please create it.")

    if parser.has_section(section):
        params = parser.items(section)
        return {param[0]: param[1].strip() for param in params} # .strip() removes hidden spaces
    else:
        raise Exception(f'Section {section} not found in {filename}')

# Load the parameters once
params = load_config()

# Construct the URL safely
DATABASE_URL = f"postgresql://{params['user']}:{params['password']}@{params['host']}/{params['database']}"