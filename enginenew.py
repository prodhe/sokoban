# -*- coding: utf-8 -*-

class GameObject(object):

    def __init__(self, char):
        self.char = char

class Worker(GameObject):

    def __init__(self):
        super(Worker, self).__init__(char = "@")

class Crate(GameObject):

    def __init__(self):
        super(Crate, self).__init__(char = "o")

class Storage(GameObject):

    def __init__(self):
        super(Storage, self).__init__(char = ".")

class Floor(GameObject):

    def __init__(self):
        super(Floor, self).__init__(char = " ")

class Wall(GameObject):

    def __init__(self):
        super(Wall, self).__init__(char = "#")


class Level(object):

    def __init__(self):
        self.board = {}
        self.level = ""

    def loadFile(self, fn):
        with open(fn) as f:
            self.level = f.read()

    def readLevel(self):
        x = 0
        y = 0
        for c in self.level:
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

    def getObjects(self, cls, filterCoords = ()):
        result = []
        for coords, obj in self.board.iteritems():
            if isinstance(obj, cls):
                # we didn't send the filter
                if not filterCoords:
                    result.append((coords, obj))
                # match only the right objects and the right coords
                elif coords == filterCoords:
                    result.append((coords, obj))
        # switch X,Y to Y,X - sort on that - and then return
        return sorted(result, key=lambda ((x, y), o): (y, x))


class Sokoban(object):

    def __init__(self):
        self.level = Level()

    def load(self, filename = ""):
        if filename:
            self.level.loadFile(filename)
        self.level.readLevel()

    def move(self, (dirX, dirY)):
        pass

    def undo(self):
        pass

    def show(self):
        objects = self.level.getObjects(GameObject)
        result = ""
        row = 0
        for (x, y), obj in objects:
            if y > row:
                result += "\n"
                row += 1
            result += obj.char
        return result


#### TESTING ####

game = Sokoban()

game.load("levels/sok01.txt")
print game.show()

print "%r" % game.level.getObjects(Wall, (10, 8))
