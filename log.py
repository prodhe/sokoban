# log handling
class Log(object):

    def __init__(self):
        self.log = []

    def __repr__(self):
        return "\n".join(self.log)

    def write(self, msg):
        s = "%d: %s" % (len(self.log) + 1, msg)
        self.log.append(s)
