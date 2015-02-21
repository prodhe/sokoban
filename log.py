#
#   log.py
#

import traceback

# log handling
class Log(object):

    def __init__(self):
        self.log = []

    def __repr__(self):
        return "\n".join(self.log)

    def write(self, msg):
        stack = traceback.extract_stack()
        print "%r" % stack
        try:
            call = stack.pop(-3)
        except IndexError:
            call = stack.pop(-2)
        for field in call:
            print "%r" % (field),
        print "\n" + "-" * 10
        s = "%s:%d: in %s : %s: %s" % (call[0], call[1], call[2], call[3], msg)
        self.log.append(s)
