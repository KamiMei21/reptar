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
from .webelements import WebElement


#Why a bunch of static methods, instead of closures under this package?
#Because Python has some weirdness doing module imports that way, this just
#worked cleaner when moving the script across platforms, and extending functionality.
class Command(object):
    QUIT = 0
        
    @staticmethod
    def find_referer(context):
        document = context.window.curdoc
        
        #TODO:  Have this referer behavior upon encountering a query string 
        #       configurable as a switch: 'SEND', 'PARTIAL', or 'DROP'  --MPC
        if (not document.address.query) and (not document.address.fragment):  
            return document.address.absolute
        else:  return ''

    @staticmethod
    def get(uri, context, timeout=60, verify=False, traversal=False):       
        headers = {}
        uri = URI(uri)
        
        #Did someone really just try to pass us a #fragment?
        if (uri.fragment != "") and (uri.absolute == context.window.curdoc.address.absolute):
            pass
        else:
            if context.window.curdoc.address and traversal:
                headers["Referer"] = find_referer(context)
            if context.window.curdoc.post_data:
                headers["Content-Type"] = context.window.curdoc.post_content_type
                data = context.window.curdoc.post_data["data"]
            else:  data = None
            
            req = context.session.get(str(uri), headers=headers, verify=verify, timeout=timeout, params=data)
            #TODO:  More robust Exception value  --MPC
            if req.status_code == 404:
                context.hold.set()
                raise Exception
            else:
                context.window.spawn_doc(uri, req.content)
                if "data" in vars(context.session) or "_data" in vars(context.session):
                    data = [(k,v) for k, v in session.connection.data.items()]
                    context.window.newdoc.post_data["data"] = data
                if "files" in vars(context.session):  
                    files = context.session.files
                    context.window.newdoc.post_data["files"] = files
                
                context.window.cache.append(context.window.curdoc)
        
    @staticmethod
    def post(uri, context, timeout=60, verify=False):
        headers = context.session.headers
        headers["Referer"] = Command.find_referer(context)
        headers["Content-Type"] = context.window.curdoc.post_content_type
        data = context.window.curdoc.post_data["data"]
        files = context.window.curdoc.post_data["files"]
        req = context.session.request("POST", uri, files=files, data=data, headers=headers, timeout=timeout, verify=verify)
        
        #TODO:  More robust Exception value  --MPC
        if req.status_code == 404:  
            context.hold.set()
            raise Exception
        else:
            context.window.spawn_doc(uri, req.content)
            if "data" in vars(context.session) or "_data" in vars(context.session):
                data = [(k,v) for k, v in session.connection.data.items()]
                context.window.newdoc.post_data["data"] = data
            if "files" in vars(context.session):  
                files = context.session.files
                context.window.newdoc.post_data["files"] = files
                
            context.window.cache.append(context.window.curdoc)
        
    @staticmethod
    def find_element(key, value, context):
        element = context.window.curdoc.content.find(attrs={key: value})
        if key == "id":  selector = ('#' + value)
        else:  selector = value
        
        for idx, line in enumerate(context.window.buffer):
            #Yes, this is slow on purpose, to emulate someone looking for the element on the page
            if str(element).rstrip() in line:  context.window.cursor = (0, idx); break
            else:  continue
        
        context.window.curdoc.focus_element = WebElement(context.window.curdoc, element, selector)
        return context.window.curdoc.focus_element
