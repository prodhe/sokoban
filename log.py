#
#   log.py
#

import traceback

# log handling
class Log(object):

    def __init__(self):
        self.log = []
        self.new_items = 0

    def __repr__(self):
        if self.new_items:
            s = self.count(self.new_items)
            self.new_items = 0
            return "\n%s\n" % s
        else:
            return ""
        #return "%s" % (self.log[-1])

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
        #s = "%s:%d: in %s : %s:\n    >>> %s" % (call[0], call[1], call[2], call[3], msg)
        s = "%s\n" % msg
        self.log.append(s)
        self.new_items += 1

#
# EOF
#
