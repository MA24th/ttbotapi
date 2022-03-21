# -*- coding: utf-8 -*-

"""
ttbotapi.utils.api_handler
~~~~~~~~~~~~~~~~~~~~~~~~~~
This submodule provides api handler functions that are consumed internally
:copyright: (c) 2022 by Mustafa Asaad.
:license: GPLv2, see LICENSE for more details.
"""

import threading
import requests
from .logger import logger
from .api_exceptions import ApiException


thread_local = threading.local()


def per_thread(key, construct_value, reset=True):
    if reset or not hasattr(thread_local, key):
        value = construct_value()
        setattr(thread_local, key, value)

    return getattr(thread_local, key)


def get_req_session(reset=True):
    return per_thread('req_session', lambda: requests.session(), reset)


def make_request(http_method, api_method, api_url, params=None, files=None, json_body=None, proxies=None):
    """
    Makes a request to the TamTam API
    :param str http_method: HTTP method ['get', 'post', 'put', 'delete']
    :param str api_method: Name of the API method to be called. (E.g. 'me')
    :param str api_url: tamtam api url for api_method
    :param dict or None params: Should be a dictionary with key-value pairs
    :param any data: body content's a data
    :param any files: files content's a data
    :param dict or None json_body: Should be a dictionary with key-value pairs
    :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy
    :return: json
    :rtype: json
    """
    logger.info(f"Request -> http_method='{http_method}' api_method='{api_method}' params={params} files={files}")
    timeout = 14.99
    if params:
        if 'timeout' in params:
            timeout = params['timeout'] + 10

    resp = requests.request(method=http_method, url=api_url, params=params, data=None, headers=None, cookies=None,
                            files=files, auth=None, timeout=timeout, allow_redirects=False, proxies=proxies, hooks=None,
                            stream=None, verify=None, cert=None, json=json_body)

    if resp.status_code != 200:
        raise ApiException(f"The Server Returned {resp.json()} ", api_method, resp)
    else:
        logger.info(f"Response -> {resp.json()}")
        return resp.json()
