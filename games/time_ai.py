import subprocess
import resource
import json
def set_limit(seconds):
    soft, hard = resource.getrlimit(resource.RLIMIT_CPU)
    resource.setrlimit(resource.RLIMIT_CPU,
                       (seconds, soft))

def run_ai(ai_info, board, time_limit, turn):
    cmd = "python run_ai.py"
    
    file("run_ai.py", 'w').write("""import wam.ais.%(user)s.%(ai)s as ai""" % ai_info + """
print ai.get_move('%s', %s, '%s')
    """ % (json.JSONEncoder().encode(board), str(time_limit), turn))
    
    t0 = resource.getrusage(resource.RUSAGE_CHILDREN)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, preexec_fn=set_limit(time_limit/1000.0))
    p.wait()
    t1 = resource.getrusage(resource.RUSAGE_CHILDREN)
    time_taken = ((t1.ru_utime + t1.ru_stime) - (t0.ru_utime + t0.ru_stime)) * 1000 # need time_taken in miliseconds, we want to use for ai records
    print "Time left: ", time_limit
    print "Time taken: ", time_taken
    print p.communicate()
    try:
        result = json.JSONDecoder().decode(p.communicate()[0])
    except ValueError: # will happen if AI doesn't have enough time to return value
        print "Time out!!"
        result = [9999, 9999]
    return (result, time_taken)
    
    
