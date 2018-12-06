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
import warnings
import base64
import copy
import warnings
import time
import errno
import platform
import subprocess

from subprocess import PIPE
from contextlib import contextmanager
from threading import Thread, Event, current_thread
from queue import Queue

from .command import Command
from .webelements import Window, Document
from .remote.remote_connection import RemoteConnection
from reptar.common.errorhandler import ErrorHandler
from reptar.common.useragent import user_agent_strings


"""*********************************************
    ***OPTIONS***    
*********************************************"""    
class Options(object):
    def __init__(self):
        pass

"""*********************************************
    ***WEBDRIVER OBJECT***    
*********************************************"""
class WebDriver(Thread):
    def __init__(self, user_agent="BSD Lynx", parse_mode="lxml", window=None):
        self.parent = current_thread()
        super().__init__()
        self.user_agent = user_agent_strings[user_agent]
        self.parse_mode = parse_mode
        self.window = window or Window()
        self.cache = []
        self.queue = Queue()
        self.start_client()
        self.sync = Event()

    def __repr__(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.quit()

    #send command to be executed by a command.CommandExecutor
    def execute(self, driver_command, params=None):
        if params:  self.queue.put((driver_command, params))
        else:  self.queue.put(driver_command)

    def start_client(self):
        #called before starting new session 
        #(may be overriden to define custom startup behavior)
        self.start_session()
        self.start()

    def stop_client(self):
        #(may be overridden to define custom shutdown behavior)
        self.session.close()

    #creates new session with desired capabilities    
    def start_session(self):
        self.session = RemoteConnection()
        self.session.headers.update({"User-Agent": self.user_agent, "Accept": "image/gif,image/jpeg,image/pjpeg,application/x-ms-application,application/xaml+xml,application/x-ms-xbap,*/*", "Accept-Language": "en-US,en;q=0.5", "Cache-Control": "no-cache"})
    
    #load web page in current browser session
    def get(self, url): 
        self.execute(Command.get, {"url": url})
    
    #return title of the current page
    @property
    def title(self):  
        pass
        
    #finds an element by id
    def find_element_by_id(self, id_):
        self.find_element(id_) 
 
    #finds an element by xpath
    def find_element_by_xpath(self, xpath):
        self.find_element(xpath)

    #finds an element by link text
    def find_element_by_link_text(self, link_text):
        self.find_element(link_text)

    #finds an element by a partial match of its link text
    def find_element_by_partial_link(self, link_text):
        self.find_element(link_text)

    #finds an element by name
    def find_element_by_name(self, name):
        self.find_element(name)
  
    #finds an element by tag name
    def find_element_by_tag_name(self, name):
        self.find_element(name)

    #finds an element by class name
    def find_element_by_class_name(self, name):
        self.find_element(name)

    @property  
    def current_url(self):
        #get URL of the current page
        return Command.get_current_url(self)

    @property
    def page_source(self):
        #gets source of current page
        return Command.get_page_source(self)

    #close current window
    def close(self):
        self.cache = []
        self.stop_client()

    #quits the driver and closes every associated window
    def quit(self):
        self.close()
        self.execute(Command.QUIT)

    #Window
    @property
    def current_window_handle(self):
        self.execute(Command.GET_CURRENT_WINDOW_HANDLE)
    
    @property
    def window_handles(self):
        self.execute(Command.GET_WINDOW_HANDLES)

    def maximize_window(self):
        params = None
        command = Command.MAXIMIZE_WINDOW
        params = {"windowHandle": "current"}
        self.execute(command, params)

    def fullscreen_window(self):
        self.execute(Command.FULLSCREEN_WINDOW)

    def minimize_window(self):
        self.execute(Command.MINIMIZE_WINDOW)

    #deprecated use driver.switch_to.active_element
    def switch_to_active_element(self):
        return self._switch_to.active_element

    def switch_to_window(self, window_name):
        self._switch_to.window(window_name)

    def switch_to_frame(self, frame_reference):
        self._switch_to.frame(frame_reference)

    def switch_to_default_content(self):
        self._switch_to.default_content()

    def switch_to_alert(self):
        return self._switch_to.alert

    # Navigation
    def back(self):
        self.execute(Command.GO_BACK)
    def forward(self):
        self.execute(Command.GO_FORWARD)
    def refresh(self):
        self.execute(Command.REFRESH)

    # Options[COOKIES]
    def get_cookies(self):
        #returns a set of dictionaries, 
        #corresponding to cookies visible in the current session
        return self.execute(Command.GET_ALL_COOKIES)
    
    def get_cookie(self, name):
        cookies = self.get_cookies()
        for cookie in cookies:
            if cookie["name"] == name:
                #get a single cookie by name. 
                #returns the cookie in found, none if not
                return cookie 
        
        return None 

    #deletes a single cookie with given name
    def delete_cookie(self, name):
        self.execute(Command.DELETE_COOKIE, {"name": name})
    
    #delete all cookies in the scope of the session
    def delete_all_cookies(self):
        self.execute(Command.DELETE_ALL_COOKIES)

    #Adds a cookie to your current session.
    def add_cookie(self, cookie_dict):
        self.execute(Command.ADD_COOKIE, {"cookie": cookie_dict})

    # Timeouts
    def implicitly_wait(self, time_to_wait):
        self.execute( Command.IMPLICIT_WAIT, { 
                "ms":  float(time_to_wait) * 1000 } )

    def set_script_timeout(self, time_to_wait):
        self.execute( Command.SET_SCRIPT_TIMEOUT, { 
                "ms":  float(time_to_wait) * 1000 } )

    def set_page_load_timeout(self, time_to_wait):
        self.execute( Command.SET_TIMEOUTS, { 
                "ms":  float(time_to_wait) * 1000,
                "type":  "page load" } )

   #Find Elements
    def find_element(self, by=None, value=None):
        self.execute( Command.FIND_ELEMENT, { 
            "using":  by,
            "value":  value } )

    def find_elements(self, by=None, value=None):
        self.execute( Command.FIND_ELEMENTS, { 
            "using":  by,
            "value":  value } )

    #Logs
    @property
    def log_types(self):
        #gets a list of the available log types
        pass

    #gets the log for given log type
    def get_log(self, log_type):
        pass
        
    def run(self):
        while True:
            cmd = self.queue.get()
            if not cmd or cmd is Command.QUIT:  break
            else:  
                if isinstance(cmd, tuple):  cmd[0](context=self, **cmd[1])
                else:  cmd(context=self)
                
                #Did that command affect our document structure?
                if Document.are_different(self.window.curdoc, self.window.newdoc):
                    self.window.curdoc = self.window.newdoc; self.window.newdoc = None
                
        return True
