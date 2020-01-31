import os
import sys
import subprocess

cores = os.cpu_count()
python = 'python'
if sys.platform.lower() == "linux":
    python = "python3"
root_ip = "localhost"
if len(sys.argv) > 1:
    root_ip = sys.argv[1]
processes = [
    subprocess.Popen(
        [python, 'hulk.py' , root_ip],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )
    for i in range(cores)
]