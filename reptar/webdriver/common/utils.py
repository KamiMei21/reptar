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

import socket
from reptar.webdriver.common.keys import Keys

basestring = str

def free_port():
    #determines free port using sockets
    pass

def find_connectable_ip():
    #resolve hostname to IP
    pass

def join_host_port():
    #joins hostname and port together
    pass

def is_connectable():
    #tries to connect to the server at port 
    pass

def is_url_connectable():
    #try to connect to http server at /status path
    pass

def keys_to_typing(value):
    #processes the values that will be typed in the element
    typing = []
    for val in value:
        if isinstance(val, Keys):
            typing.append(val)
        elif isinstance(val, int):
            val = str(val)
            for i in range(len(val)):
                typing.append(val[i])
        else:
            for i in range(len(val)):
                typing.append(val[i])
    return typing