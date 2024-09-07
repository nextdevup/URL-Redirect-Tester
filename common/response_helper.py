import re
import requests
from models.Session import Session as Sess
from urllib.parse import urlparse, urljoin
from common.extensions import is_empty_string
from common.settings_helper import get_request_headers, should_use_head_requests, should_use_session

def get_domain(domain):
    if not is_empty_string(domain) and not bool(re.match("http", domain, re.I)):
        domain = f'https://{domain}'

    return domain

def get_domain_from_url(url):
    parsedURL = urlparse(url)
    domain = parsedURL.hostname

    return get_domain(domain)

def get_fixed_url(url, domain):
    parsedURL = urlparse(str(url).strip())

    if not domain == "" and not domain.isspace() and domain not in parsedURL.path and parsedURL.netloc == '':
        domain = get_domain(domain)
        parsedURL = urlparse(urljoin(domain, parsedURL.geturl()))
        parsedURL._replace(netloc=domain)

    if parsedURL.scheme == '' or parsedURL.scheme == 'http':
        parsedURL._replace(scheme='https')

    return parsedURL.geturl()

def get_redirect_from_response(resp: requests.Response, domain):
    if "Location" in resp.headers:
        redirect = resp.headers["Location"].strip()
        redirect = get_fixed_url(redirect, domain)
    else:
        redirect = f'No Redirect -- Status Code: {resp.status_code}'

    return redirect

def is_valid_url(url):
    try:
        parsedURL = urlparse(url)
        return bool(parsedURL.scheme and parsedURL.netloc)
    except:
        return False
    
def make_request(url):
    if should_use_session():
        if should_use_head_requests():
            return Sess().get_session().head(url, headers=get_request_headers(), allow_redirects=False, verify=False)
        else:
            return Sess().get_session().get(url, headers=get_request_headers(), allow_redirects=False, verify=False)
    else:
        if should_use_head_requests():
            return requests.head(url, headers=get_request_headers(), allow_redirects=False, verify=False)
        else:
            return requests.get(url, headers=get_request_headers(), allow_redirects=False, verify=False)
        
import requests