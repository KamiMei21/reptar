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

from .common.by import By
from .common import utils
from .command import Command
from .webelement import WebElement
from .remote.remote_connection import RemoteConnection
from reptar.common.errorhandler import ErrorHandler
from .remote.switch_to import SwitchTo
from reptar.common.exceptions import WebDriverException


'''*********************************************
    ***APPLICATIONCACHE***    
*********************************************'''
class ApplicationCache(object):
    UNCACHED = 0
    IDLE = 1
    CHECKING = 2
    DOWNLOADING = 3
    UPDATE_READY = 4
    OBSOLETE = 5

    def __init__(self, driver):
        self.driver = driver #creates new Application Cache

    @property
    def status(self):
        return self.driver.execute(Command.GET_APP_CACHE_STATUS)['value'] #returns a current status of application cache


'''*********************************************
    ***SERVICE***    
*********************************************'''
class Service(object):
    #we may not need this. "provides an interface for x WebDriver to use with y"
    def __init__():
        pass

    @property
    def service_url(self):
        return "htttp://%s" % utils.join_host_port('localhost', self.port) #Gets the url of the Service

    def command_line_args(self):
        pass

    def start(self):
        pass #starts the service

    def assert_process_still_running(self):
        pass 

    def is_connectable(self):
        return utils.is_connectable(self.port)

    def send_remote_shutdown_command(self):
        pass

    def stop(self):
        pass #stops the service

    def __del__(self):
        pass


'''*********************************************
    ***OPTIONS***    
*********************************************'''    
class Options(object):
    def __init__(self):
        pass


'''*********************************************
    ***WEBDRIVER***    
*********************************************'''
class WebDriver(object):
    
    _web_element_cls = WebElement

    def __init__(self):
        pass

    def __repr__(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.quit()

 
    def start_client(self):
        pass  #called before starting new session (may be overriden to define custom startup behavior)

    def stop_client(self):
        pass #called after executing a quit command (may be overridden to define custom shutdown behavior)

    def start_session(self):
        pass #creates new session with desired capabilities    


    def execute(self, driver_command, params=None):
        pass #send command to be executed by a command.CommandExecutor
    
    def get(self, url): 
        self.execute(Command.GET, {'url': url}) #load web page in current browser session
    
    @property
    def title(self):  
        #return title of the current page
        resp = self.execute(Command.GET_TITLE)
        return resp['value'] if resp['value'] is not None else ""
        

    def find_element_by_id(self, id_):
        return self.find_element(by=By.ID, value= id_) #finds an element by id
 
    def find_element_by_xpath(self, xpath):
        return self.find_element(by=By.XPATH, value=xpath) #finds an element by xpath

    def find_element_by_link_text(self, link_text):
        return self.find_element(by=By.LINK_TEXT, value=link_text) #finds an element by link text

    def find_element_by_partial_link(self, link_text):
        return self.find_element(by=By.PARTIAL_LINK_TEXT, value=link_text) #finds an element by a partial match of its link text

    def find_element_by_name(self, name):
        return self.find_element(by=By.NAME, value=name) #finds an element by name
  
    def find_element_by_tag_name(self, name):
        return self.find_element(by=By.TAG_NAME, value=name) #finds an element by tag name

    def find_element_by_class_name(self, name):
        return self.find_element(by=By.CLASS_NAME, value=name) #finds an element by class name


    @property  
    def current_url(self):
        return self.execute(Command.GET_CURRENT_URL)['value'] #get URL of the current page

    @property
    def page_source(self):
        return self.execute(Command.GET_PAGE_SOURCE)['value'] #gets source of current page

    def close(self):
        self.execute(Command.CLOSE) #close current window

    def quit(self):
        #quits the driver and closes every associated window
        try:
            self.execute(Command.QUIT)
        finally:
            self.stop_client()


    #Window
    @property
    def current_window_handle(self):
        return self.execute(Command.GET_CURRENT_WINDOW_HANDLE)['value']
    @property

    def window_handles(self):
        return self.execute(Command.GET_WINDOW_HANDLES)['value']

    def maximize_window(self):
        params = None
        command = Command.MAXIMIZE_WINDOW
        params = {'windowHandle' : 'current'}
        self. execute(command, params)

    def fullscreen_window(self):
        self.execute(Command.FULLSCREEN_WINDOW)

    def minimize_window(self):
        self.execute(Command.MINIMIZE_WINDOW)


    # Target Locators
    @property
    def switch_to(self):
        return self._switch_to

    def switch_to_active_element(self):
        return self._switch_to.active_element #deprecated use driver.switch_to.active_element

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
        return self.execute(Command.GET_ALL_COOKIES)['value'] #returns a set of dictionaries, corresponding to cookies visible in the current session
    
    def get_cookie(self, name):
        cookies = self.get_cookies()
        for cookie in cookies:
            if cookie['name'] == name:
                return cookie #get a single cookie by name. returns the cookie in found, none if not
        return None 

    def delete_cookie(self, name):
        self.execute(Command.DELETE_COOKIE, {'name': name}) #deletes a single cookie with given name
    
    def delete_all_cookies(self):
        self.execute(Command.DELETE_ALL_COOKIES) #delete all cookies in the scope of the session

    def add_cookie(self, cookie_dict):
        self.execute(Command.ADD_COOKIE, {'cookie': cookie_dict}) #Adds a cookie to your current session.
    
    
    # Timeouts
    def implicitly_wait(self, time_to_wait):
        self.execute(Command.IMPLICIT_WAIT, {
                'ms': float(time_to_wait) * 1000})

    def set_script_timeout(self, time_to_wait):
        self.execute(Command.SET_SCRIPT_TIMEOUT, {
                'ms': float(time_to_wait) * 1000})

    def set_page_load_timeout(self, time_to_wait):
        self.execute(Command.SET_TIMEOUTS, {
                'ms': float(time_to_wait) * 1000,
                'type': 'page load'})

   
   #Find Elements
    def find_element(self, by=By.ID, value=None):
        return self.execute(Command.FIND_ELEMENT, {
            'using': by,
            'value': value})['value']

    def find_elements(self, by=By.ID, value=None):
        return self.execute(Command.FIND_ELEMENTS, {
            'using': by,
            'value': value})['value'] or []


    #Logs
    @property
    def log_types(self):
        return self.execute(Command.GET_AVAILABLE_LOG_TYPES)['value'] #gets a list of the available log types

    def get_log(self, log_type):
        return self.execute(Command.GET_LOG, {'type':log_type})['value'] #gets the log for given log type