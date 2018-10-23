"""
Card module for solitaires.

Created on 27.08.2018

@author: Ruslan Dolovanyuk

"""

import pygame

from constants import Colors


class Card:
    """Card class for solitaires."""
    rate_index = property(lambda self: self.__RATE)
    rate = property(lambda self: self.__RATE_NAME)
    suit = property(lambda self: self.__SUIT)

    def __init__(self, rate, suit, width, height, deck_count):
        """Initialize card class."""
        self.__RATE = rate
        self.__SUIT = suit
        self.__WIDTH = width
        self.__HEIGHT = height
        self.color = Colors.YELLOW
        self.__status = False
        self.__take = False

        if 11 == self.__RATE:
            self.__RATE_NAME = 'jack'
            self.tex_name = '_'.join(['jack', self.__SUIT])
        elif 12 == self.__RATE:
            self.__RATE_NAME = 'queen'
            self.tex_name = '_'.join(['queen', self.__SUIT])
        elif 13 == self.__RATE:
            self.__RATE_NAME = 'king'
            self.tex_name = '_'.join(['king', self.__SUIT])
        else:
            self.__RATE_NAME = 'ace' if 1 == self.__RATE else str(self.__RATE)
            self.tex_name = '_'.join([self.__SUIT, str(self.__RATE)])

        if 36 == deck_count:
            if 1 == self.__RATE:
                self.__RATE = 5

        self.tex_face = None
        self.tex_back = None

        self.surface = pygame.Surface((self.__WIDTH, self.__HEIGHT))

    @property
    def status(self):
        """Return status card."""
        return self.__status

    @status.setter
    def status(self, value):
        """Setter for status card."""
        self.__status = value
        if self.status:
            self.surface.blit(self.tex_face, (0, 0))
        else:
            self.surface.blit(self.tex_back, (0, 0))

    @property
    def take(self):
        """Return take status card."""
        return self.__take

    @take.setter
    def take(self, value):
        """Setter for take status card."""
        self.__take = value
        if self.take:
            pygame.draw.rect(self.surface, self.color, (0, 0, self.__WIDTH, self.__HEIGHT), 1)
        else:
            self.status = self.__status

    def draw(self, zone, offset):
        """Draw card on surface."""
        zone.blit(self.surface, offset)
