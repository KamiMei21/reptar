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

class ProxyTypeFactor:
    def make():
        pass


class ProxyType:
    def load():
        pass

class Proxy(object):
    def __init__(self):
        #create new proxy
        pass

    @property
    def proxy_type(self):
        return self.proxyType


    @proxy_type.setter
    def proxy_type(self, value):
        self._verify_proxy_type_compatibility(value)
        self.proxyType = value
    
    
    @property
    def auto_detect(self):
        return self.autodetect
    
    
    @auto_detect.setter
    def auto_detect(self, value):
        if isinstance(value, bool):
            if self.autodetect is not value:
                self._verify_proxy_type_compatibility(ProxyType.AUTODETECT)
                self.proxyType = ProxyType.AUTODETECT
                self.autodetect = value
        else:
            raise ValueError("Autodetect proxy value needs to be a boolean")
    
    
    @property
    def ftp_proxy(self):
        return self.ftpProxy
    
    
    @ftp_proxy.setter
    def ftp_proxy(self, value):
        self._verify_proxy_type_compatibility(ProxyType.MANUAL)
        self.proxyType = ProxyType.MANUAL
        self.ftpProxy = value

    
    
    @property
    def http_proxy(self):
        return self.httpProxy
    
    
    @http_proxy.setter
    def http_proxy(self, value):
        self._verify_proxy_type_compatibility(ProxyType.MANUAL)
        self.proxyType = ProxyType.MANUAL
        self.httpProxy = value

    
    
    @property
    def no_proxy(self):
        return self.noProxy
    
    
    @no_proxy.setter
    def no_proxy(self, value):
        self._verify_proxy_type_compatibility(ProxyType.MANUAL)
        self.proxyType = ProxyType.MANUAL
        self.noProxy = value

    
    
    @property
    def proxy_autoconfig_url(self):
        return self.proxyAutoconfigUrl
    
    
    @proxy_autoconfig_url.setter
    def proxy_autoconfig_url(self, value):
        self._verify_proxy_type_compatibility(ProxyType.PAC)
        self.proxyType = ProxyType.PAC
        self.proxyAutoconfigUrl = value
    
    @property
    def ssl_proxy(self):
        return self.sslProxy
    
    
    @ssl_proxy.setter
    def ssl_proxy(self, value):
        self._verify_proxy_type_compatibility(ProxyType.MANUAL)
        self.proxyType = ProxyType.MANUAL
        self.sslProxy = value

    
    @property
    def socks_proxy(self):
        return self.socksProxy
    
    
    @socks_proxy.setter
    def socks_proxy(self, value):
        self._verify_proxy_type_compatibility(ProxyType.MANUAL)
        self.proxyType = ProxyType.MANUAL
        self.socksProxy = value

    
    @property
    def socks_username(self):
        return self.socksUsername
    
    
    @socks_username.setter
    def socks_username(self, value):
        self._verify_proxy_type_compatibility(ProxyType.MANUAL)
        self.proxyType = ProxyType.MANUAL
        self.socksUsername = value

    
    
    @property
    def socks_password(self):
        return self.socksPassword
    
    
    @socks_password.setter
    def socks_password(self, value):
        self._verify_proxy_type_compatibility(ProxyType.MANUAL)
        self.proxyType = ProxyType.MANUAL
        self.socksPassword = value
    
    def _verify_proxy_type_compatibility(self, compatibleProxy):
        if self.proxyType != ProxyType.UNSPECIFIED and self.proxyType != compatibleProxy:
            raise Exception(" Specified proxy type (%s) not compatible with current setting (%s)" % (compatibleProxy, self.proxyType))
    
