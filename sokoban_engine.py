# -*- coding: utf-8 -*-

###

class GameObject(object):

    def __init__(self, symbol, canMove, solid, hidden):
        self.symbol = symbol
        self.canMove = canMove
        self.hidden = hidden
        self.solid = solid
    
    def show(self):
        return self.symbol

    def hide(self, TrueOrFalse):
        self.hidden = TrueOrFalse


class Wall(GameObject):

    def __init__(self):
        super(Wall, self).__init__("#", False, True, False)

class Player(GameObject):

    def __init__(self):
        super(Player, self).__init__("@", True, True, False)
        self.coords = (0, 0)
        self.inStorageSymbol = "+"

    def showInStorage(self):
        return self.inStorageSymbol

class Crate(GameObject):

    def __init__(self):
        super(Crate, self).__init__("o", True, True, False)
        self.inStorageSymbol = "*"
        self.inStorage = False

    def showInStorage(self):
        return self.inStorageSymbol

class Storage(GameObject):

    def __init__(self):
        super(Storage, self).__init__(".", False, False, False)

class Floor(GameObject):

    def __init__(self):
        super(Floor, self).__init__(" ", False, False, False)

###

class Game(object):

    def __init__(self, level = ""):
        self.level = level

    def init(self):
        """Clears the board, reads a new level and initialize the game."""

        self.board = []
        self.player = Player()
        self.crates = {}
        self.levelFinished = False
        self.numberOfMoves = 0
        self.moveHistory = []

        # Manually track (x,y)-coords and loop through each character
        # and create game objects accordingly
        x = 0
        y = 0
        for c in self.level:
            if c == "@":
                self.player.coords = (x, y)
                f = Floor()
                f.hide(True)
                self.board.append(((x, y), f))
            elif c == " ":
                self.board.append(((x, y), Floor()))
            elif c == ".":
                self.board.append(((x, y), Storage()))
            elif c == "o":
                self.crates[(x, y)] = Crate()
                f = Floor()
                f.hide(True)
                self.board.append(((x, y), f))
            elif c == "#":
                self.board.append(((x, y), Wall()))
            elif c == "\n":
                y += 1
                x = 0
                continue
            x += 1

    def changeLevel(self, level):
        self.level = level
        self.init()

    def victory(self):
        return self.levelFinished

    def output(self):
        """Return a string representation of the board"""
        if self.levelFinished:
            return "Congratulations!\n\nYou finished in %d moves." % self.numberOfMoves

        # create and return a string representation of the board
        row = 0
        output = ""
        for (x, y), obj in self.board:
            if y > row:
                output += "\n"
                row += 1
            if not obj.hidden:
                output += obj.show()
            if (x, y) == self.player.coords and isinstance(obj, Storage):
                output += self.player.showInStorage()
            elif (x, y) == self.player.coords:
                output += self.player.show()
            if (x, y) in self.crates:
                if isinstance(obj, Storage):
                    output += self.crates[(x, y)].showInStorage()
                else:
                    output += self.crates[(x, y)].show()

        return output

    def move(self, direction):
        # unpack the direction tuple
        try:
            dirX, dirY = direction
            self.moveHistory.append(direction)
        except:
            return None

        # get current player coords
        oldCoords = self.player.coords
        oldX, oldY = oldCoords

        # get direction
        newX = oldX + dirX
        newY = oldY + dirY

        # make new coords
        newCoords = (newX, newY)
        crateNewCoords = (newX + dirX, newY + dirY)

        # collision detect
        isValidMove, isCrate = self.lookahead(newCoords)

        # act based on the collision detection
        movePlayer = None
        updateCrates = None
        if isValidMove:
            if not isCrate:
                movePlayer = True
            else:
                # make a deeper look and see what's behind the crate
                isValidAgain, anotherCrate = self.lookahead(crateNewCoords)
                # allowed to move the crate
                if isValidAgain and not anotherCrate:
                    # delete the current crate and create a new one on step away
                    del self.crates[newCoords]
                    self.crates[crateNewCoords] = Crate()
                    # update
                    movePlayer = True
                    updateCrates = True
                # cannot move the crate
                else:
                    movePlayer = False
                    updateCrates = False

            # move player
            if movePlayer:
                self.player.coords = newCoords
                self.numberOfMoves += 1

            # loop and update all floors and storages
            for coords, obj in self.board:
                if coords == oldCoords and movePlayer:
                    obj.hide(False)
                elif coords == newCoords:
                    obj.hide(True)
                else:
                    if updateCrates and coords == crateNewCoords:
                        obj.hide(True)
                        if isinstance(obj, Storage):
                            self.crates[crateNewCoords].inStorage = True

            # check to see if all crates are in storage
            if updateCrates:
                for coords, crate in self.crates.items():
                    if not crate.inStorage:
                        self.levelFinished = False
                        break
                    else:
                        self.levelFinished = True

        else:
            pass #invalid move

    def lookahead(self, newCoords):
        isValidMove = True
        isCrate = False
        # loop for walls
        for coords, obj in self.board:
            if coords == newCoords and obj.solid:
                if not obj.canMove:
                    isValidMove = False
                    break
        # check for crate
        if newCoords in self.crates:
            isCrate = True
        # return
        return (isValidMove, isCrate)

    def debug(self):
        for (x, y), obj in self.board:
            print "(%d, %d) %s hidden:%r" % (x, y, repr(type(obj)), obj.hidden)
        px, py = self.player.coords
        print "(%d, %d) Player" % (px, py)

