"""
Card module for solitaires.

Created on 27.08.2018

@author: Ruslan Dolovanyuk

"""

import pygame


class Card:
    """Card class for solitaires."""
    rate = property(lambda self: self.__RATE_NAME)
    suit = property(lambda self: self.__SUIT)

    def __init__(self, rate, suit, width, height):
        """Initialize card class."""
        self.__RATE = rate
        self.__SUIT = suit
        self.__WIDTH = width
        self.__HEIGHT = height
        self.status = False

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

        self.tex_face = None
        self.tex_back = None

        self.surface = pygame.Surface((self.__WIDTH, self.__HEIGHT))

    def draw(self, zone, offset):
        """Draw card on surface."""
        if self.status:
            self.surface.blit(self.tex_face, (0, 0))
        else:
            self.surface.blit(self.tex_back, (0, 0))
        zone.blit(self.surface, offset)
