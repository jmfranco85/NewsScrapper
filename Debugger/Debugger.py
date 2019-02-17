#
# Class Debugger
#


class Debugger:
    
    def __init__(self, debugger_level):
        if debugger_level:
            self.debugger_level = debugger_level
        else:
            self.debugger_level = 0
    
    def debug(self, message, level=1):
        if self.debugger_level >= level:
            print(message)
