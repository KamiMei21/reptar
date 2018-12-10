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
import time
import subprocess
import html5lib

from io import StringIO
from contextlib import contextmanager
from threading import Thread, Event, current_thread
from queue import Queue

from reptar.common.errorhandler import ErrorHandler
from .remote.remote_connection import RemoteConnection
from .webelements import Window
from .command import Command


"""*********************************************
    ***WEBDRIVER OBJECT***    
*********************************************"""
class WebDriver(Thread):
    def __init__(self):
        super().__init__()
        self.q = Queue()
        self.hold = Event()
        self.session = RemoteConnection(self)
        self.window = Window(self)
        self.start()
        
    #Method to receive a request from a child object
    #Why bubbles instead of queues?  I don't want the command queue cluttered
    #with anything besides direct user requests, for one.  For another, the queues
    #would end up being passed pretty deep.  --MPC
    def bubble_option(self, func, params):
        getattr(self, func)(**params)
        
    def get(self, uri):
        self.hold.clear()
        self.q.put((Command.get, {"uri": uri}))
        
    def post(self, uri):
        self.hold.clear()
        self.q.put((Command.post, {"uri": uri}))
        
    def close(self):
        self.hold.wait()
        self.q.put(Command.QUIT)
        
    def quit(self):
        self.hold.clear()
        self.session.close()
        del self.session
        del self.window
        del self.hold
        del self.q
        
    @property
    def page_source(self):
        self.hold.wait()
        return self.window.curdoc.content
        
    def find_element_by_id(self, element_id):
        self.hold.wait()
        return Command.find_element(key="id", value=element_id, context=self)
        
    def run(self):
        while True:
            cmd = self.q.get()
            if not cmd or cmd == Command.QUIT:  break
            else:
                if isinstance(cmd,tuple):
                    if isinstance(cmd[1], dict):  cmd[0](**cmd[1], context=self)
                    else:  cmd[0](cmd[1], context=self)
                else:  cmd[0](context=self)
                
                if self.window.is_different():  self.window.swap_doc()
                self.hold.set()
        
        self.quit()
        return True
