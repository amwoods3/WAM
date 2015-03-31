import subprocess

file('main.py', 'w').write('''
print 1 + 2
''')
cmd = 'python main.py'
subprocess.Popen(cmd, shell=True,
                 stdout=subprocess.PIPE,
                 stderr=subprocess.PIPE)

