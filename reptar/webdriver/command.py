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
from .remote.remote_connection import URI
from .webelements import Document

class Command(object):
    #defines constants for the standard WebDriver commands
    STATUS = "status"
    NEW_SESSION = "newSession"
    GET_ALL_SESSIONS = "getAllSessions"
    DELETE_SESSION = "deleteSession"
    CLOSE = "close"
    QUIT = "quit"
    GO_BACK = "goBack"
    GO_FORWARD = "goForward"
    REFRESH = "refresh"
    ADD_COOKIE = "addCookie"
    GET_COOKIE = "getCookie"
    GET_ALL_COOKIES = "getCookies"
    DELETE_COOKIE = "deleteCookie"
    DELETE_ALL_COOKIES = "deleteAllCookies"
    FIND_ELEMENT = "findElement"
    FIND_ELEMENTS = "findElements"
    FIND_CHILD_ELEMENT = "findChildElement"
    FIND_CHILD_ELEMENTS = "findChildElements"
    CLEAR_ELEMENT = "clearElement"
    SEND_KEYS_TO_ELEMENT = "sendKeysToElement"
    SEND_KEYS_TO_ACTIVE_ELEMENT = "sendKeysToActiveElement"
    SUBMIT_ELEMENT = "submitElement"
    UPLOAD_FILE = "uploadFile"
    GET_CURRENT_WINDOW_HANDLE = "getCurrentWindowHandle"
    GET_WINDOW_HANDLES = "getWindowHandles"
    GET_WINDOW_SIZE = "getWindowSize"
    GET_WINDOW_POSITION = "getWindowPosition"
    SET_WINDOW_SIZE = "setWindowSize"
    SET_WINDOW_RECT = "setWindowRect"
    GET_WINDOW_RECT = "getWindowRect"
    SET_WINDOW_POSITION = "setWindowPosition"
    SWITCH_TO_WINDOW = "switchToWindow"
    SWITCH_TO_FRAME = "switchToFrame"
    SWITCH_TO_PARENT_FRAME = "switchToParentFrame"
    GET_ACTIVE_ELEMENT = "getActiveElement"
    GET_TITLE = "getTitle"
    EXECUTE_SCRIPT = "executeScript"
    GET_ELEMENT_TEXT = "getElementText"
    GET_ELEMENT_VALUE = "getElementValue"
    GET_ELEMENT_TAG_NAME = "getElementTagName"
    SET_ELEMENT_SELECTED = "setElementSelected"
    IS_ELEMENT_SELECTED = "isElementSelected"
    IS_ELEMENT_ENABLED = "isElementEnabled"
    GET_ELEMENT_PROPERTY = "getElementProperty"
    SCREENSHOT = "screenshot"
    ELEMENT_SCREENSHOT = "elementScreenshot"
    IMPLICIT_WAIT = "implicitlyWait"
    EXECUTE_ASYNC_SCRIPT = "executeAsyncScript"
    SET_SCRIPT_TIMEOUT = "setScriptTimeout"
    SET_TIMEOUTS = "setTimeouts"
    MAXIMIZE_WINDOW = "windowMaximize"
    GET_LOG = "getLog"
    GET_AVAILABLE_LOG_TYPES = "getAvailableLogTypes"
    FULLSCREEN_WINDOW = "fullscreenWindow"
    MINIMIZE_WINDOW = "minimizeWindow"
    GET_ELEMENT_LOCATION = "getElementLocation"

    #Alerts
    DISMISS_ALERT = "dismissAlert"
    ACCEPT_ALERT = "acceptAlert"
    SET_ALERT_VALUE = "setAlertValue"
    GET_ALERT_TEXT = "getAlertText"
    SET_ALERT_CREDENTIALS = "setAlertCredentials"

    #HTML 5
    EXECUTE_SQL = "executeSql"

    GET_LOCATION = "getLocation"
    SET_LOCATION = "setLocation"

    GET_APP_CACHE = "getAppCache"
    GET_APP_CACHE_STATUS = "getAppCacheStatus"
    CLEAR_APP_CACHE = "clearAppCache"

    GET_LOCAL_STORAGE_ITEM = "getLocalStorageItem"
    REMOVE_LOCAL_STORAGE_ITEM = "removeLocalStorageItem"
    GET_LOCAL_STORAGE_KEYS = "getLocalStorageKeys"
    SET_LOCAL_STORAGE_ITEM = "setLocalStorageItem"
    CLEAR_LOCAL_STORAGE = "clearLocalStorage"
    GET_LOCAL_STORAGE_SIZE = "getLocalStorageSize"

    GET_SESSION_STORAGE_ITEM = "getSessionStorageItem"
    REMOVE_SESSION_STORAGE_ITEM = "removeSessionStorageItem"
    GET_SESSION_STORAGE_KEYS = "getSessionStorageKeys"
    SET_SESSION_STORAGE_ITEM = "setSessionStorageItem"
    CLEAR_SESSION_STORAGE = "clearSessionStorage"
    GET_SESSION_STORAGE_SIZE = "getSessionStorageSize"

    @staticmethod
    def find_referer(document):
        #TODO:  Have this referer behavior upon encountering a query string 
        #       configurable as a switch: 'SEND', 'PARTIAL', or 'DROP'  --MPC
        if (not document.address.query) and (not document.address.fragment):  
            return document.address.absolute()
        else:  return ''

    @staticmethod
    def traverse_anchor(fragment):
        pass

    @staticmethod
    def get(url, context, **kwargs):
        timeout = kwargs["timeout"] if "timeout" in kwargs else 60
        verify = kwargs["verify"] if "verify" in kwargs else False
        traversal = kwargs["traversal"] if "traversal" in kwargs else False
        url = url
        session = context.session
        document = context.window.curdoc
        req = None
        headers = {}
        uri = URI(url)
    
        #Did someone really just try to pass us a #fragment?
        if (uri.fragment != "") and (uri.absolute() == document.address.absolute()):
            traverse_anchor(uri.fragment)
        else:
            if document.address and traversal:
                headers["Referer"] = find_referer(document)
            if document.post_data:
                headers["Content-Type"] = document.post_content_type
                data = document.post_data["data"]
            else:  data = None
            
            req = session.get(str(uri), headers=headers, verify=verify, timeout=timeout, params=data)
            #TODO:  More robust Exception value  --MPC
            if req.status_code == 404:  raise Exception
            else:
                context.window.newdoc = Document(content=req.content, content_parse_mode=context.parse_mode, address=uri)
                context.cache.append(context.window.newdoc)
                
        context.sync.set()
    
    @staticmethod
    def get_page_source(context):
        context.sync.wait()
        return str(context.window.curdoc.content)
        
    @staticmethod
    def get_current_url(context):
        return str(context.window.curdoc.address)
