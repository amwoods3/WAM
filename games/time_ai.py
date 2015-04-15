import subprocess
import resource
import json
import os
import sys
from config import AI_PATH

def set_limit(seconds):
    soft, hard = resource.getrlimit(resource.RLIMIT_CPU)
    resource.setrlimit(resource.RLIMIT_CPU,
                       (seconds, soft))

def run_ai(ai_info, board, time_limit, turn):
    cmd = "python run_ai.py"
    print type(board)
    file("run_ai.py", 'w').write("""import %s.""" % AI_PATH +"""%(user)s.%(ai)s as ai""" % ai_info + """
print ai.get_move('%s', %s, '%s')
    """ % (json.dumps(board.state), str(time_limit), turn))
    
    t0 = resource.getrusage(resource.RUSAGE_CHILDREN)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, preexec_fn=set_limit(time_limit/1000.0))
    p.wait()
    t1 = resource.getrusage(resource.RUSAGE_CHILDREN)
    time_taken = ((t1.ru_utime + t1.ru_stime) - (t0.ru_utime + t0.ru_stime)) * 1000 # need time_taken in miliseconds, we want to use for ai records
    result_tuple = p.communicate()
    result_str = result_tuple[0]
    try:
        print result_tuple
        result = json.loads(result_str)
    except ValueError ,msg: # will happen if AI doesn't have enough time to return value
        print "Time out!!!!!"
        result = [9999, 9999]
    os.system("rm run_ai.py")
    return (result, time_taken)
    
    
