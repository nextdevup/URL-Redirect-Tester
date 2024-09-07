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

def should_use_head_requests():
    use_head_request = False

    try:
        config.read('settings.ini')
        use_head_request = config.getboolean('DEFAULT', 'UseHEADRequests')
    except Exception as ex:
        print(ex)
        use_head_request = False

    return use_head_request

def should_use_session():
    use_session = True

    try:
        config.read('settings.ini')
        use_session = config.getboolean('DEFAULT', 'PersistSession')
    except Exception as ex:
        print(ex)
        use_session = True

    return use_session