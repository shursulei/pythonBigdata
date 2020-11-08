from subprocess import call
import time
import sys
class BaseArgs(object):
    """ Base Argument Class that handles keyword argument parsing"""
def _init_(self,*args,**kwargs):
    self.args= args
    self.kwargs=kwargs
    if self.kwargs.has_key("delay"):
        self.delay=self.kwargs["delay"]
    else:
        self.delay=0
    if self.kwargs.has_key("verbose"):
        self.verbose=self.kwargs["verbose"]
    else:
        self.verbose=False
    def run(self):
        raise NotImplementedError
        class Runner(BaseArgs):
           ""
    def run(self):
        for cmd in self.args:
            if self.verbose:
                print("Running %s with delay=%s" % (cmd,self.delay))
            time.sleep(self.delay)
            call(cmd,shell=True)
