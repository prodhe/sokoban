#
#   enginenew.py
#

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

    def __gt__(self, other):
        if self.y > other.y:
            return True
        elif self.y == other.y and self.x > other.x:
            return True
        else:
            return False

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

    def __init__(self, coords, solid=True, movable=False, behind=False):
        self.char = ""
        self.solid = solid
        self.movable = movable
        self.coords = coords
        self.behind = behind

    def __repr__(self):
        return "%s:'%s':s-%r:m-%r" % (self.coords, self.char, self.solid,
                                      self.movable)

    def move(self, dirpos):
        if not self.movable and not self.solid:
            if self.behind:
                self.behind = False
            else:
                self.behind = True
        else:
            self.coords += dirpos

    def show(self):
        return self.char

class Worker(GameObject):

    def __init__(self, coords):
        super(Worker, self).__init__(coords, solid=True, movable=True)
        self.char = "@"
        self.char_on_storage = "+"

class Crate(GameObject):

    def __init__(self, coords):
        super(Crate, self).__init__(coords, solid=True, movable=True)
        self.char = "o"
        self.char_on_storage = "*"
        self.in_storage = False

class Storage(GameObject):

    def __init__(self, coords):
        super(Storage, self).__init__(coords, solid=False, movable=False)
        self.char = "."

class Floor(GameObject):

    def __init__(self, coords, behind=False):
        super(Floor, self).__init__(coords, solid=False, movable=False,
                                    behind=behind)
        self.char = " "

class Wall(GameObject):

    def __init__(self, coords):
        super(Wall, self).__init__(solid = True, movable = False,
                                   coords = coords)
        self.char = "#"


class State(object):
    """Parse a level in text format into objects for corresponding characters
       and keeps a list of the updated objects and current state in game"""

    def __init__(self):
        self.objects = []
        self.level = ""

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
        if not self.level:
            self.loadfile("")
        x = 0
        y = 0
        for c in self.level:
            coords = Coords(x, y)
            if c == "@":
                self.objects.append(Worker(coords))
                self.objects.append(Floor(coords, behind=True))
            elif c == "o":
                self.objects.append(Crate(coords))
                self.objects.append(Floor(coords, behind=True))
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

    def update(self, dirpos, *update_objects):
        """Update the objects given as argument. If a given object is not
           movable nor solid, it will toggle it's behind flag instead"""
        if len(update_objects):
            for obj in update_objects:
                # to check if obj in argument list is valid
                index = self.objects.index(obj)
                if index:
                    self.objects[index].move(dirpos)
            return True
        else:
            return False


class Sokoban(object):
    """Main game logic and API"""

    def __init__(self):
        self.state = State()

    def load(self, filename = ""):
        """Reads a file and load, otherwise just (re)load our current level"""
        if filename:
            self.state.loadfile(filename)
        self.state.loadlevel()

    def player(self):
        """Returns the player object from current state"""
        for obj in self.state.get():
            if isinstance(obj, Worker):
                return obj
        return None

    def move(self, (x, y)):
        """Move the player in (x, y) relative direction if valid"""
        current_state = self.state.get()

        player = [obj for obj in current_state if isinstance(obj, Worker)].pop()

        dirpos = Coords(x, y)
        curpos = player.coords
        newpos = curpos + dirpos
        newpos2 = curpos + dirpos*2

        blockobjs = self.relative_objects(current_state, curpos, dirpos)
        blockobjs.reverse()
        blockobjs.pop()
        blockobjs.reverse()
        log.write("blocking: %r" % blockobjs)

        if blockobjs[1].solid and not blockobjs[1].movable:
            return False
        elif blockobjs[1].solid and blockobjs[1].movable:
            if blockobjs[2].solid:
                return False
            else:
                if self.state.update(dirpos, player, blockobjs[0], blockobjs[1], blockobjs[2]):
                    return True
                else:
                    log.write("error moving double blocks")
                    return False
        else:
            log.write("valid move to %s" % newpos)
            if self.state.update(dirpos, player, blockobjs[0], blockobjs[1]):
                return True
            else:
                log.write("error moving %s to %s" % (player, dirpos))
                return False

    def relative_objects(self, state, curpos, dirpos):
        newpos = curpos + dirpos
        newpos2 = curpos + dirpos*2
        log.write("get block for %s, %s and %s" % (curpos, newpos, newpos2))
        result = [obj for obj in state if obj.coords == curpos or
                                          obj.coords == newpos or
                                          obj.coords == newpos2]
        result.reverse() # so our nearest blocking object is at index 0
        return result

    def undo(self):
        pass

    def output(self):
        objects = self.state.get()
        print "%r" % [obj for obj in objects if isinstance(obj, Worker)]
        result = ""
        row = 0
        for obj in objects:
            if obj.coords[1] > row:
                result += "\n"
                row += 1
            if not obj.behind:
                result += obj.show()
        return result

    def finished(self):
        pass


#### TESTING ####

game = Sokoban()

game.load("")
#game.start("levels/sok01.txt")


print game.output()
game.move((+0, -1))
print game.output()
game.move((+0, -1))
print game.output()
game.move((+0, -1))
print game.output()
game.move((+0, -1))
#for i in range(10):
#    print game.output()
#    print "%r" % game.move(Coords(-1, +0))
#    i += 1

print "-" * 10
print log.count(0)
