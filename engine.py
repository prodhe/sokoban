#
#   enginenew.py
#


# get log handling
from log import Log
log = Log()


#####


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

    def __gt__(self, other):
        if self.y > other.y:
            return True
        elif self.y == other.y and self.x > other.x:
            return True
        else:
            return False

    def __add__(self, other):
        return Coords(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Coords(self.x - other.x, self.y - other.y)

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


#####


class GameObject(object):
    """Parent class for all objects in the game"""

    def __init__(self, coords, solid=True, movable=False, beneath=False):
        self.char = [""]
        self.char_to_show = 0
        self.solid = solid
        self.movable = movable
        self.coords = coords
        self.beneath = beneath
        self.authority = False  # if allowed to ask another solid object to move

    def __repr__(self):
        return "('%s':%s:s-%r:m-%r:b-%r:a-%r)" % (self.show(), self.coords, self.solid,
                                      self.movable, self.beneath, self.authority)

    def move(self, dirpos, objects, authority):
        if self.movable and self.solid:  # worker, crate
            if authority:
                newpos = self.coords + dirpos
                # ask our neighbour(s) for movement
                neighbours = self.neighbours(newpos, objects)
                log.write("GameObject.move(): %s\n\tmy neighbours:\n\t%s" % (self, neighbours))
                for obj in neighbours:
                    log.write("GameObject.move(): %s\n\tasking %s" % (self, obj))
                    if not obj.move(dirpos, objects, self.authority):
                        return False
                
                # if I'm here all my neighbours can move and so can I :-)
                # I must make sure the one beneath me wakes up
                beneath = filter(lambda obj: obj.coords == self.coords and obj.beneath, objects)
                for obj in beneath:
                    log.write("GameObjects.move(): %s\n\tthese are beneath me:\n\t%s" % (self, beneath))
                    obj.move(dirpos, objects)

                self.coords = newpos
                log.write("GameObjects.move(): %s\n\tmoved" % (self))

                # we had a successful move
                return True
            else:
                log.write("GameObject.move(): %s\n\tThe request does not come from an authority" % self)
                return False
        else:
            log.write("GameObject.move(): %s\n\tI'm neither movable nor solid" % self)
            return False
            
    def neighbours(self, pos, objects):
        # filter on given position
        neighbours = filter(lambda obj: obj.coords == pos, objects)
        # sort on visible first - False > True
        neighbours.sort(key=lambda obj: obj.beneath)
        return neighbours

    def show(self):
        """Always show the first char, if there's more than one..."""
        return self.char[self.char_to_show]

class Worker(GameObject):

    def __init__(self, coords):
        super(Worker, self).__init__(coords, solid=True, movable=True)
        self.char = ["@", "+"]
        self.authority = True

    def move(self, dirpos, objects):
        valid_move = super(Worker, self).move(dirpos, objects, authority=True)
        if valid_move:
            for obj in filter(lambda obj: obj.beneath, self.neighbours(self.coords, objects)):
                if isinstance(obj, Storage):
                    self.char_to_show = 1
                else:
                    self.char_to_show = 0
        return valid_move

class Crate(GameObject):

    def __init__(self, coords):
        super(Crate, self).__init__(coords, solid=True, movable=True)
        self.char = ["o", "*"]
        self.in_storage = False
        self.authority = False

    def move(self, dirpos, objects, authority):
        valid_move = super(Crate, self).move(dirpos, objects, authority)
        if valid_move:
            for obj in filter(lambda obj: obj.beneath, self.neighbours(self.coords, objects)):
                if isinstance(obj, Storage):
                    self.char_to_show = 1
                    self.in_storage = True
                else:
                    self.char_to_show = 0
                    self.in_storage = False
        return valid_move

class Storage(GameObject):

    def __init__(self, coords):
        super(Storage, self).__init__(coords, solid=False, movable=False)
        self.char = ["."]

    def move(self, *args):
        if self.beneath:
            self.beneath = False
            log.write("Storage.move(): %s\n\tback in the light" % self)
        else:
            self.beneath = True
            log.write("Storage.move(): %s\n\tinto the shadows" % self)
        return True

class Floor(GameObject):

    def __init__(self, coords, beneath=False):
        super(Floor, self).__init__(coords, solid=False, movable=False,
                                    beneath=beneath)
        self.char = [" "]

    def move(self, *args):
        if self.beneath:
            self.beneath = False
            log.write("Floor.move(): %s\n\tback in the light" % self)
        else:
            self.beneath = True
            log.write("Floor.move(): %s\n\tinto the shadows" % self)
        return True

class Wall(GameObject):

    def __init__(self, coords):
        super(Wall, self).__init__(coords, solid=True, movable=False)
        self.char = ["#"]

    def move(self, *args):
        log.write("Wall.move(): %s\n\tI can't move" % self)
        return False


#####


class State(object):
    """Parse a level in text format into objects for corresponding characters
       and keeps a list of the updated objects and current state in game"""

    def __init__(self):
        self.objects = []
        self.level = ""
        self.moves = 0

    def loadfile(self, fn):
        """Tries to load <fn> and save as string,
           otherwise hard coded default"""
        try:
            with open(fn) as f:
                self.level = f.read()
                log.write("loaded %s" % fn)
        except:
            self.level  = " ####### \n"
            self.level += "#       #\n"
            self.level += "# @ o . #\n"
            self.level += "#       #\n"
            self.level += " ####### "
            log.write("adding default level")

    def loadlevel(self):
        """Reads the level string into proper game objects"""
        self.objects = []
        self.moves = 0
        if not self.level:
            self.loadfile("")
        x = 0
        y = 0
        for c in self.level:
            coords = Coords(x, y)
            if c == "@":
                self.objects.append(Worker(coords))
                self.objects.append(Floor(coords, beneath=True))
            elif c == "o":
                self.objects.append(Crate(coords))
                self.objects.append(Floor(coords, beneath=True))
            elif c == ".":
                self.objects.append(Storage(coords))
            elif c == "#":
                self.objects.append(Wall(coords))
            elif c == " ":
                self.objects.append(Floor(coords))
            elif c == "\n":
                y += 1
                x = 0
                continue
            x += 1

    def get(self):
        """Returns a clean, sorted and filtered list of objects"""
        immovable_objects = filter(lambda obj: not obj.movable, self.objects)
        movable_objects = filter(lambda obj: obj.movable, self.objects)
        result = immovable_objects + movable_objects
        return sorted(result, key=lambda obj: obj.coords)

    def update(self, dirpos):
        player = filter(lambda obj: isinstance(obj, Worker), self.objects).pop()
        valid_move = player.move(dirpos, self.objects)
        if valid_move:
            self.moves += 1
        return valid_move

    def finished(self):
        not_done = [obj for obj in self.objects if isinstance(obj, Crate) and not obj.in_storage]
        log.write("State.finished():\n\t%r" % not_done)
        return not not_done


class Sokoban(object):
    """Main game logic and API"""

    def __init__(self):
        self.state = State()

    def load(self, filename = ""):
        """Reads a file and load, otherwise just (re)load our current level"""
        if filename:
            self.state.loadfile(filename)
        self.state.loadlevel()

    def move(self, (x, y)):
        """Demand a state update with the given direction coordinates"""
        dirpos = Coords(x, y)
        return self.state.update(dirpos)

    def undo(self):
        pass

    def output(self):
        if self.state.finished():
            result  = "Congratulations!\n\n"
            result += "You finished in %d moves.\n\n" % self.state.moves
            result += "Press SPACE"
            return result
        else:
            objects = self.state.get()
            result = ""
            row = 0
            for obj in objects:
                if obj.coords[1] > row:
                    result += "\n"
                    row += 1
                if not obj.beneath:
                    result += obj.show()
            return result

    def finished(self):
        return self.state.finished()


#
# EOF
#
