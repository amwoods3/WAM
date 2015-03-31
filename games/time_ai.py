import subprocess
import resource
import json
def set_limit(seconds):
    soft, hard = resource.getrlimit(resource.RLIMIT_CPU)
    resource.setrlimit(resource.RLIMIT_CPU,
                       (seconds, hard))

def run_ai(ai, board, time_limit, turn):
    cmd = "python run_ai.py"
    file("run_ai.py", 'w').write("""import %s as ai
print ai.get_move('%s', %s, '%s')
    """ % (ai, json.JSONEncoder().encode(board), str(time_limit), turn))
    t0 = resource.getrusage(resource.RUSAGE_CHILDREN)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, preexec_fn= lambda : set_limit(time_limit/1000.0))
    p.wait()
    t1 = resource.getrusage(resource.RUSAGE_CHILDREN)
    time_taken = ((t1.ru_utime + t1.ru_stime) - (t0.ru_utime + t0.ru_stime)) * 1000
    print "time_limit:", time_limit
    print "time_taken:", time_taken
    try:
        result = json.JSONDecoder().decode(p.communicate()[0])
    except ValueError:
        print "Time out!!"
        result = [9999, 9999]
    return (result, time_taken)
    
    
