# -*- coding: utf8 -*-

"""
Module d'affichage via OpenGL et GLUT.

S'occupe du windowing et de tout l'affichage graphique.
"""

from OpenGL import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import time

import main

_boule_store = None

def drawScene():
    """
    drawScene()

    Affiche toute la scène, via OpenGL.
    """
    global _boule_store
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glTranslatef(0.0, 0.0, -10.0)

    boules = _boule_store.get_boules()
    print("drawScene() ; %d boules" % len(boules))

    # TODO : drawScene()
    gluSphere(_quadric, 1.3, 32, 32)

    glutSwapBuffers()

def resizeWindow(width, height):
    """
    resizeWindow(width, height)

    Fonction appelée lorsque la fenêtre change de taille pour mettre à jour le
    viewport et la projection en perspective.
    """
    if height == 0:
        height = 1

    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width)/float(height), 1, 1000.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def keyPressed(*args):
    """
    keyPressed(*args)

    Fonction gérant les appuis clavier.
    STUB
    """
    pass

def initGL():
    """
    initGL()

    Initialise OpenGL en début de programme.
    """
    glShadeModel(GL_SMOOTH)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

    global _quadric
    _quadric = gluNewQuadric()
    gluQuadricNormals(_quadric, GLU_SMOOTH)
    gluQuadricTexture(_quadric, GL_TRUE)

_last_frame = time.clock()

def updateScene():
    """
    updateScene()

    Fonction de mise à jour appelée périodiquement par GLUT.
    Wrapper se contentant d'appeler main.update()
    """
    global _last_frame
    now = time.clock()
    delta = now - _last_frame
    _last_frame = now
    main.update(delta)

def run(boule_store):
    """
    run()

    Point d'entrée du module d'affichage ; lance la boucle principale du
    programme.

    Cette boucle se charge ensuite de dessiner les objets et d'appeler
    périodiquement main.update() pour les mettre à jour.
    """
    global _window
    global _boule_store

    _boule_store = boule_store

    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(10, 10)

    _window = glutCreateWindow('Visualisation')

    glutDisplayFunc(drawScene)

    glutIdleFunc(updateScene)

    glutReshapeFunc(resizeWindow)

    glutKeyboardFunc(keyPressed)

    initGL()

    glutMainLoop()
