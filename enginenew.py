# -*- coding: utf-8 -*-

class GameObject(object):

    def __init__(self):
        pass

class Worker(GameObject):

    def __init__(self):
        pass

class Crate(GameObject):

    def __init__(self):
        pass

class Storage(GameObject):

    def __init__(self):
        pass

class Floor(GameObject):

    def __init__(self):
        pass

class Wall(GameObject):

    def __init__(self):
        pass


class Level(object):

    def __init__(self):
        self.board = None  #{(0, 0): []}
        self.level = ""

    def loadFile(self, fn):
        with open(fn) as f:
            self.level = f.read()

    def loadLevel(self):
        for c in self.level:
            x = 0
            y = 0
            if c == "@":
                self.board[(x, y)] = Worker()
            elif c == " ":
                self.board[(x, y)] = Floor()
            elif c == ".":
                self.board[(x, y)] = Storage()
            elif c == "o":
                self.board[(x, y)] = Crate()
                pass
            elif c == "#":
                self.board[(x, y)] = Wall()
                pass
            elif c == "\n":
                y += 1
                x = 0
                continue
            x += 1

    def getObject(self, (x, y)):
        return self.board[(x, y)]


class Engine(object):

    def __init__(self):
        self.level = Level()

    def move(self):
        pass

    def undo(self):
        pass


#### TESTING ####


