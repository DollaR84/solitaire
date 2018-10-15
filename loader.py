"""
Functions for loading resources.

Created on 15.10.2018

@author: Ruslan Dolovanyuk

"""

import pickle

import processes


def textures(svg_cards, svg_start_pos, svg_card_size, defs_dict, card_x, card_y):
    """Load textures from svg or cache."""
    try:
        cache_file = open('cache.dat', 'rb')
    except IOError as e:
        pass
    else:
        with cache_file:
            cache = pickle.load(cache_file)
            if (cache['card_x'] == card_x) and (cache['card_y'] == card_y):
                cache.pop('card_x')
                cache.pop('card_y')
                data = [(name, png) for name, png in cache.items()]
                return processes.png2tex(data, card_x, card_y)
    data = processes.svg2png(svg_cards, svg_start_pos, svg_card_size, defs_dict)
    __cacher(data, card_x, card_y)
    return processes.png2tex(data, card_x, card_y)


def __cacher(data, card_x, card_y):
    """Write data in cache."""
    with open('cache.dat', 'wb') as save_file:
        cache = {name: png for name, png in data}
        cache['card_x'] = card_x
        cache['card_y'] = card_y
        pickle.dump(cache, save_file)


def sounds(volume):
    """Load sounds wav data from binary file."""
    with open('sounds.dat', 'rb') as file_data:
        wavs = pickle.load(file_data)
        data = [(name, wav) for name, wav in wavs.items()]
        return processes.sounds(data, volume)


def music():
    """Load music from binary file."""
    with open('music.dat', 'rb') as file_data:
        return pickle.load(file_data)
