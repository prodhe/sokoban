#
#   log.py
#

import traceback

# log handling
class Log(object):

    def __init__(self):
        self.log = []

    def __repr__(self):
        return "%s" % (self.log[-1])

    def count(self, count = 0):
        if count == 0:
            return "\n".join(self.log)
        else:
            start = len(self.log) - count
            stop = len(self.log)
            try:
                return "\n".join(self.log[start:stop])
            except IndexError:
                return "\n".join(self.log)

    def write(self, msg):
        stack = traceback.extract_stack()
        try:
            call = stack.pop(-3)
        except IndexError:
            call = stack.pop(-2)
        s = "%s:%d: in %s : %s: %s" % (call[0], call[1], call[2], call[3], msg)
        self.log.append(s)
