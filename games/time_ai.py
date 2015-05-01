import subprocess
import resource
import json
import os
import sys
from config import AI_PATH

def set_limit(seconds):
    soft, hard = resource.getrlimit(resource.RLIMIT_CPU)
    resource.setrlimit(resource.RLIMIT_CPU,
                       (seconds, hard))

def convert_data_structure(d):
    my_format = []
    for l in d:
        x = []
        for mv in l:
            x.append(mv[0])
            x.append(mv[1])
        my_format.append(x)
    return my_format

def run_ai(ai_info, board, time_limit, turn, game_type):
    cmd = "python run_ai.py"
    print type(board)
    file("run_ai.py", 'w').write("""import %s.""" % AI_PATH +"""%(user)s.%(ai)s as ai""" % ai_info + """
move = ai.get_move('%s', %s, '%s')
print ' '
print ' '
print move
    """ % (json.dumps(board), str(time_limit), turn))
    
    t0 = resource.getrusage(resource.RUSAGE_CHILDREN)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, preexec_fn=set_limit(time_limit/1000.0))
    p.wait()
    t1 = resource.getrusage(resource.RUSAGE_CHILDREN)
    time_taken = ((t1.ru_utime + t1.ru_stime) - (t0.ru_utime + t0.ru_stime)) * 1000 # need time_taken in miliseconds, we want to use for ai records
    try:
        result_tuple = p.communicate()
        #print result_tuple
        result_str = result_tuple[0].split('\n')[-2]
    except:
        result = "Time out!!!"
        return (result, time_taken)
    try:
        #print result_tuple
        #print result_str
        result = json.loads(result_str)
    except:
        result = "%s is not JSON serializable!!!" % (result_str)
        return (result, time_taken)
    try:
        if game_type == 'checkers':
            print game_type
            result = convert_data_structure(result)
        else:
            print "not checkers"
    except:
        result = "%s does not follow the format!!!" % (result)
    os.system("rm run_ai.py")
    return (result, time_taken)
    
    
