# -*- coding: utf-8 -*-

class GameObject(object):

    def __init__(self, char, solid = True, movable = True, hidden = False):
        self.char = char
        self.solid = solid
        self.movable = movable

    def __repr__(self):
        return "'%s'" % self.char

class Worker(GameObject):

    def __init__(self):
        super(Worker, self).__init__(char = "@")

class Crate(GameObject):

    def __init__(self):
        super(Crate, self).__init__(char = "o")

class Storage(GameObject):

    def __init__(self):
        super(Storage, self).__init__(char = ".", solid = False, movable = False)

    def __hash__(self):
        return hash(self.char)

    def __eq__(self, other):
        return self.char == other.char

class Floor(GameObject):

    def __init__(self):
        super(Floor, self).__init__(char = " ", solid = False, movable = False)

    def __hash__(self):
        return hash(self.char)

    def __eq__(self, other):
        return self.char == other.char

class Wall(GameObject):

    def __init__(self):
        super(Wall, self).__init__(char = "#", solid = True, movable = False)

    def __hash__(self):
        return hash(self.char)

    def __eq__(self, other):
        return self.char == other.char

class Coord(object):

    def __init__(self, x = False, y = False):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if not self.x and not self.y:
            return False
        else:
            return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return Coord(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        if isinstance(other, Coord):
            return Coord(self.x * other.x, self.y * other.y)
        else:
            return Coord(self.x * other, self.y * other)

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


class Level(object):

    def __init__(self):
        self.board = {}
        self.level = ""

    def loadfile(self, fn):
        try:
            with open(fn) as f:
                self.level = f.read()
        except:
            self.level = "#####\n#@o.#\n#####"

    def readlevel(self):
        self.board = {}
        if not self.level:
            self.loadfile("")
        x = 0
        y = 0
        for c in self.level:
            coord = Coord(x, y)
            if c == "@":
                self.add_object(Worker(), coord)
            elif c == "o":
                self.add_object(Crate(), coord)
            elif c == ".":
                self.add_object(Storage(), coord)
            elif c == "#":
                self.add_object(Wall(), coord)
            elif c == " ":
                self.add_object(Floor(), coord)
            elif c == "\n":
                y += 1
                x = 0
                continue
            x += 1

    def add_object(self, obj, coord):
        if isinstance(obj, Worker) or isinstance(obj, Crate):
            self.board[obj] = []
            self.board[obj].append(coord)
        elif obj in self.board:
            self.board[obj].append(coord)
        else:
            self.board[obj] = []
            self.board[obj].append(coord)

    def get_objects(self, cls, filter_coords = False):
        result = []
        for obj, coords in self.board.iteritems():
            if isinstance(obj, cls):
                # we didn't send the filter
                if not filter_coords:
                    for spot in coords:
                        result.append((spot, obj))
                # match only the right objects and the right coords
                elif filter_coords in coords:
                    result.append((filter_coords, obj))
        # switch X,Y to Y,X - sort on that - and then return
        return sorted(result, key=lambda ((x, y), o): ((y, x), o))

    def update_object(self, obj, delpos, addpos):
        update = [coords for coords, o in self.get_objects(GameObject) if o == obj]
        update.remove(delpos)
        update.append(addpos)
        self.board[obj] = update


class Sokoban(object):

    def __init__(self):
        self.level = Level()

    def load(self, filename = ""):
        if filename:
            self.level.loadfile(filename)
        self.level.readlevel()

    def move(self, (x, y)):
        dirpos = Coord(x, y)
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

    def show(self):
        objects = self.level.get_objects(GameObject)
        result = ""
        row = 0
        for (x, y), obj in objects:
            if y > row:
                result += "\n"
                row += 1
            result += obj.char
        return result

    def finished(self):
        pass


#### TESTING ####

#game = Sokoban()
#
#game.load("levels/sok01.txt")
#
#print game.show()
#game.move(Coord(+0, -1))
#for i in range(10):
#    print game.show()
#    game.move(Coord(-1, +0))
#    i += 1
