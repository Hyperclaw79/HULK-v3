<!--
    Title: Hulk v3
    Description: Asynchronous HTTP Botnet for Distributed Denial of Service (DDoS)
    Author: Hyperclaw79
    Url: https://github.com/Hyperclaw79/HULK-v3
    Image: https://raw.githubusercontent.com/Hyperclaw79/Hulk-v3/async/assets/Hulk.png
-->

<meta name="title" content="Hulk v3" />
<meta name="description" content="Asynchronous HTTP Botnet for Distributed Denial of Service (DDoS)" />
<meta name="author" content="Hyperclaw79" />
<meta name="url" content="https://github.com/Hyperclaw79/HULK-v3" />
<meta name="image" content="https://raw.githubusercontent.com/Hyperclaw79/Hulk-v3/async/assets/Hulk.png" />
<meta name="keywords" content="async,asynchronous,ddos,ddos-attack,ddos-script,electron,gui,http,https,hulk,named-pipes,nextron,nodejs,python,python3,typescript,websockets" />
<meta name="og:title" content="Hulk v3" />
<meta name="og:description" content="Asynchronous HTTP Botnet for Distributed Denial of Service (DDoS)" />
<meta name="og:author" content="Hyperclaw79" />
<meta name="og:url" content="https://github.com/Hyperclaw79/HULK-v3" />
<meta name="og:image" content="https://raw.githubusercontent.com/Hyperclaw79/Hulk-v3/async/assets/Hulk.png" />
<meta name="og:keywords" content="async,asynchronous,ddos,ddos-attack,ddos-script,electron,gui,http,https,hulk,named-pipes,nextron,nodejs,python,python3,typescript,websockets" />


![Hulk_Banner](/assets/Hulk_banner.png)

![Python Version](https://img.shields.io/badge/python-3.8+-blue?style=for-the-badge)
![License](https://img.shields.io/badge/License-GNU-green?style=for-the-badge)
![Build and Package](https://img.shields.io/github/workflow/status/Hyperclaw79/HULK-v3/Build%20and%20Package/async?style=for-the-badge)
![Codacy branch grade](https://img.shields.io/codacy/grade/c4f7560e8231423691d819129c7b3afa/async?style=for-the-badge)


## ⚠️ Disclaimer

| **Hulk is meant for educational and research purposes only.<br />Any malicious usage of this tool is prohibited.<br />The authors must not to be held responsible for any consequences from the usage of this tool.** |
| :--- |


## Introducing **HULK-v3** :robot:

| :information_source: | **Hulk** is a *Distributed Denial of Service* tool that can put heavy load on HTTPS servers, in order to bring them to their knees, by exhausting the resource pool. |
| :---: | :--- |

### Check out Hulk in Action

**GUI :desktop_computer:**
![Hulk_demo](/assets/Hulk_demo.gif)

**Server :computer:**
![Hulk_server](/assets/Hulk_server.png)
**Client/Bot :space_invader:**
![Hulk_client](/assets/Hulk_client.png)

:green_circle: To get started, expand the sections below to read about them.


## Changelog :page_with_curl:
You can refer the Changelog [here](/CHANGELOG.md).


<details markdown=1><summary markdown="span"><h2>Usage :book:</h2></summary>

1.  Run `pip install -r requirements_(linux/win).txt` before starting this script.
    > Ex: On Windows: `pip install -r requirements_win.txt`
    > Ex: On Linux: `pip install -r requirements_linux.txt`

2.  Launch the `hulk_launcher.py server` with the target website as arg.
    > Ex: `python hulk_launcher.py server https://testdummysite.com`
    >
    > Append `--persistent False` to kill the botnet after a succesfull DDoS.
    >
    > Append `--gui` if you are running the GUI in parallel.

3.  Launch the `hulk_launcher.py client` to spawn multiple processes of hulk - one per CPU Core.
    > Ex: `python hulk_launcher.py client [localhost]`
    >
    > If the server is running remotely, replace localhost with the server's IP.

4. To run the GUI, you need to:
    * Install `NodeJS`, change to `gui` directory and use `npm install`.
    * Launch the GUI with `npm run dev`.

5.  Sit back and sip your coffee while the carnage unleashes! 😈

*(P.S. Do not run the binaries (except `hulk_gui`) directly, use them from command line like shown above without using `python`.)*

</details>


<details markdown=1><summary markdown="span"><h2>Syntax Help :scroll:</h2></summary>

### Server :computer:
```py
usage: hulk_launcher.py server [-h] [-p PORT] [-m MAX_MISSILES] [--persistent] [--gui] target

The Hulk Server Launcher

positional arguments:
target                the target url.

options:
-h, --help            show this help message
-p PORT, --port PORT  the Port to bind the server to.
-m MAX_MISSILES, --max_missiles MAX_MISSILES
                        the maximum number of missiles to connect to.
--persistent          keep attacking even after target goes down.
--gui                 run on the GUI mode.
```

### Client :space_invader:
```py
usage: hulk_launcher.py client [-h] [-r ROOT_IP] [-p ROOT_PORT] [-n NUM_PROCESSES] [-s]

The Hulk Bot Launcher

options:
-h, --help            show this help message
-r ROOT_IP, --root_ip ROOT_IP
                        IPv4 Address where Hulk Server is running.
-p ROOT_PORT, --root_port ROOT_PORT
                        Port where Hulk Server is running.
-n NUM_PROCESSES, --num_processes NUM_PROCESSES
                        Number of Processes to launch.
-s, --stealth         Stealth mode.
```

</details>


<details markdown=1><summary markdown="span"><h2>Architecture :gear:</h2></summary>

| :warning: The intention of Hulk is to demonstrate the damage that a DDoS attack can do to a server if unprotected. |
| :--- |
| :bulb: Please go through the code for full details. I'm keeping it well documented and request the contributors to do so too. |

Hulk consists of 2 major and 1 optional components:
 - Server
 - Client
 - [Gui]

<p align="center">

 ![Hulk_architecture](/assets/Hulk_architecture.svg)

</p>

**Client :space_invader:**

> The core part of Hulk is the `Hulk client` aka `Hulk.py`. \
This client\bot launches a barrage of `asynchronous HTTP requests` to the target server. \
These incoming requests, put a burden on the target and makes it slow to respond. \
With the launcher script, we can launch multiple instances of Hulk using `multi-threading`. \
The target will be hit with so many requests that it will ultimately break into a `500 error`. \
Usually, the client completes 500 attacks and sends back the list of status messages. \
In case of special events, the client will immediately send an Interrupt message to the server. \
Example Special Events: *Successful DDoS*, *404 Target Not Found*, etc.

**Server :computer:**

> Hulk was originally a single instanced DoS script. However, it has been modified to be run as multiple instances. \
The cluster of many such instances is called a `botnet`. And this botnet can be controlled and monitored by the `Server`. \
The `Server` and `Client` communicate with each other through TCP `WebSockets`.
Based on the settings, this is usally a persistent bidirectional channel. \
In case the server receives `Interrupts` from a client, it will send out a broadcast message to all the clients, asking them to stop the attacks. \
The clients go to Standby mode and await further instructions from the server.
>
> The server can also send information to the GUI to keep a track of the botnet. \
This information is sent via Unix\Windows `Named Pipes` for low latency `IPC`.

**GUI :desktop_computer:**

> The GUI is a `NextJS` web application that is used to monitor the botnet via Named Pipes. \
When run as a binary, GUI makes use of `Electron` which exposes the information directly to the Frontend. \
When run as a Node process, a node server listens to the Named Pipe and passes on the information to a HTTP Streaming API. \
Then the frontend will pick it up from the API using `EventSource`.

</details>


<details markdown=1><summary markdown="span"><h2>Acknowledgements :busts_in_silhouette:</h2></summary>

### Authors :writing_hand:
|         Name       | Version |
|--------------------|---------|
| **Hyperclaw79**    |   2.0+  |
| **Barry Shteiman** |   1.0   |

### Contributors :handshake:
Thanks for contributing to the repo. Follow the [Contribution Guide](/.github/CONTRIBUTING.md) and open a PR.

| Contributor | Contribution |
| :--: | :--: |
| [Nexuzzzz](https://github.com/Nexuzzzz) | Fixed typo in the code |

</details>


<details markdown=1><summary markdown="span"><h2>License :page_facing_up:</h2></summary>

HULK v3 is a Python 3 compatible Asynchronous Distributed Denial of Service Script.\
[Original script](http://www.sectorix.com/2012/05/17/hulk-web-server-dos-tool/) was created by Barry Shteiman.
You can use that one if you have Python 2.

Using a [GNU license](/LICENSE) cause there was no mention about any license used by Barry.
Feel free to modify and share it, but leave some credits to us both and don't hold us liable.

</details>
