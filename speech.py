"""
The speak module.

Created on 22.11.2018

@author: Ruslan Dolovanyuk

"""

import Tolk


class Speech:
    """The speak class for speak voice."""

    def __init__(self, config):
        """Initialize speech class."""
        self.config = config
        Tolk.load()
        self.name = Tolk.detect_screen_reader()
        if not self.name:
            print('Not find supported screen reader')
        if not Tolk.has_speech():
            print('Screen reader nottsupport speak text')

    def finish(self):
        """Unload Tolk."""
        Tolk.unload()

    def speak(self, phrase):
        """Speak phrase."""
        Tolk.output(phrase)
