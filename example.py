import multiprocessing
import resource
import signal

def count(x):
    y = 1
    while y != x: # this won't end...
        y += 1 

class TimeOutException(Exception): pass
def time_out(signum, frame):
    raise TimeOutException, "Time Out!!"

def call_function(func, time, * args):
    p = multiprocessing.Process(target=func, args=args)
    soft, hard = resource.getrlimit(resource.RLIMIT_CPU)
    resource.setrlimit(resource.RLIMIT_CPU,
                       (time, hard))
    signal.signal(signal.SIGXCPU, time_out) # want to halt process if takes too long
    try:
        p.start() # start process
        while p.is_alive(): # wait for process to finish
            pass
        signal.pause() # don't need signal anymore
        p.join() 
    except TimeOutException, msg:
        p.join()
        print msg
        return False
    return True
    
def test(func, time):
    while 1:
        if not call_function(func, time, 0):
            break
    print "done testing"
    
