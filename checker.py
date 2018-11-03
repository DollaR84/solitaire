"""
Module contain functions with check rules.

Created on 21.10.2018

@author: Ruslan Dolovanyuk

"""

from constants import Cards


def change_suit(card1, card2):
    """Check change suit two cards."""
    if card1.suit in Cards.black_suits:
        return True if card2.suit in Cards.red_suits else False
    else:
        return True if card2.suit in Cards.black_suits else False


def change_suits(cards):
    """Check change suits cards."""
    for index, card in enumerate(cards):
        if (len(cards) - 1) > index:
            if not change_suit(card, cards[index + 1]):
                return False
    return True


def rate_down(cards):
    """Check down rate index cards."""
    for index, card in enumerate(cards):
        if (len(cards) - 1) > index:
            if cards[index + 1].rate_index != card.rate_index - 1:
                return False
    return True
