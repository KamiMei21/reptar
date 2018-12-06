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
import hashlib
import os
import pkgutil
import warnings
import zipfile

from io import BytesIO as IOStream 
from bs4 import BeautifulSoup

from reptar.common.exceptions import WebDriverException



"""*********************************************
    ***HTML DOCUMENT OBJECT***    
*********************************************"""    
class Document(object):
    def __init__(self, content=None, content_parse_mode="lxml", post_content_type="", post_data={"data": '', "files": ''}, address=""):
        self.line_count        = 0
        self.content           = BeautifulSoup(content, content_parse_mode) if content else ''
        self.post_content_type = post_content_type
        self.post_data         = post_data
        self.address           = address
        self.focus_element     = None
        
    @staticmethod
    def are_different(doc1, doc2):
        if (not isinstance(doc1, Document)) or (not isinstance(doc2, Document)):
            return True
        if (doc1.address != doc2.address):
            return True
        if (doc1.post_data != doc2.post_data):
            return True
        
        return False
        
class Window(object):
    def __init__(self, resolution=(1280, 720), font_size=12, zoom_level=100, curdoc=None):
        self.resolution = resolution
        self.font_size  = font_size
        self.zoom_level = zoom_level
        self.cursor     = 0
        self.buffer     = None
        self.curdoc     = curdoc or Document()
        self.newdoc     = None

class WebElement(object):
    def __init__(self, parent, id_):
        self._parent = parent
        self._id = id_

    def __repr__(self):
        #?
        pass

    #this element's 'tagName' property
    @property
    def tag_name(self):
        pass

    #the text of the element
    @property
    def text(self):
        pass
    
    #clicks the element
    def click(self):
        pass

    #submits a form
    def submit(self):
        pass

    #clear text if it's a text entry element
    def clear(self):
        pass

    #gets given attribute or property of the element
    def get_attribute(self,name): 
        pass
    
    #returns whether element is selected
    def is_selected(self):
        pass

    #returns whether the element is enabled
    def is_enabled(self): 
        pass

    #find element within this element's chilcdren by ID
    def find_element_by_id(self, id_):
        return self.find_element(id_)

    #finds a list of elements within this element's children by ID
    def find_elements_by_id(self, id_):
        return self.find_elements(id_)

    #finds elements within this element's children by name
    def find_element_by_name(self, name):
        return self.find_element(name)
     
    #finds a list of elements within this element's children by name
    def find_elements_by_name(self, name):
        return self.find_elements(name)
        
    #finds element within this element's children by visible link text
    def find_element_by_link_text(self, link_text):
        return self.find_element(link_text)

    #finds a list of elements within this element's children 
    #by visible link text
    def find_elements_by_link_text(self, link_text):
        return self.find_elements(link_text)
    
    #finds element within this element's children by partially visible link text
    def find_element_by_partial_link_text(self, link_text):
        return self.find_element(link_text)
    
    #finds a list of elements within this element's children by link text
    def find_elements_by_partial_link_text(self, link_text):
        return self.find_elements(link_text)
    
    #finds element within this element's children by tag name
    def find_element_by_tag_name(self, name):
        return self.find_element(name)
    
    #finds a list of elements within this element's children by tag name
    def find_elements_by_tag_name(self, name):
        return self.find_elements(name)
    
    #finds element by xpath
    def find_element_by_xpath(self, xpath):
        return self.find_element(xpath)
    
    #finds elements within the element by xpath
    def find_elements_by_xpath(self, xpath):
        return self.find_elements(xpath)
    
    #finds element within this element's children by class name
    def find_element_by_class_name(self, name):
        return self.find_element(name)
    
    #finds a list of elements within this element's childrn by class name
    def find_elements_by_class_name(self, name):
        return self.find_elements(name)
    
    def send_keys(self, *value):
        pass

    @property
    def location(self):
        pass

    #saves screenshot of the current element to PNG.
    @property
    def screenshot(self, filename):
        pass

    #Internal reference to the WebDriver instance this element was found from
    @property
    def parent(self):
        return self._parent

    #Internal ID
    @property
    def id(self):
        return self._id

    
    def __eq__(self):
        #?
        pass

    def __ne__(self):
        #?
        pass

    #executes a command against the underlying HTML element
    def _execute(self, command, params=None):
        if not params:
            params = {}
        params["id"] = self._id
        pass

    #find an element given a By strategy and locator
    def find_element(self, by=None, value=None):
        pass

    #find elements given a By strategy and locator
    def find_elements(self, by=None, value=None):
        pass

    def __hash__(self):
        #?
        pass

    def _upload(self):
        pass
