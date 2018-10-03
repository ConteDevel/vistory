# Create a SSL context to accept not-trusted certificates
import json
import ssl
import urllib.request
from base64 import b64encode

import urllib3

untrusted_ssl_ctx = ssl.create_default_context()
untrusted_ssl_ctx.check_hostname = False
untrusted_ssl_ctx.verify_mode = ssl.CERT_NONE

http = urllib3.PoolManager(cert_reqs=ssl.CERT_NONE)


def to_basic(username, password):
    # Create a header for the basic authorization
    client_id_secret = username + ":" + password
    return "Basic " + b64encode(bytes(client_id_secret, 'ascii')).decode('ascii')


def get_auth_header(auth):
    if auth:
        # Create a header for the authorization
        return {'Authorization': auth}
    return {}


def get_content(response):
    return json.loads(response.data.decode('utf-8')), response.data.status


def get(url, auth=None):
    auth_header = get_auth_header(auth)
    response = http.request('GET', url, headers=auth_header)
    return get_content(response)


def post(url, fields=None, body=None, auth=None):
    auth_header = get_auth_header(auth)
    response = http.request('POST', url, headers=auth_header, fields=fields, body=body)
    return get_content(response)
