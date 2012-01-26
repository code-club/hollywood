# -*- coding: utf8 -*-

import itertools
import time
import parse
from boule import Boule


class BouleStore(object):
    def __init__(self, files):
        self.lines = {}
        self.files = files
        self.last_update = 0
        self.boules = None

    def update(self):
        if time.time() - self.last_update > 5:
            self._feed_lines(itertools.chain.from_iterable(parse.parse(f)
                for f in self.files))
            self.last_update = time.time()
            self.boules = list(self.lines.values())

    def _feed_lines(self, new_lines):
        left = self.lines.keys()
        links_to_update = []
        for line, parent in new_lines:
            try:
                left.remove(line)
            except ValueError:
                pass  # Déjà là, on supprime pas
            if line in self.lines:
                continue

            # creer la boule avec ses liens
            boule = Boule(
                text=line.text,
                type=line.type,
                parent=self.lines.get(parent))
            links_to_update.append((boule, line))
            self.lines[line] = boule

        for boule, line in links_to_update:
            # Faire des trucs avec les liens (heritage, appels, etc)
            pass

        for line in left:
            self.lines[line].delete()
            del self.lines[line]

    def get_boules(self):
        return self.boules


if __name__ == '__main__':
    bs = BouleStore([__file__])
    bs.update()
    print bs.get_boules()
