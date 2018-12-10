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
import socket
import string
import urllib

import requests

from reptar.common.useragent import user_agent_strings

#Wrapper class for Requests
class RemoteConnection(object):
    def __init__(self, parent=None, user_agent="BSD Lynx"):
        self.parent = parent
        self.user_agent = user_agent_strings[user_agent]
        self.session = requests.Session()
        requests.packages.urllib3.disable_warnings()
        self.session.headers.update({"User-Agent": self.user_agent, "Accept": "image/gif,image/jpeg,image/pjpeg,application/x-ms-application,application/xaml+xml,application/x-ms-xbap,*/*", "Accept-Language": "en-US,en;q=0.5", "Cache-Control": "no-cache"})

    def close(self):
        self.session.close()
        
    def get(self, url, timeout, verify, headers, params):
        if not headers:  headers=self.session.headers
        return self.session.get(url, timeout=timeout, verify=verify, headers=headers, params=params)
        
    @property
    def headers(self):
        return self.session.headers
        
    def request(self, method, url, timeout, verify, headers, data, files):
        if not headers:  headers=self.session.headers
        return self.session.request(method, url, timeout=timeout, verify=verify, headers=headers, data=data, files=files)

#Lovingly borrowed from Lynx - please wrap, don't modify
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
    
    @property
    def absolute(self):
        return ''.join([self.protocol, "://", self.URL, self.URN])
    
    def urljoin(self, url):
        return urllib.parse.urljoin(self.absolute, url, allow_fragments=False)
        
    def __repr__(self):
        return ''.join([self.protocol, "://", self.URL, ':' , str(self.port), self.URN, self.query, self.fragment])
