#!/usr/bin/env python3

"""
Hulk v3

Script to launch multiple instances of Hulk.
"""

import argparse
from copy import copy
import logging
import os
import platform
import sys
from typing import Tuple

from utils import bordered


LOGGER = logging.getLogger("Hulk_Launcher")
LOGGER.setLevel(logging.INFO)
LOGGER.addHandler(logging.StreamHandler(sys.stdout))


def get_live_message(title: str, args: argparse.Namespace):
    """Get a visually appealing status message.

    :param title: The title.
    :type title: str
    :param args: The arguments.
    :type args: argparse.Namespace
    :return: The live message.
    :rtype: str
    """
    # pylint: disable=import-outside-toplevel
    import chalk

    title_msg = chalk.green(title)
    arg_msg = '\n'.join(
        f'{name.title()}: {chalk.blue(value)}'
        for name, value in vars(args).items()
    )
    message = f'{title_msg}\n{arg_msg}'
    return bordered(message, num_internal_colors=1)


def launch_server(args: argparse.Namespace):
    """
    Launch the Hulk server.
    :param args: The arguments.
    :type args: argparse.Namespace
    """
    # pylint: disable=import-outside-toplevel, duplicate-code
    from server.hulk_server import HulkServer

    msg_args = copy(args)
    msg_args.__dict__.pop('target')
    LOGGER.info(get_live_message("Hulk Server is Live!", msg_args))
    if args.gui:
        if platform.system() == 'Windows':
            from server.logger import WinNamedPipeHandler, UnixNamedPipeHandler

            logging.getLogger('Hulk_Server').addHandler(
                WinNamedPipeHandler(wait_for_pipe=True)
            )
        else:
            from server.logger import UnixNamedPipeHandler

            logging.getLogger('Hulk_Server').addHandler(
                UnixNamedPipeHandler(wait_for_pipe=True)
            )
    server = HulkServer(
        args.target, args.port,
        args.persistent,
        args.max_missiles
    )
    server.launch()


def launch_client(args: argparse.Namespace):
    """
    Launches the Hulk client.
    :param args: The arguments.
    :type args: argparse.Namespace
    """
    # pylint: disable=import-outside-toplevel
    import asyncio
    from threading import Thread

    from client.hulk import Comms

    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(
            asyncio.WindowsSelectorEventLoopPolicy()
        )

    # Parse the arguments.
    root_ip = args.root_ip
    root_port = args.root_port
    num_processes = args.num_processes
    if args.stealth:
        logging.getLogger('Hulk_Client').setLevel(logging.ERROR)
    LOGGER.info(get_live_message("Launching Hulk v3", args))

    threads = [
        Thread(
            target=lambda: asyncio.new_event_loop().run_until_complete(
                Comms(root_ip, root_port).monitor()
            ),
        ) for _ in range(num_processes)
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


def create_parser() -> Tuple[
    argparse.ArgumentParser,
    argparse._SubParsersAction
]:
    """
    Creates the Multicommand Argument Parser.
    :return: The Multicommand Argument Parser and Subparsers.
    :rtype: Tuple[argparse.ArgumentParser, argparse.ArgumentParser]
    """

    class CustomParser(argparse.ArgumentParser):
        """
        Custom parser to format error string.
        """
        def error(self, message):
            if "{Client / Server}" in message:
                LOGGER.info(
                    "Either 'client' or 'server' must be specified "
                    "as the first argument."
                )
                sys.exit(1)
            super().error(message)

    class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter):
        """
        Custom formatter for the help text.
        """
        def _get_help_string(self, action):
            help_text = super()._get_help_string(action)
            if action.dest == 'num_processes':
                return help_text.replace(
                    '(default: %(default)s)',
                    '(default: No. of Cores. [%(default)s])'
                )
            return help_text

    parser = CustomParser(
        description="Hulk Launcher",
        formatter_class=CustomFormatter
    )
    subparsers = parser.add_subparsers(
        dest="mode",
        required=True,
        metavar="{Client / Server}",
    )
    return parser, subparsers


def add_client_parser(subparsers: argparse._SubParsersAction):
    """
    Adds the Client Parser.
    :param subparsers: The Subparsers.
    :type subparsers: argparse._SubParsersAction
    """
    # pylint: disable=import-outside-toplevel
    from client.hulk import modify_parser

    client_parser = subparsers.add_parser(
        "client",
        description="The Hulk Bot Launcher",
        help="Launches multiple Hulk Clients.\n"
        "(Check out [hulk_launcher.py client -h])"
    )
    modify_parser(client_parser)
    client_parser.add_argument(
        '-n', '--num_processes',
        help='Number of processes to launch.',
        default=os.cpu_count(),
        type=int,
    )


def add_server_parser(subparsers: argparse._SubParsersAction):
    """
    Adds the Server Parser.
    :param subparsers: The Subparsers.
    :type subparsers: argparse._SubParsersAction
    """
    # pylint: disable=import-outside-toplevel
    from server.hulk_server import modify_parser

    server_parser = subparsers.add_parser(
        "server",
        description="The Hulk Server Launcher",
        help="Launches the Hulk Server.\n"
        "(Check out [hulk_launcher.py server -h])"
    )
    modify_parser(server_parser)


if __name__ == '__main__':
    created_parser, created_subparsers = create_parser()
    add_client_parser(created_subparsers)
    add_server_parser(created_subparsers)

    parsed_args = created_parser.parse_args()
    launchables = {
        'server': launch_server,
        'client': launch_client
    }
    launchables[parsed_args.mode](parsed_args)
