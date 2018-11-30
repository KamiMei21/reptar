'''
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
'''

import base64
import logging
import platform
import socket
import string
import urllib3


from urllib import parse #for py3+

LOGGER = loggin.getLogger(__name__)

class RemoteConnection(pbject):
    _timeout = socket._GLOBAL_DEFAULT_TIMEOUT

    @classmethod
    def get_timeout(cls):
        return None if cls._timeout == socket._GLOBAL_DEFAULT_TIMEOUT else cls._timeout

    @classmethod
    def set_timeout(cls):
        cls._timeout = _timeout

    @classmethod
    def reset_timeout(cls):
        cls._timeout = socket._GLOBAL_DEFAULT_TIMEOUT

    @classmethod
    def get_remote_connection_headers(cls, parsed_url, keep_alive = False):
        #get headers for remote request
        pass


    def __init__(self, remote_server_addr, keep_alive = False, resolve_ip = True):
        #try to resolve hostname & get IP
        pass

    def execute(self, command, params):
        #send command to remote server
        pass


    def _request(self, method, url, body = None):
        #send http request to remote server
        pass
    