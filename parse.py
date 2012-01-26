# -*- coding: utf8 -*-

import re


LINE_TYPES = {
    'FILE': re.compile(r'(\w\.py)'),
    'CLASS': re.compile(r'^class (\w*)'),
    'DEF': re.compile(r'^def (\w)*'),
}


class Line:
    def __init__(self, text, parent):
        self.text = text
        self.parent = parent
        self.type = ''
        for type, reg in LINE_TYPES.iteritems():
            m = reg.search(text)
            if m:
                self.type = type
                self.name = m.group()
                break

    def __repr__(self):
        return "Line(%s)" % repr(self.text)

    def __hash__(self):
        return hash(self.parent) ^ hash(self.text)


def parse(filename):
    indent_width = 1
    root = Line(filename, None)
    yield root, None
    refs = {-1: root}

    with open(filename) as f:
        for line in f.readlines():
            spaces = re.search(r'\A[ \t]*', line).end()
            if spaces + 1 == len(line) or line.strip().startswith('#'):
                continue

            # Depth normalization
            if indent_width == 1 and spaces != 0:
                indent_width = spaces
            depth = spaces / indent_width

            obj = Line(line.strip(), refs[depth - 1])
            refs[depth] = obj
            if obj.type:
                yield obj, refs[depth - 1]


if __name__ == '__main__':
    for line, parent in parse(__file__):
        print(line, parent)
