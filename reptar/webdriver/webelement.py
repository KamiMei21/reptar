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
import hashlib
import os
import pkgutil
import warnings
import zipfile

from reptar.common.exceptions import WebDriverException
from reptar.webdriver.common.by import By
from reptar.webdriver.common.utils import keys_to_typing
from .command import Command

from io import BytesIO as IOStream #it's either this or "from StringIO import StringIO as IOStream"



class WebElement(object):
    def __init__(self, parent, id_):
        self._parent = parent
        self._id = id_


    def __repr__(self):
        #?
        pass


    @property
    def tag_name(self):
        #this element's 'tagName' property
        pass

    @property
    def text(self):
        return self._execute(Command.GET_ELEMENT_TEXT)['value'] #the text of the element
    
    def click(self):
        self._execute(Command.CLICK_ELEMENT) #clicks the element

    def submit(self):
        self._execute(Command.SUBMIT_ELEMENT) #submits a form

    def clear(self):
        self._execute(Command.CLEAR_ELEMENT)  #clear text if it's a text entry element

    def get_attribute(self,name): 
        attributeValue = ''
        resp = self._execute(Command.GET_ELEMENT_ATTRIBUTE, {'name': name})
        attributeValue = resp.get('value')
        if attributeValue is not None:
            if name != 'value' and attributeValue.lower() in ('true', 'false'):
                attributeValue = attributeValue.lower()
        return attributeValue #gets given attribute or property of the element
    
    def is_selected(self:
        return self._execute(Command.IS_ELEMENT_SELECTED)['value']  #returns whether element is selected

    def is_enabled(self): 
        return self._execute(Command.IS_ELEMENT_ENABLED)['value'] #returns whether the element is enabled

    def find_element_by_id(self, id_):
        return self.find_element(by=By.ID, value=id_) #find element within this element's chilcdren by ID

    def find_elements_by_id(self, id_):
        return self.find_elements(by=By.ID, value=id_) #finds a list of elements within this element's children by ID

    def find_element_by_name(self, name):
        return self.find_element(by=By.NAME, value=name) #finds elements within this element's children by name
     
    def find_elements_by_name(self, name):
        return self.find_elements(by=By.NAME, value=name) #finds a list of elements within this element's children by name
        
    def find_element_by_link_text(self, link_text):
        return self.find_element(by=By.LINK_TEXT, value=link_text) #finds element within this element's children by visible link text

    def find_elements_by_link_text(self, link_text):
        return self.find_elements(by=By.LINK_TEXT, value=link_text) #finds a list of elements within this element's children by visible link text
    
    def find_element_by_partial_link_text(self, link_text):
        return self.find_element(by=By.PARTIAL_LINK_TEXT, value=link_text) #finds element within this element's children by partially visible link text
    
    def find_elements_by_partial_link_text(self, link_text):
        return self.find_elements(by=By.PARTIAL_LINK_TEXT, value=link_text) #finds a list of elements within this element's children by link text
    
    def find_element_by_tag_name(self, name):
        return self.find_element(by=By.TAG_NAME, value=name) #finds element within this element's children by tag name
    
    def find_elements_by_tag_name(self, name):
        return self.find_elements(by=By.TAG_NAME, value=name) #finds a list of elements within this element's children by tag name
    
    def find_element_by_xpath(self, xpath):
        return self.find_element(by=By.XPATH, value=xpath) #finds element by xpath
    
    def find_elements_by_xpath(self, xpath):
        return self.find_elements(by=By.XPATH, value=xpath) #finds elements within the element by xpath
    
    def find_element_by_class_name(self, name):
        return self.find_element(by=By.CLASS_NAME, value=name) #finds element within this element's children by class name
    
    def find_elements_by_class_name(self, name):
        return self.find_elements(by=By.CLASS_NAME, value=name) #finds a list of elements within this element's childrn by class name
    
    def send_keys(self, *value):
        if self.parent._is_remote:
            local_file = self.parent.file_detector.is_local_file(*value)
            if local_file is not None:
                value = self._upload(local_file)
        self._execute(Command.SEND_KEYS_TO_ELEMENT,{'text': "".join(keys_to_typing(value)),'value': keys_to_typing(value)}) #simulates typing into the element

    @property
    def location(self):
        old_loc = self._execute(Command.GET_ELEMENT_LOCATION)['value']
        new_loc = {"x": round(old_loc['x']),
                   "y": round(old_loc['y'])}
        return new_loc #locaiton of the element in the renderable canvas

    @property
    def screenshot(self, filename):
        if not filename.lower().endswith('.png'):
            warnings.warn("name used for saved screenshot does not match file "
                          "type. It should end with a `.png` extension", UserWarning)
        png = self.screenshot_as_png
        try:
            with open(filename, 'wb') as f:
                f.write(png)
        except IOError:
            return False
        finally:
            del png
        return True #saves screenshot of the current element to PNG.

    @property
    def parent(self):
        return self._parent #Internal reference to the WebDriver instance this element was found from

    @property
    def id(self):
        return self._id #Internal ID

    
    def __eq__(self):
        #?
        pass

    def __ne__(self):
        #?
        pass


    #Private Methods
    def _execute(self, command, params=None):
        if not params:
            params = {}
        params['id'] = self._id
        return self._parent.execute(command, params) #executes a command against the underlying HTML element

    def find_element(self, by=By.ID, value=None):
        return self._execute(Command.FIND_CHILD_ELEMENT, {"using": by, "value": value})['value'] #find an element given a By strategy and locator

    def find_elements(self, by=By.ID, value=None):
        return self._execute(Command.FIND_CHILD_ELEMENTS, {"using": by, "value": value})['value'] #find elements given a By strategy and locator


    def __hash__(self):
        #?
        pass


    def _upload(self):
        pass
