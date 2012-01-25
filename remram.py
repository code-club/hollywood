# -*- coding: utf8 -*-

"""
Module qui envoie du LOL.
"""

def rofl(file):
    """
    rofl(file)

    Affiche un roflcopter sur le fichier spécifié.
    """
    file.write("""\
 ROFL:ROFL:ROFL:ROFL
         _^___
 L    __/   []\\
LOL===_        \\
 L     \________]
         I   I
        -------/
""")

if __name__ == "__main__":
    from sys import stdout

    rofl(stdout)
