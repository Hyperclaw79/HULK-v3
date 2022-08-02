#!/usr/bin/env python3

"""
Hulk v3

Collection of Utitlity functions.
"""

# pylint: disable=duplicate-code, no-member
from collections import deque
import contextlib
import logging
import os
import platform
import re
import socket
import sys
import time
from typing import List, Optional
import unicodedata

import chalk

if platform.system() == 'Windows':
    import pywintypes
    from win32 import win32file


def bordered(
    text: str,
    unicode_list: Optional[List[str]] = None,
    num_internal_colors: Optional[int] = 0
) -> str:
    """
    Returns a string with a border around the text.
    :param text: The text to be bordered.
    :type text: str
    :param unicode_list: The list of unicode characters in the string.
    :type unicode_list: Optional[List[str]]
    :param num_internal_colors: The number of internal colors.
    :type num_internal_colors: Optional[int]
    :return: The bordered text.
    :rtype: str
    """
    def unicode_padding(line_: str) -> int:
        pad_count = 0
        for char in unicode_list:
            if char in line_:
                pad_count += int(
                    unicodedata.east_asian_width(char) == 'N'
                ) * 2
        return pad_count

    sentences = trim_lines(text).splitlines()
    hor = max(len(line) for line in sentences) + 2
    pad = [
        '┌' + ('─' * 4)
        + ('┬' if len(unicode_list) > 0 else '')
        + ('─' * (
            hor + len(unicode_list) - 5 - (num_internal_colors * 8)
        )) + '┐'
    ]
    pad.extend(
        '│ ' + (line + ' ' * hor)[
            :hor - 1
            + num_internal_colors
            + unicode_padding(line)
        ] + '│'
        for line in sentences
    )
    pad.append(
        '└' + ('─' * 4)
        + ('┴' if len(unicode_list) > 0 else '')
        + ('─' * (
            hor + len(unicode_list) - 5 - (num_internal_colors * 8)
        )) + '┘'
    )
    return '\n'.join(pad)


def trim_lines(text: str) -> str:
    """
    Trims the lines of the text.
    :param text: The text to be trimmed.
    :type text: str
    :return: The trimmed text.
    :rtype: str
    """
    return '\n'.join(
        line.strip()
        for line in text.splitlines()
    )


def colorize_brackets(text: str) -> str:
    """
    Colorizes the text present inside brackets.
    :param text: The text to be colorized.
    :type text: str
    :return: The colorized text.
    :rtype: str
    """
    def get_color(match: re.Match):
        """
        Returns the color for the given match.
        :param match: The match to be colorized.
        :type match: re.Match
        :return: The color for the given match.
        :rtype: str
        """
        if match[1] == 'StatusCodes.NO_LUCK':
            color = 'red'
        elif match[1] == 'StatusCodes.PWNED':
            color = 'green'
        elif match[1] in {
            'StatusCodes.ANTI_DDOS',
            'StatusCodes.CONNECTIO_FAILURE'
        }:
            color = 'yellow'
        else:
            color = 'blue'
        return getattr(chalk, color)(f"<{match[1]}>")

    return re.sub(
        r'<([^>]*?)>',
        get_color,
        text
    )


class WinNamedPipeHandler(logging.StreamHandler):
    """
    Handler for sending data to Windows Named Pipes.

    :param pipe_name: The name of the pipe.
    :type pipe_name: Optional[str]
    :param wait_for_pipe: Whether to wait for the pipe to be created.
    :type wait_for_pipe: Optional[bool]
    """
    def __init__(
        self, *args,
        pipe_name: Optional[str] = "HULK",
        wait_for_pipe: Optional[bool] = False,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.pipe_name = pipe_name
        self.message_queue = deque()
        self.pipe = None
        if wait_for_pipe:
            while not self.pipe:
                self.connect()
                if not self.pipe:
                    time.sleep(0.1)
            sys.stdout.buffer.write(
                (
                    chalk.green(
                        bordered(
                            "✅ | Connected to GUI PIPE.",
                            unicode_list=['✅']
                        )
                    ) + '\n\n'
                ).encode()
            )
            sys.stdout.buffer.flush()

    def __enter__(self):
        """
        Context manager entry for Named Pipe.
        """
        return self

    def __exit__(self, *_, **__):
        """
        Context manager exit for Named Pipe.
        Closes the named pipe.
        """
        self.close_pipe()

    def connect(self):
        """
        Connects to the named pipe.
        """
        try:
            pipe_name = fr'\\.\pipe\{self.pipe_name}'
            self.pipe = win32file.CreateFile(
                pipe_name,
                win32file.GENERIC_WRITE,
                0,
                None,
                win32file.OPEN_EXISTING,
                (
                    win32file.FILE_ATTRIBUTE_NORMAL
                    | win32file.FILE_FLAG_NO_BUFFERING
                ),
                None
            )
        except pywintypes.error:
            self.pipe = None

    def send(self, data: str):
        """
        Sends data to the named pipe.
        :param data: The data to be sent.
        :type data: str
        """
        if self.pipe:
            self.flush()
            self._send(data)
        else:
            self.message_queue.append(data)
            self.connect()
            if self.pipe:
                self.flush()
                self._send(data)

    def flush(self):
        """
        Flushes the message queue.
        """
        while self.message_queue:
            self._send(self.message_queue.popleft())

    def emit(self, record: logging.LogRecord):
        """
        Emits the record to the named pipe.
        :param record: The record to be emitted.
        :type record: logging.LogRecord
        """
        self.send(record.message)

    def close_pipe(self):
        """
        Closes the named pipe.
        """
        with contextlib.suppress(pywintypes.error):
            win32file.CloseHandle(self.pipe)

    def _send(self, data: str):
        if self.pipe is None:
            return
        try:
            win32file.WriteFile(self.pipe, f"|{data}|".encode())
        except pywintypes.error:
            self.close_pipe()
            self.pipe = None


class UnixNamedPipeHandler(logging.StreamHandler):
    """
    Handler for sending data to Unix Named Pipes.

    :param pipe_name: The name of the pipe.
    :type pipe_name: Optional[str]
    :param wait_for_pipe: Whether to wait for the pipe to be created.
    :type wait_for_pipe: Optional[bool]
    """
    def __init__(
        self, *args,
        pipe_name: Optional[str] = "HULK",
        wait_for_pipe: Optional[bool] = False,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.pipe_name = pipe_name
        self.message_queue = deque()
        self.pipe: socket.socket = None
        if wait_for_pipe:
            while not self.pipe:
                self.connect()
                if not self.pipe:
                    time.sleep(0.1)
            sys.stdout.buffer.write(
                (
                    chalk.green(
                        bordered(
                            "✅ | Connected to GUI PIPE.",
                            unicode_list=['✅']
                        )
                    ) + '\n\n'
                ).encode()
            )
            sys.stdout.buffer.flush()

    def __enter__(self):
        """
        Context manager entry for Named Pipe.
        """
        return self

    def __exit__(self, *_, **__):
        """
        Context manager exit for Named Pipe.
        Closes the named pipe.
        """
        self.close_pipe()

    def connect(self):
        """
        Connects to the named pipe.
        """
        try:
            sock = socket.socket(
                socket.AF_UNIX,
                socket.SOCK_STREAM
            )
            sock.connect(f'/tmp/{self.pipe_name}')
            self.pipe = sock
        except OSError:
            sock.close()
            self.pipe = None

    def flush(self):
        """
        Flushes the message queue.
        """
        while self.message_queue:
            self.pipe.sendall(
                f"|{self.message_queue.popleft()}|".encode()
            )

    def send(self, data: str):
        """
        Sends data to the named pipe.
        :param data: The data to be sent.
        :type data: str
        """
        if self.pipe:
            self.flush()
            self.pipe.sendall(f"|{data}|".encode())
        else:
            self.message_queue.append(data)
            self.connect()
            if self.pipe:
                self.flush()
                os.write(self.pipe, f"|{data}|".encode())

    def emit(self, record: logging.LogRecord):
        """
        Emits the record to the named pipe.
        :param record: The record to be emitted.
        :type record: logging.LogRecord
        """
        self.send(record.message)

    def close_pipe(self):
        """
        Closes the named pipe.
        """
        if self.pipe is not None:
            with contextlib.suppress(OSError):
                self.pipe.close()


class StdoutHandler(logging.StreamHandler):
    """
    Logging handler for stdout.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(sys.stdout, *args, **kwargs)

    @staticmethod
    def info(text: str) -> str:
        """Returns a info message in a pretty format.

        :param text: The message to be printed.
        :type text: str
        :return: The message in a pretty format.
        :rtype: str
        """
        return chalk.blue(
            bordered(f"⚪ | {text}", unicode_list=['⚪'])
        )

    @staticmethod
    def warning(text: str):
        """Returns a warning message in a pretty format.

        :param text: The message to be printed.
        :type text: str
        :return: The warning in a pretty format.
        :rtype: str
        """
        return chalk.yellow(
            bordered(
                f"⚠️  | {text}",
                unicode_list=[unicodedata.lookup('WARNING SIGN')]
            )
        )

    @staticmethod
    def error(text: str) -> str:
        """Returns an error message in a pretty format.

        :param text: The message to be printed.
        :type text: str
        :return: The error in a pretty format.
        :rtype: str
        """
        return chalk.red(
            bordered(f"❌ | {text}", unicode_list=['❌'])
        )

    @staticmethod
    def success(text: str) -> str:
        """Returns a success message in a pretty format.

        :param text: The message to be printed.
        :type text: str
        :return: The success message in a pretty format.
        :rtype: str
        """
        return chalk.green(
            bordered(f"✅ | {text}", unicode_list=['✅'])
        )

    @staticmethod
    def incoming(text: str) -> str:
        """Returns an incoming message in a pretty format.

        :param text: The message to be printed.
        :type text: str
        :return: The incoming message in a pretty format.
        :rtype: str
        """
        modded_text = text
        matches = []
        if matches := re.findall(r'\[.*?\]', modded_text):
            modded_text = colorize_brackets(modded_text)
        return bordered(
            f"🔻 | {modded_text}",
            unicode_list=['🔻'],
            num_internal_colors=len(matches)
        )

    @staticmethod
    def outgoing(text: str) -> str:
        """Returns an outgoing message in a pretty format.

        :param text: The message to be printed.
        :type text: str
        :return: The outgoing message in a pretty format.
        :rtype: str
        """
        modded_text = text
        matches = []
        if matches := re.findall(r'<([^>]*?)>', modded_text):
            modded_text = colorize_brackets(modded_text)
        return bordered(
            f"🔼 | {modded_text}",
            unicode_list=['🔼'],
            num_internal_colors=len(matches)
        )

    def emit(self, record: logging.LogRecord):
        msg = self.format(record)
        if record.funcName == 'success':
            msg = self.success(msg)
        elif record.funcName == 'incoming':
            msg = self.incoming(msg)
        elif record.funcName == 'outgoing':
            msg = self.outgoing(msg)
        elif record.levelno == logging.INFO:
            msg = self.info(msg)
        elif record.levelno == logging.WARNING:
            msg = self.warning(msg)
        elif record.levelno == logging.ERROR:
            msg = self.error(msg)
        stream = self.stream
        # issue 35046: merged two stream.writes into one.
        stream.write(msg + self.terminator)
        self.flush()


class CustomLoggerClass(logging.Logger):
    """
    Extending the Logger class to add Succes, Incoming and Outgoing methods.
    """

    def success(self, text: str, *args, **kwargs):
        """Prints a success message in a pretty format.

        :param text: The message to be printed.
        :type text: str
        """
        self.info(text, *args, **kwargs)

    def incoming(self, text: str, *args, **kwargs):
        """Prints an incoming message in a pretty format.

        :param text: The message to be printed.
        :type text: str
        """
        self.info(text, *args, **kwargs)

    def outgoing(self, text: str, *args, **kwargs):
        """Prints an outgoing message in a pretty format.

        :param text: The message to be printed.
        :type text: str
        """
        self.info(text, *args, **kwargs)


logging.setLoggerClass(CustomLoggerClass)


LOGGER: CustomLoggerClass = logging.getLogger("Hulk_Server")
LOGGER.setLevel(logging.INFO)
LOGGER.addHandler(StdoutHandler())


if __name__ == '__main__':
    LOGGER.addHandler(WinNamedPipeHandler())
    inp = input('> ')
    for word in inp.split(', '):
        LOGGER.info(word)
