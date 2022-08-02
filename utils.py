#!/usr/bin/env python3

"""
Hulk v3

Collection of Utitlity functions.
"""


from typing import Optional


def bordered(
    text: str,
    num_internal_colors: Optional[int] = 0
) -> str:
    """
    Returns a string with a border around the text.
    :param text: The text to be bordered.
    :type text: str
    :param num_internal_colors: The number of internal colors.
    :type num_internal_colors: Optional[int]
    :return: The bordered text.
    :rtype: str
    """
    sentences = trim_lines(text).splitlines()
    hor = max(len(line) for line in sentences) + 2
    pad = [
        '┌' + ('─' * 4)
        + ('─' * (
            hor - 5 - (num_internal_colors * 8)
        )) + '┐'
    ]
    pad.extend(
        '│ ' + (line + ' ' * hor)[
            :hor - 2
            + num_internal_colors
        ] + '│'
        for line in sentences
    )
    pad.append(
        '└' + ('─' * 4)
        + ('─' * (
            hor - 5 - (num_internal_colors * 8)
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
