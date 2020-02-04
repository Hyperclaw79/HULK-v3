import os
import sys
import subprocess

cores = os.cpu_count()
python = 'python3'
flag = 0
if sys.platform.startswith('win'):
    python = "python"
    flag = subprocess.CREATE_NEW_CONSOLE
root_ip = "localhost"
if len(sys.argv) > 1:
    root_ip = sys.argv[1]
processes = [
    subprocess.Popen(
        [python, 'hulk.py' , root_ip],
        creationflags=flag
    )
    for i in range(cores)
]
