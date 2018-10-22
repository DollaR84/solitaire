"""
The speak module.

Created on 22.11.2018

@author: Ruslan Dolovanyuk

"""

import Tolk

import win32com.client


class Speech:
    """The speak class for speak voice."""

    def __init__(self, config):
        """Initialize speech class."""
        self.config = config

        self.speaker = win32com.client.Dispatch("Sapi.SpVoice")
        self.voices = self.speaker.GetVoices()
        self.voices_ids = [voice.Id for voice in self.voices]
        self.voices_names = [voice.GetDescription() for voice in self.voices]

        self.sapi = self.config.getboolean('speech', 'sapi')
        self.set_voice(self.config.getint('speech', 'voice'))
        self.speaker.Rate = self.config.getint('speech', 'rate')
        self.speaker.Volume = self.config.getint('speech', 'volume')

        self.error = False
        Tolk.load()
        self.name = Tolk.detect_screen_reader()
        if not self.name:
            self.error = True
            print('Not find supported screen reader')
        if not Tolk.has_speech():
            self.error = True
            print('Screen reader nottsupport speak text')

        self.set_speak_out()

    def finish(self):
        """Unload Tolk."""
        Tolk.unload()

    def set_voice(self, index):
        """Set voice for speak."""
        try:
            self.speaker.Voice = self.voices[index]
        except:
            print('error: do not set voice')

    def set_speak_out(self):
        """Set speak out: tolk or sapi."""
        if self.sapi and self.error:
            self.speak = self.speak_sapi
        else:
            self.speak = self.speak_tolk

    def speak_tolk(self, phrase):
        """Speak phrase with tolk."""
        Tolk.output(phrase)

    def speak_sapi(self, phrase):
        """Speak phrase in sapi voice."""
        self.speaker.Speak(phrase)
