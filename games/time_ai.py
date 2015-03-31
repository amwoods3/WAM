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
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, preexec_fn= lambda : set_limit(time_limit/1000.0))
    result = json.JSONDecoder().decode(p.communicate()[0])
    return result
    
    
