# Async Hulk - HTTPS Unbearable Load King - HULK v3
-----------------------------------------------------------------------------------------------
![Python Version](https://img.shields.io/badge/python-3.8+-blue?style=for-the-badge)
![License](https://img.shields.io/badge/License-GNU-green?style=for-the-badge)
![Codacy branch grade](https://img.shields.io/codacy/grade/c4f7560e8231423691d819129c7b3afa/async?style=for-the-badge)

## Introduction

 This script is a *Distributed Denial of Service* tool that can put heavy load on HTTPS servers,\
 in order to bring them to their knees, by exhausting the resource pool.
 
 Its is meant for research purposes only and any malicious usage of this tool is prohibited.
 
 **The authors aren't to be held responsible for any consequence of usage of this tool.**


### Authors
|         Name       | Version |
|--------------------|---------|
| **Hyperclaw79**    |   2.0+  |
| **Barry Shteiman** |   1.0   |


 ### Notes
     * Edited and improved by Hyperclaw79 for smoother working and PY3+ compatibility.
     * Now works with an asynchronous model.
     * Works for Python 3.8+.
        > No backward compatiblity.
 
-----------------------------------------------------------------------------------------------

## Changelog
### v3.1
    1. Refactored the code to make it more performant.
    2. Standardized the code using PEP8 and Pylint.
    3. Switched to Multithreaded Asyncio.
    4. Added a new Launcher script to launch either the Client or the Server.
    5. Added Argument Parser to increase the flexibility of the tool.
    6. Fixed bugs in HTTP Requests.
    7. Fixed bugs in botnet communication.
    8. Enhanced Logging for Server.
    9. Added Stealth Mode for Hulk Client.
    10. Improved documentation and overall readability.

### v3.0
    1. Switched from Multiprocessing to asynchronous event loops.
    2. Included a Root Server to control all bots for a DDoS.
    3. Fixed some issues with request generation and headers.
    4. Improved attack and overall performance.
    5. Switched to Json Payload for POST attacks.
    6. Synchronized target status across all bots.
    7. Bots are reusable if the target isn't down within 500 attacks.
    8. Improved Documentation.
    9. Added optional Persistence after successful DDoS.
### v2.0
    1)Syntax Corrections.
    2)Replaced urllib2 module with requests module.
    3)Replaced support for Http with support for Https.
    4)Added more HTTP Status Error Codes for detection and control.
    5)Randomized buildblock size a bit more.
    6)Deprecated 'safe'.
    7)Improved Documentation.
    8)Payload Obfuscation.
    9)Converted global variables to class variables.
    10)Replaced Threading with Multiprocessing.
    11)Introduced Shared Memory for interprocess communication. 
    12)Performed other performance tweaks.

-------------------------------------------------------------------------------------------------
## Usage

1.  Run `pip install -r requirements_(linux/win).txt` before starting this script.
    > Ex: On Windows: `pip install -r requirements_win.txt`
    > Ex: On Linux: `pip install -r requirements_linux.txt`

2.  Launch the `hulk_launcher.py server` with the target website as arg.
    > Ex: `python hulk_launcher.py server https://testdummysite.com`
    >
    > Append `--persistent False` to kill the botnet after a succesfull DDoS.

3.  Launch the `hulk_launcher.py client` to spawn multiple processes of hulk - one per CPU Core.
    > Ex: `python hulk_launcher.py client [localhost]`
    >
    > If the server is running remotely, replace localhost with the server's IP.

4.  Sit back and sip your coffee while the carnage unleashes! >:D

-------------------------------------------------------------------------------------------------
## Syntax Help

### Client
    usage: hulk_launcher.py client [-h] [-r ROOT_IP] [-p ROOT_PORT] [-n NUM_PROCESSES] [-s]

    The Hulk Bot Launcher

    options:
    -h, --help            show this help message and exit
    -r ROOT_IP, --root_ip ROOT_IP
                            IPv4 Address where Hulk Server is running.
    -p ROOT_PORT, --root_port ROOT_PORT
                            Port where Hulk Server is running.
    -n NUM_PROCESSES, --num_processes NUM_PROCESSES
                            Number of processes to launch.
    -s, --stealth         Stealth mode.

### Server
    usage: hulk_launcher.py server [-h] [-p PORT] [-m MAX_MISSILES] [--persistent] target

    The Hulk Server Launcher

    positional arguments:
    target                The target url.

    options:
    -h, --help            show this help message and exit
    -p PORT, --port PORT  The port to bind the server to.
    -m MAX_MISSILES, --max_missiles MAX_MISSILES
                            The maximum number of missiles to connect to.
    --persistent          Continue attacks after target is down.

-------------------------------------------------------------------------------------------------
## License

HULK v3 is a Python 3 compatible Asynchronous Distributed Denial of Service Script.\
[Original script](http://www.sectorix.com/2012/05/17/hulk-web-server-dos-tool/) was created by Barry Shteiman.
You can use that one if you have Python 2.

Using a GNU license cause there was no mention about any license used by Barry.
Feel free to modify and share it, but leave some credits to us both and don't hold us liable.
