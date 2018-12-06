"""
Reptar - a headless Python-native webdriver
2018

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import base64
import logging
import platform
import socket
import string
import urllib

import requests


LOGGER = logging.getLogger(__name__)


class RemoteConnection(requests.Session):
    _timeout = socket._GLOBAL_DEFAULT_TIMEOUT

    @classmethod
    def get_timeout(cls):
        if cls._timeout == socket._GLOBAL_DEFAULT_TIMEOUT:  return None
        else:  return cls._timeout

    @classmethod
    def set_timeout(cls):
        cls._timeout = _timeout

    @classmethod
    def reset_timeout(cls):
        cls._timeout = socket._GLOBAL_DEFAULT_TIMEOUT

    @classmethod
    def get_remote_connection_headers(cls, parsed_url, keep_alive=False):
        #get headers for remote request
        pass


    def __init__(self):
        super().__init__()
        requests.packages.urllib3.disable_warnings()


class URI(object):    
    def __init__(self, uri_string):
        uri = urllib.parse.urlparse(uri_string)
        self.protocol = uri.scheme
        self.URL = uri.netloc
        self.URN = uri.path
        self.query = ("?" + uri.query) if uri.query else ""
        self.fragment = ("#" + uri.fragment) if uri.fragment else ""
        if uri.port:  self.port = uri.port
        else:
            if self.protocol == "http":  self.port = 80
            if self.protocol == "https":  self.port = 443
    
    def absolute(self):
        return ''.join([self.protocol, "://", self.URL, self.URN])
    
    def urljoin(self, url):
        return urllib.parse.urljoin(self.absolute(), url, allow_fragments=False)
        
    def __repr__(self):
        return ''.join([self.protocol, "://", self.URL, ':' , str(self.port), self.URN, self.query, self.fragment])
