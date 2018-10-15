"""
Functions for multiprocessing.

Created on 12.10.2018

@author: Ruslan Dolovanyuk

"""

import io
import math
import multiprocessing
import multiprocessing.pool
import os
import sys
if getattr(sys, 'frozen', False):
    os.environ['path'] += os.pathsep + os.path.join(os.path.dirname(sys.executable), 'gtk')
else:
    os.environ['path'] += os.pathsep + os.path.join(os.getcwd(), 'gtk')

import xml.etree.ElementTree as etree

from itertools import repeat

import cairosvg

import pygame


def __thread_svg2png(svg_string, svg_start_pos, svg_card_size, defs_string):
        """Convert svg to png."""
        root = etree.Element('svg')
        root.set('version', '1.1')
        root.set('width', str(int(math.ceil(svg_card_size[0]))))
        root.set('height', str(int(math.ceil(svg_card_size[1]))))
        defs = etree.SubElement(root, 'defs')
        for obj in defs_string:
            defs.append(etree.fromstring(obj))
        g = etree.SubElement(root, 'g')
        svg = etree.fromstring(svg_string)
        offset_x, offset_y = 0, 0
        for elem in svg.findall('./'):
            if ('{http://www.w3.org/2000/svg}use' == elem.tag) and ('#base' == elem.attrib['{http://www.w3.org/1999/xlink}href']):
                offset_x = float(elem.attrib['x'])
                offset_y = float(elem.attrib['y'])
                break
        root.set('viewBox', '{} {} {} {}'.format(svg_start_pos[0]+offset_x, svg_start_pos[1]+offset_y, svg_card_size[0], svg_card_size[1]))
        g.append(svg)
        png = cairosvg.svg2png(bytestring=etree.tostring(root))
        return (svg.attrib['id'], png)


def __thread_png2tex(data, card_x, card_y):
    """Convert png file object in pygame surface with need sizes."""
    png = io.BytesIO(data[1])
    image = pygame.image.load(png)
    png.close()
    return (data[0], pygame.transform.scale(image, (card_x, card_y)))


def __thread_sound(data, volume):
    """Create pygame Sound object."""
    wav = pygame.mixer.Sound(data[1])
    wav.set_volume(volume)
    return (data[0], wav)


def svg2png(svg_cards, svg_start_pos, svg_card_size, defs_dict):
    """Run processes for convert svg to png."""
    svg_cards_string = [etree.tostring(card) for card in svg_cards.values()]
    defs_string = [etree.tostring(obj) for obj in defs_dict.values()]
    with multiprocessing.Pool() as pool:
        return pool.starmap(__thread_svg2png, zip(svg_cards_string, repeat(svg_start_pos), repeat(svg_card_size), repeat(defs_string)))


def png2tex(data, card_x, card_y):
    """Run threads for convert png to pygame surface."""
    with multiprocessing.pool.ThreadPool() as pool:
        results = pool.starmap(__thread_png2tex, zip(data, repeat(card_x), repeat(card_y)))
        return {name: tex for name, tex in results}


def sounds(data, volume):
    """Thread for load wav sound in pygame."""
    with multiprocessing.pool.ThreadPool() as pool:
        results = pool.starmap(__thread_sound, zip(data, repeat(volume)))
        return {name: wav for name, wav in results}
