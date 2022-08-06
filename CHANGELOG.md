## Changelog
### v3.2
    1. Added a (NextJs) GUI to show the bots in action.
    2. Project-wide improvements and refactoring.
    3. Added Workflows to automatically build binaries in Linux and Windows.
    4. Improved contribution-friendlyness by completing all community guidelines.

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
