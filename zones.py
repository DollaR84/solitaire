"""
Zones module for solitaires.

Created on 08.09.2018

@author: Ruslan Dolovanyuk

"""

import pygame

from constants import Colors


class ZoneBase:
    """Base zone class for solitaires."""

    def __init__(self, left, top, card_size, offset, offset_cols):
        """Initialize base class."""
        self.LEFT = left
        self.TOP = top
        self.card_size = card_size
        self.OFFSET = offset
        self.OFFSET_COLS = offset_cols
        self.color = Colors.YELLOW
        self.offset_zone = (self.LEFT, self.TOP)


class ZoneRecall(ZoneBase):
    """Recall zone class for solitaires."""

    def __init__(self, left, top, card_size, offset, offset_cols):
        """Initialize recall class."""
        super().__init__(left, top, card_size, offset[0], offset_cols)
        self.WIDTH = 2 * offset_cols + card_size[0] + 23 * offset[0]
        self.HEIGHT = 2 * offset_cols + card_size[1] + 51 * offset[0]
        self.zone = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.cards = []

    def draw(self, screen):
        """Draw zone on board."""
        left, top = self.get_coord_zero(0)
        pygame.draw.rect(self.zone, self.color, (left, top, self.card_size[0], self.card_size[1]), 1)
        for index, card in enumerate(self.cards):
            offset = self.get_coord_card(0, index)
            card.draw(self.zone, offset)
        screen.blit(self.zone, self.offset_zone)

    def get_coord_zero(self, index):
        """Return coord x and y empty row."""
        return (self.OFFSET_COLS, self.HEIGHT-self.OFFSET_COLS-self.card_size[1])

    def get_coord_card(self, row_index, index):
        """Return coord x and y card in row stack."""
        return (self.OFFSET_COLS+index*self.OFFSET, self.HEIGHT-self.OFFSET_COLS-self.card_size[1]-index*self.OFFSET)

    def clear(self):
        """Clear cards stack."""
        self.cards.clear()

    def if_empty(self, index):
        """Check stack cards of empty."""
        return True if self.cards else False


class ZoneDeck(ZoneBase):
    """Deck zone class for solitaires."""

    def __init__(self, left, top, card_size, offset, offset_cols):
        """Initialize deck class."""
        super().__init__(left, top, card_size, offset[0], offset_cols)
        self.WIDTH = 2 * offset_cols + card_size[0] + 51 * offset[0]
        self.HEIGHT = 2 * offset_cols + card_size[1] + 51 * offset[0]
        self.zone = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.cards = []

    def draw(self, screen):
        """Draw zone on board."""
        left, top = self.get_coord_zero(0)
        pygame.draw.rect(self.zone, self.color, (left, top, self.card_size[0], self.card_size[1]), 1)
        for index, card in enumerate(self.cards):
            offset = self.get_coord_card(0, index)
            card.draw(self.zone, offset)
        screen.blit(self.zone, self.offset_zone)

    def get_coord_zero(self, index):
        """Return coord x and y empty row."""
        return (self.OFFSET_COLS, self.HEIGHT-self.OFFSET_COLS-self.card_size[1])

    def get_coord_card(self, row_index, index):
        """Return coord x and y card in row stack."""
        return (self.OFFSET_COLS+index*self.OFFSET, self.HEIGHT-self.OFFSET_COLS-self.card_size[1]-index*self.OFFSET)

    def clear(self):
        """Clear cards stack."""
        self.cards.clear()

    def if_empty(self, index):
        """Check stack cards of empty."""
        return True if self.cards else False


class ZoneIncoming(ZoneBase):
    """Incoming zone class for solitaires."""

    def __init__(self, left, top, card_size, offset, offset_cols):
        """Initialize incoming class."""
        super().__init__(left, top, card_size, offset[0], offset_cols)
        self.OFFSET_OPEN = offset[1]
        self.WIDTH = 2 * offset_cols + card_size[0] + 2 * offset[1]
        self.HEIGHT = 2 * offset_cols + card_size[1] + 51 * offset[0]
        self.zone = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.cards = []

    def draw(self, screen):
        """Draw zone on board."""
        for index, card in enumerate(self.cards):
            offset = self.get_coord_card(0, index)
            card.draw(self.zone, offset)
        screen.blit(self.zone, self.offset_zone)

    def get_coord_zero(self, index):
        """Return coord x and y empty row."""
        return (self.OFFSET_COLS, self.HEIGHT-self.OFFSET_COLS-self.card_size[1])

    def get_coord_card(self, row_index, index):
        """Return coord x and y card in row stack."""
        return (self.OFFSET_COLS+index*self.OFFSET_OPEN, self.HEIGHT-self.OFFSET_COLS-self.card_size[1])

    def clear(self):
        """Clear cards stack."""
        self.cards.clear()

    def if_empty(self, index):
        """Check stack cards of empty."""
        return True if self.cards else False


class ZoneHouse(ZoneBase):
    """House zone class for solitaires."""

    def __init__(self, left, top, card_size, offset, offset_cols):
        """Initialize house class."""
        super().__init__(left, top, card_size, offset[0], offset_cols)
        self.WIDTH = 5 * offset_cols + 4 * card_size[0] + 12 * offset[0]
        self.HEIGHT = 2 * offset_cols + card_size[1] + 51 * offset[0]
        self.zone = pygame.Surface((self.WIDTH, self.HEIGHT))

        self.rows = []
        for _ in range(4):
            self.rows.append([])

    def draw(self, screen):
        """Draw zone on board."""
        for row_index, row in enumerate(self.rows):
            left, top = self.get_coord_zero(row_index)
            pygame.draw.rect(self.zone, self.color, (left, top, self.card_size[0], self.card_size[1]), 1)
            for index, card in enumerate(row):
                offset = self.get_coord_card(row_index, index)
                card.draw(self.zone, offset)
        screen.blit(self.zone, self.offset_zone)

    def get_coord_zero(self, index):
        """Return coord x and y empty row."""
        return (self.OFFSET_COLS+index*(self.card_size[0]+self.OFFSET_COLS), self.HEIGHT-self.OFFSET_COLS-self.card_size[1])

    def get_coord_card(self, row_index, index):
        """Return coord x and y card in row stack."""
        return (self.OFFSET_COLS+row_index*(self.card_size[0]+self.OFFSET_COLS)+index*self.OFFSET, self.HEIGHT-self.OFFSET_COLS-self.card_size[1]-index*self.OFFSET)

    def clear(self):
        """Clear cards stack."""
        for row in self.rows:
            row.clear()

    def if_empty(self, index):
        """Check stack cards of empty."""
        return True if self.rows[index] else False


class ZoneColumns(ZoneBase):
    """Columns zone class for solitaires."""

    def __init__(self, left, top, card_size, offset, offset_cols):
        """Initialize columns class."""
        super().__init__(left, top, card_size, offset[0], offset_cols)
        self.OFFSET_OPEN = offset[1]
        self.WIDTH = 14 * offset_cols + 7 * card_size[0] + 7 * 7 * offset[0]
        self.HEIGHT = 2 * offset_cols + card_size[1] + 7 * offset[0] + 12 * offset[1]
        self.zone = pygame.Surface((self.WIDTH, self.HEIGHT))

        self.rows = []
        for _ in range(7):
            self.rows.append([])

    def draw(self, screen):
        """Draw zone on board."""
        for row_index, row in enumerate(self.rows):
            left, top = self.get_coord_zero(row_index)
            pygame.draw.rect(self.zone, self.color, (left, top, self.card_size[0], self.card_size[1]), 1)
            for index, card in enumerate(row):
                offset = self.get_coord_card(row_index, index)
                card.draw(self.zone, offset)
        screen.blit(self.zone, self.offset_zone)

    def get_coord_zero(self, index):
        """Return coord x and y empty row."""
        return (self.OFFSET_COLS+index*(self.card_size[0]+self.OFFSET_COLS), self.OFFSET_COLS)

    def get_coord_card(self, row_index, index):
        """Return coord x and y card in row stack."""
        index_first_open = self.rows[row_index].index(next(card for card in self.rows[row_index] if card.status))
        offset_close_cards = index_first_open * self.OFFSET
        if self.rows[row_index][index].status:
            offset = (self.OFFSET_COLS+row_index*(self.card_size[0]+self.OFFSET_COLS), self.OFFSET_COLS+offset_close_cards+(index-index_first_open)*self.OFFSET_OPEN)
        else:
            offset = (self.OFFSET_COLS+row_index*(self.card_size[0]+self.OFFSET_COLS), self.OFFSET_COLS+index*self.OFFSET)
        return offset

    def clear(self):
        """Clear cards stack."""
        for row in self.rows:
            row.clear()

    def if_empty(self, index):
        """Check stack cards of empty."""
        return True if self.rows[index] else False


def get_zones():
    """Return all zones classes."""
    return (ZoneRecall, ZoneDeck, ZoneIncoming, ZoneHouse, ZoneColumns)
