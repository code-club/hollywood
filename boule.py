# -*- coding: utf8 -*-

"""
Module général définissant et contenant les Boules.
"""

from random import random

# Masse selon le type d'objet
BOULE_MASSES = {
    'FILE': 1.,
    'CLASS': 1.,
    'DEF': 1.,
}

# Lo, k
LINKS_TYPES = {
    'PARENT_CHILD': (1., 1.),
}


class Boule(object):
    """
    Classe représentant une Boule, i.e. un objet représenté en 3D.

    Cette classe est la classe principale manipulée par le programme ; elle est
    commune à tous les autres modules.
    Le module converter se charge de créer/détruire et modifier le contenu des
    Boules.
    Le module runge_kutta déplace les Boules par simulation physique.
    Le module display_gl affiche les Boules en utilisant leur position et leur
    contenu fournis par les autres modules.
    """
    def __init__(self, text, type, parent):
        self.text = text
        self.type = type
        self.x = random() * 5
        self.y = random () * 5
        self.z = -5
        self.dx = 0
        self.dy = 0
        self.dz = 0
        self.ax = 0
        self.ay = 0
        self.az = 0
        self.m = BOULE_MASSES[type]
        self.links = [] # (autre_boule, Lo, k)
        self.parent = parent
        if self.parent:
            l0, k = LINKS_TYPES['PARENT_CHILD']
            self.links.append((parent, l0, k))
            self.parent.links.append((self, l0, k))
    def delete(self):
        for other, _, _ in self.links:
            other.remove_links(self)
    
    def remove_links(self, other):
        # TODO : remplacer self.links par un dict
        self.links = [l for l in self.links if l[0] != other]
