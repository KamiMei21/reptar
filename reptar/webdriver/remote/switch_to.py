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

from .command import Command
from reptar.webdriver.common.alert import Alert
from reptar.webdriver.common.by import By
from reptar.common.exceptions import WebDriverException

class SwitchTo:
    def __init__(self, driver):
        self._driver = driver
    
    
    @property
    def active_element(self):
        #return element with focus, or Body if nothing has focus
        return self._driver.execute(Command.GET_ACTIVE_ELEMENT)['value']


    @property
    def alert(self):
        #switches focus to an alert on the page
        alert = Alert(self._driver)
        alert.text
        return alert


    def default_content(self):
        #switch focus to the default frame
        self._driver.execute(Command.SWITCH_TO_FRAME, {'id': None})


    def frame(self, frame_reference):
        #switches focus to the specified frame, by index, name, or webelement
        if isinstance(frame_reference, basestring) and self._driver.w3c:
            try:
                frame_reference = self._driver.find_element(By.ID, frame_reference)
            except NoSuchElementException:
                try:
                    frame_reference = self._driver.find_element(By.NAME, frame_reference)
                except NoSuchElementException:
                    raise NoSuchFrameException(frame_reference)

        self._driver.execute(Command.SWITCH_TO_FRAME, {'id': frame_reference})


    def parent_frame(self):
        self._driver.execute(Command.SWITCH_TO_PARENT_FRAME)


    def window(self, window_name):
        data = {'name': window_name}
        self._driver.execute(Command.SWITCH_TO_WINDOW, data)
        