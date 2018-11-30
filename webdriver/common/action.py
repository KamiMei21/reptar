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

import time
from reptar.webdriver.command import Command
from .utils import keys_to_typing

import ActionBuilder
import Interaction
import KeyAcions
import KeyInput



'''*********************************************
    ***INTERACTION***    
*********************************************'''
KEY = "key"
NONE = "none"
SOURCE_TYPES = set([KEY, NONE])

class Interaction(object):
    PAUSE = "pause"
    def __init__(self, source):
        self.source = source


class Pause(Interaction):
    def __init__(self, source, duration=0):
        super(Interaction, self).__init__()
        self.source = source
        self.duration = duration

    def encode(self):
        return {"type": self.PAUSE,
                "duration": int(self.duration * 1000)}



'''*********************************************
    ***KEY_ACTIONS***    
*********************************************'''
class KeyActions(Interaction):
    def __init__(self, source=None):
        if source is None:
            source = KeyInput(KEY)
        self.source = source
        super(KeyActions, self).__init__(source)

    def key_down(self, letter):
        return self._key_action("create_key_down", letter)

    def key_up(self, letter):
        return self._key_action("create_key_up", letter)

    def pause(self, duration=0):
        return self._key_action("create_pause", duration)

    def send_keys(self, text):
        if not isinstance(text, list):
            text = keys_to_typing(text)
        for letter in text:
            self.key_down(letter)
            self.key_up(letter)
        return self

    def _key_action(self, action, letter):
        meth = getattr(self.source, action)
        meth(letter)
        return self



'''*********************************************
    ***KEY_INPUT***    
*********************************************'''
class KeyInput(InputDevice):
    def __init__(self, name):
        super(KeyInput, self).__init__()
        self.name = name
        self.type = interaction.KEY

    def encode(self):
        return {"type": self.type, "id": self.name, "actions": [acts.encode() for acts in self.actions]}

    def create_key_down(self, key):
        self.add_action(TypingInteraction(self, "keyDown", key))

    def create_key_up(self, key):
        self.add_action(TypingInteraction(self, "keyUp", key))

    def create_pause(self, pause_duration=0):
        self.add_action(Pause(self, pause_duration))


class TypingInteraction(Interaction):
    def __init__(self, source, type_, key):
        super(TypingInteraction, self).__init__(source)
        self.type = type_
        self.key = key

    def encode(self):
        return {"type": self.type, "value": self.key}



'''*********************************************
    ***ACTIONBUILDER***    
*********************************************'''
class ActionBuilder(object):
    def __init__(self, driver, keyboard=None):
        if keyboard is None:
            keyboard = KeyInput(interaction.KEY)
        self.devices = [keyboard]
        self._key_action = KeyActions(keyboard)
        self.driver = driver

    @property
    def key_inputs(self):
        return [device for device in self.devices if device.type == interaction.KEY]

    @property
    def key_action(self):
        return self._key_action

    def add_key_input(self, name):
        new_input = KeyInput(name)
        self._add_input(new_input)
        return new_input

    def clear_actions(self):
        pass

    def _add_input(self, input):
        self.devices.append(input)



'''*********************************************
    ***ACTIONCHAINS***    
*********************************************'''
class ActionChains(object):
    def __init__(self,driver):
        #create new action chain
        self._driver = driver
        self._actions = []
    
    def perform(self):
        #performs all stored actions
        for action in self._actions:
            action()

    def reset_action(self):
        #resets the chain
        self._actions = []
   
    def key_down(self, value, element=None):
        #sends a key press only, without releasing it (probs should use for Ctrl, or Alt, or Shift)
        self._actions.append(lambda: self._driver.execute(Command.SEND_KEYS_TO_ACTIVE_ELEMENT,{"value": keys_to_typing(value)}))
        return self
        
    def key_up(self, value, element=None):
        #releases a modifier key
        self._actions.append(lambda: self._driver.execute(Command.SEND_KEYS_TO_ACTIVE_ELEMENT, {"value": keys_to_typing(value)}))
        return self

    def pause(self, seconds):
        self._actions.append(lambda: time.sleep(seconds))
        return self

    def send_keys(self, *keys_to_send):
        typing = keys_to_typing(keys_to_send)
        self._actions.append(lambda: self._driver.execute(Command.SEND_KEYS_TO_ACTIVE_ELEMENT, {'value': typing}))

    def __enter__(self):
        return self 

    def __exit__(self, _type, _value, _traceback):
        pass 