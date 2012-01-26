# -*- coding: utf8 -*-

"""
Module main, point d'entrée du logiciel.

Initialise tout le bordel et contient la glue liant les différents modules entre
eux.
"""

import sys
import runge_kutta
from converter import BouleStore


boule_store = None


def update(delta):
    """
    update(delta)

    Met à jour la représentation des objets :
    1) Via le module converter (création/suppression d'objets, changement de
    leur représentation)
    2) Via le module runge_kutta (mise à jour de la position uniquement, par
    simulation physique)
    """
    # Gestion des sources : mise à jour des boules depuis les fichiers
    # Utilisation de inotify(2) ?

    # Gestion physique : mise à jour des positions des boules par simulation
    # physique
    global boule_store
    boule_store.update()
    runge_kutta.move(boule_store.get_boules(), delta)


def main():
    # ROFLCOPTER
    from remram import rofl
    from sys import stdout
    rofl(stdout)

    # Lecture des sources, génération des Boules
    if len(sys.argv) > 1:
        files = sys.argv[1:]
    else:
        files = [__file__]
    global boule_store
    boule_store = BouleStore(files)

    # Lancement de GLUT, initialisation graphique
    from display_gl import run
    run(boule_store)
