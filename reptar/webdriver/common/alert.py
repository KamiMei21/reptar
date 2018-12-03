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

from reptar.webdriver.common.utils import keys_to_typing
from reptar.webdriver.command import Command


class Alert(object):
    def __init__(self, driver):
        self.driver = driver 

    @property
    def text(self):
        #gets text of alert
        return self.driver.execute(Command.GET_ALERT_TEXT)["value"]

    def dismiss(self):
        #dismissed alert available
        self.driver.execute(Command.DISMISS_ALERT)

    def accept(self):
        #accepts alert
        self.driver.execute(Command.ACCEPT_ALERT)

    def send_keys(self, keysToSend):
        #send keys to the alert. 
        self.driver.execute(Command.SET_ALERT_VALUE, {'text': keysToSend})