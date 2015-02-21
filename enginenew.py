# -*- coding: utf-8 -*-

# get log handling
from log import Log
log = Log()

class Coords(object):
    """Custom class for working with x,y coordinates"""

    def __init__(self, x = False, y = False):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if not self.x and not self.y:
            return False
        else:
            return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return Coords(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        if isinstance(other, Coords):
            return Coords(self.x * other.x, self.y * other.y)
        else:
            return Coords(self.x * other, self.y * other)

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise IndexError

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        else:
            raise IndexError

    def __repr__(self):
        return "(%d,%d)" % (self.x, self.y)

class GameObject(object):
    """Parent class for all objects in the game"""

    def __init__(self, char, solid, movable, coords):
        self.char = char
        self.solid = solid
        self.movable = movable
        self.coords = coords

    def __repr__(self):
        return "%s:'%s'" % (self.coords, self.char)

    def move(newpos):
        if not movable:
            return false
        return true

class Worker(GameObject):

    def __init__(self, coords = Coords()):
        super(Worker, self).__init__(char = "@", solid = True, movable = True, coords = coords)

class Crate(GameObject):

    def __init__(self, coords = Coords()):
        super(Crate, self).__init__(char = "o", solid = True, movable = True, coords = coords)

class Storage(GameObject):

    def __init__(self, coords = Coords()):
        super(Storage, self).__init__(char = ".", solid = False, movable = False, coords = coords)

class Floor(GameObject):

    def __init__(self, coords = Coords()):
        super(Floor, self).__init__(char = " ", solid = False, movable = False, coords = coords)

class Wall(GameObject):

    def __init__(self, coords = Coords()):
        super(Wall, self).__init__(char = "#", solid = True, movable = False, coords = coords)

class Level(object):
    """Keeps track of all the objects in a given level"""

    def __init__(self):
        self.board = {}
        self.objects = []
        self.level = ""
        self.player = Worker()

    def loadfile(self, fn):
        try:
            with open(fn) as f:
                self.level = f.read()
                log.write("level from %s" % fn)
        except:
            self.level = " ####### \n#       #\n# @ o . #\n#       #\n ####### "
            log.write("default level")

    def loadlevel(self):
        self.objects = []
        if not self.level:
            self.loadfile("")
        x = 0
        y = 0
        for c in self.level:
            coords = Coords(x, y)
            if c == "@":
                self.player.coords = coords
                self.objects.append(self.player)
            elif c == "o":
                self.objects.append(Crate(coords = coords))
            elif c == ".":
                self.objects.append(Storage(coords = coords))
            elif c == "#":
                self.objects.append(Wall(coords = coords))
            elif c == " ":
                self.objects.append(Floor(coords = coords))
            elif c == "\n":
                y += 1
                x = 0
                continue
            x += 1
        print "%r" % self.objects


class Sokoban(object):
    """Main game logic and API"""

    def __init__(self):
        self.level = Level()

    def start(self, filename = ""):
        if filename:
            self.level.loadfile(filename)
        self.level.loadlevel()

    def move(self, (x, y)):
        dirpos = Coords(x, y)
        curpos, worker = self.level.get_objects(Worker).pop()
        newpos = curpos + dirpos
        blocking_objects = self.blocking_objects(newpos)
        print "blocking: %r" % blocking_objects
        valid_move = True
        for obj in blocking_objects:
            if not obj.movable and obj.solid:
                valid_move = False
            elif not obj.movable and not obj.solid:
                valid_move = True
                self.level.update_object(obj, newpos, curpos)
            else:
                newpos2 = curpos + dirpos*2
                newpos2, nextobj = self.level.get_objects(GameObject, newpos2).pop()
                if nextobj.solid:
                    valid_move = False
                else:
                    valid_move = True
                    self.level.update_object(obj, newpos, newpos2)
        if valid_move:
            self.level.update_object(worker, curpos, newpos)
            print "moved to: %r" % (newpos)
        else:
            print "%s invalid move" % curpos

    def blocking_objects(self, coords):
        return [obj for coords, obj in
                self.level.get_objects(GameObject, coords)]

    def undo(self):
        pass

    def output(self):
        objects = self.level.objects
        result = ""
        row = 0
        for obj in objects:
            if obj.coords[1] > row:
                result += "\n"
                row += 1
            result += obj.char
        return result

    def finished(self):
        pass


#### TESTING ####

game = Sokoban()

game.start("")

print game.output()

#game.move(Coords(+0, -1))
#for i in range(10):
#    print game.show()
#    game.move(Coords(-1, +0))
#    i += 1

print log
