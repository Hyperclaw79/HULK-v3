# Async Hulk - HTTPS Unbearable Load King - HULK v3
-----------------------------------------------------------------------------------------------
![Python Version](https://img.shields.io/badge/python-3.6%20%7C%203.7-blue?style=for-the-badge)
![License](https://img.shields.io/badge/License-GNU-green?style=for-the-badge)
![Platform](https://img.shields.io/badge/platform-Windows--10-lightgrey?style=for-the-badge)
![Codacy grade](https://img.shields.io/codacy/grade/a5939f58e4c44daebfbe46937686050b?style=for-the-badge)

## Introduction

 > This script is a *Distributed Denial of Service* tool that can put heavy load on HTTPS servers,
 > in order to bring them to their knees, by exhausting the resource pool.
 > Its is meant for research purposes only and any malicious usage of this tool is prohibited.
 > **The authors aren't to be held responsible for any consequence of usage of this tool.**

 Authors : **Hyperclaw79**, *version 3.0, 2.0*; **Barry Shteiman** , *version 1.0*

 ### Notes
     * Edited and improved by Hyperclaw79 for smoother working and PY3+ compatibility.
     * Now works with an asynchronous model.
     * Works for Python 3.6, 3.7. No backward compatiblity.
 
-----------------------------------------------------------------------------------------------

## Edits
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

1.  Run `pip install -r requirements.txt` before starting this script.

2.  Launch the `hulk-server.py` with the target website as arg.
    >  `python hulk-server.py https://testdummysite.com`
    >> Append `--persistent` at the end of the above command if you want a continuous attack even after a succesfull DDoS.
    >> You can press `Ctrl` + `C` (KeyboardInterrupt) to stop and change the target.

3.  Launch the `hulk-launcher.py` to spawn multiple processes of hulk - one per CPU Core.
    >  `python hulk-launcher.py localhost`
    >  If it's a bot on a remote client, replace localhost with the server's IP.

4.  Sit back and sip your coffee while the carnage unleashes! >:D
-------------------------------------------------------------------------------------------------

## License

HULK v3 is a Python 3 compatible Asynchronous Distributed Denial of Service Script.
[Original script](http://www.sectorix.com/2012/05/17/hulk-web-server-dos-tool/) was created by Barry Shteiman.
You can use that one if you have Python 2.

Using a GNU license cause there was no mention about any license used by Barry.
Feel free to modify and share it, but leave some credits to us both and don't hold us liable.
