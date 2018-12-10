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
import os

from time import sleep
from io import StringIO
from bs4 import BeautifulSoup

from reptar.common.exceptions import WebDriverException
from .remote.remote_connection import URI


#Lovingly borrowed from Lynx - please wrap, don't modify
class Document(object):
    def __init__(self, parent, parser="html5lib", content=None, address=None):
        self.parent = parent
        self.parser = parser
        self.post_content_type = ''
        self.post_data = {"data": [], "files": []}
        self.focus_element = None
        
        if (not address) or (isinstance(address, URI)):  self.address = address
        else:  self.address = URI(address)
        
        if content:  self.content = BeautifulSoup(content, parser)
        else:  self.content = content
        
    #Method to send a request up the chain to parent
    def bubble_option(self, func, params):
        try:
            getattr(self, func)(**params)
        except:
            self.parent.bubble_option(func, params)
        
    #Do all the house-keeping required to present a proper data object to the server
    def pack_form(self):
        self.focus_element = self.focus_element.recover_context()
        self.focus_element = self.focus_element.find_parent("form")
        method = self.focus_element.get("method", "GET")
        selector = ','.join("{}[name]".format(i) for i in ("input", "button", "textarea", "select"))
        for tag in self.focus_element.select(selector):
            name = tag.get("name")
        
            if tag.name == "input":
                if tag.get("type") in ("radio","checkbox"):
                    if "checked" not in tag.attrs:  continue
                    value = tag.get("value", "on")
                else:
                    value = tag.get("value", "")
            
                if tag.get("type") == "file":
                    if not value:  continue
                    if isinstance(value, str):  value = open(value, "rb")
                    self.post_data["files"][name] = value
                else:
                    self.post_data["data"].append((name, value))
            
            if tag.name == "button":
                if tag.get("type", "") in ("button", "reset"):  continue
                else:  self.post_data["data"].append((name, tag.get("value", "")))
        
            if tag.name == "textarea":
                self.post_data["data"].append((name, tag.text))
        
            if tag.name == "select":
                options = tag.select("option")
                selected_values = [i.get("value", i.text) for i in options if "selected" in i.attrs]
            
                if "multiple" in tag.attrs:
                    for value in selected_values:
                        self.post_data["data"].append((name, value))
                elif selected_values:
                    self.post_data["data"].append((name, selected_values[-1]))
                elif options:
                    self.post_data["data"].append((name, options[0].get("value", options[0].text)))
                    
        if (not self.post_data["files"]) and method.lower() != "put":
            self.post_content_type = "application/x-www-form-urlencoded"
        else:
            self.post_content_type = "multipart/form-data"
      
#Lovingly borrowed from Lynx - please wrap, don't modify
class Window(object):
    def __init__(self, parent):
        self.parent = parent
        self.curdoc = Document(self)
        self.newdoc = None
        self.cache = []
        self.cursor = (0,0)
        self.buffer = None
        
    #Method to send a request up the chain to parent
    def bubble_option(self, func, params):
        try:
            getattr(self, func)(**params)
        except:
            self.parent.bubble_option(func, params)
        
    def spawn_doc(self, address, content, parser="html5lib"):
        if self.newdoc:  self.cache.append(self.newdoc)
        self.newdoc = Document(parent=self, parser=parser, content=content, address=address)
        
    def is_different(self):
        if (not isinstance(self.curdoc, Document)) or (not isinstance(self.newdoc, Document)):
            return True
        if (self.curdoc.address != self.newdoc.address):
            return True
        if (self.curdoc.post_data != self.newdoc.post_data):
            return True
        
        return False
        
    def swap_doc(self):
        self.curdoc = self.newdoc
        self.buffer = StringIO(str(self.curdoc.content)).readlines()
        self.newdoc = None

#Wrapper class for BeautifulSoup tag elements
class WebElement(object):
    def __init__(self, parent, element, selector):
        self.parent = parent
        self.element = element
        self.selector = selector
        
    def recover_context(self):
        return self.parent.content.select(self.selector)[0]
        
    def send_keys(self, keys):
        #TODO:  Currently only expects an "input" type form element
        element = self.recover_context()
        element["value"] = keys
        sleep((0.17 * len(keys)))
        self.element = element
        
    def submit(self):
        self.parent.pack_form()
        method = self.parent.focus_element.get("method")
        action = self.parent.focus_element.get("action")
        url = self.parent.address.urljoin(action)
        
        if method is "GET":  self.parent.bubble_option("get", {"uri": url})
        else:  self.parent.bubble_option("post", {"uri": url})
        
    def __repr__(self):
        return str(self.element)
