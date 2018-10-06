"""
Board for solitaire.

Created on 01.09.2018

@author: Ruslan Dolovanyuk

"""

import io
import os
os.environ['path'] += os.pathsep + os.path.join(os.getcwd(), 'gtk')

import random
import xml.etree.ElementTree as etree

import cairosvg

import pygame

import zones

from card import Card

from constants import Colors


class Board:
    """Board class for solitaire."""

    def __init__(self, config, screen, sounds):
        """Initialize board class."""
        self.config = config
        self.screen = screen
        self.sounds = sounds

        self.card_x = self.config.getint('board', 'card_x')
        self.card_y = self.config.getint('board', 'card_y')

        self.deck = []
        self.svg = etree.parse('cards.svg')
        root = self.svg.getroot()
        self.prefix = "{http://www.w3.org/2000/svg}"
        cards_iter = root.iterfind('./'+self.prefix+'g/')
        defs_iter = root.iterfind('./'+self.prefix+'defs/')
        self.svg_cards = {card.attrib['id']: card for card in cards_iter}
        self.defs = {obj.attrib['id']: obj for obj in defs_iter}
        self.textures = {name: self.svg2png(svg) for name, svg in self.svg_cards.items()}

        self.create_zones()

    def svg2png(self, svg):
        """Convert svg to png."""
        root = etree.Element('svg')
        root.set('version', '1.1')
        root.set('width', str(self.card_x))
        root.set('height', str(self.card_y))
        root.set('viewBox', '0 0 {} {}'.format(self.card_x, self.card_y))
        defs = etree.SubElement(root, 'defs')
        for obj in self.defs.values():
            defs.append(obj)
        g = etree.SubElement(root, 'g')
        g.append(svg)
        if 'joker_red' == svg.attrib['id']:
            joker_addons = [elem for elem in self.svg_cards['joker_black'].findall('./') if self.prefix+'g' == elem.tag]
            for addon in joker_addons:
                svg.append(addon)
        png = io.BytesIO(cairosvg.svg2png(bytestring=etree.tostring(root)))
        image = pygame.image.load(png)
        png.close()
        return image

    def create_deck(self):
        """Create all cards."""
        self.deck.clear()
        self.delivery = 3 if '3' == self.config.get('board', 'delivery') else 1
        deck_count = 36 if 'half' == self.config.get('board', 'deck') else 52

        for suit in ['club', 'diamond', 'heart', 'spade']:
            for rate in range(1, 14):
                if 36 == deck_count:
                    if 1 < rate < 6:
                        continue
                self.deck.append(Card(rate, suit, self.card_x, self.card_y))

        for card in self.deck:
            card.tex_face = self.textures[card.tex_name]
            card.tex_back = self.textures['back']

        random.seed()
        random.shuffle(self.deck)

    def create_zones(self):
        """Create all gaming zones."""
        screen_x = self.config.getint('screen', 'size_x')
        screen_y = self.config.getint('screen', 'size_y')
        offset_card_total = self.config.getint('board', 'offset_card_total')
        offset_card_open = self.config.getint('board', 'offset_card_open')
        offset_cols = self.config.getint('board', 'offset_cols')
        offset_card = (offset_card_total, offset_card_open)

        self.zones = []
        left = 0
        top = 0
        for index, zone in enumerate(zones.get_zones()):
            self.zones.append(zone(left, top, (self.card_x, self.card_y), offset_card, offset_cols))
            if 0 == index:
                left += 2 * offset_cols + self.card_x + 23 * offset_card_total
            elif 1 == index:
                left += 2 * offset_cols + self.card_x + 51 * offset_card_total
            elif 2 == index:
                left += 2 * offset_cols + self.card_x + 2 * offset_card_open
            elif 3 == index:
                width = 14 * offset_cols + 7 * self.card_x + 7 * 7 * offset_card_total
                left = (screen_x - width) // 2
                top = 2 * offset_cols + self.card_y +51 * offset_card_total

    def clear_zones(self):
        """Clear all zones card stack."""
        for zone in self.zones:
            zone.clear()

    def draw(self):
        """Draw method for board."""
        for zone in self.zones:
            zone.draw(self.screen)

    def distribution(self):
        """Distribution cards in new game."""
        while self.deck:
            self.zones[1].cards.append(self.deck.pop())
            self.sounds.play('deal')

        for start_row in range(len(self.zones[4].rows)):
            for row in range(start_row, len(self.zones[4].rows)):
                self.zones[4].rows[row].append(self.zones[1].cards.pop())
                self.sounds.play('distrib')

        for row in range(len(self.zones[4].rows)):
            self.zones[4].rows[row][-1].status = True
            self.sounds.play('open')
