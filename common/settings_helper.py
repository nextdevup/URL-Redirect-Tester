import configparser

config = configparser.ConfigParser()

def get_max_redirects():
    max_redirects = 0

    try:
        config.read('settings.ini')
        max_redirects = int(config['DEFAULT']['RedirectLimit'])
    except Exception as ex:
        max_redirects = 0

    return max_redirects

def get_max_urls():
    max_urls = 0

    try:
        config.read('settings.ini')
        max_urls = int(config['DEFAULT']['LinkLimit'])
    except Exception as ex:
        max_urls = 0

    return max_urls

def get_request_headers():
    headers = {}

    try:
        config.read('settings.ini')
        headers = {'User-agent': config['DEFAULT']['UserAgent']}
    except Exception as ex:
        headers = {}

    return headers

def should_use_session():
    use_session = True

    try:
        config.read('settings.ini')
        use_session = bool(config['DEFAULT']['PersistSession'])
    except Exception as ex:
        use_session = True

    return use_session