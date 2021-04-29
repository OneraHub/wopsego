from __future__ import print_function

# Python 2 and 3: easiest option for request
from future.standard_library import install_aliases

install_aliases()

import os
import sys
import json
import re
import requests
import numpy as np

from urllib.parse import urlparse, urlencode


from wopsego import __version__

WHATSOPT_DIRNAME = os.path.join(os.path.expanduser("~"), ".whatsopt")
API_KEY_FILENAME = os.path.join(WHATSOPT_DIRNAME, "api_key")
URL_FILENAME = os.path.join(WHATSOPT_DIRNAME, "url")

PROD_URL = "https://ether.onera.fr/whatsopt"
WOP_MINIMAL_VERSION = "1.0"


class WhatsOptLoginRequiredError(Exception):
    pass


class WhatsOpt(object):
    def __init__(self):
        if os.path.exists(URL_FILENAME):
            with open(URL_FILENAME, "r") as f:
                self._url = f.read()
        else:
            self._url = self.default_url

        # config session object
        self.session = requests.Session()
        urlinfos = urlparse(self._url)
        self.session.trust_env = re.match(r"\w+.onera\.fr", urlinfos.netloc)
        self.headers = {}

        if not self.check_login():
            raise WhatsOptLoginRequiredError(
                "You need to log in with wop before using WhatsOpt SEGOMOE API"
            )

    @property
    def url(self):
        return self._url

    def endpoint(self, path):
        return self._url + path

    @staticmethod
    def err_msg(resp):
        error(
            "{} ({}) : {}".format(
                resp.status_code,
                requests.status_codes._codes[resp.status_code][0],
                resp.json()["message"],
            )
        )

    @property
    def default_url(self):
        self._default_url = PROD_URL
        return self._default_url

    @staticmethod
    def _read_api_key():
        with open(API_KEY_FILENAME, "r") as f:
            api_key = f.read()
            return api_key

    def check_login(self):
        ok = False

        if os.path.exists(API_KEY_FILENAME):
            test_api_key = self._read_api_key()

        if test_api_key:
            self.headers = {
                "Authorization": "Token token=" + test_api_key,
            }
            url = self.endpoint("/api/v1/versioning")
            try:
                resp = self.session.get(url, headers=self.headers)
                return resp.ok
            except requests.exceptions.ConnectionError:
                return False
        else:
            return False
