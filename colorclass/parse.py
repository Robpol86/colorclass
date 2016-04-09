"""Parse color markup tags into ANSI escape sequences."""

import re

from colorclass.codes import ANSICodeMapping

RE_ANSI = re.compile(r'(\033\[([\d;]+)m)')
RE_COMBINE = re.compile(r'\033\[([\d;]+)m\033\[([\d;]+)m')
RE_NUMBER_SEARCH = re.compile(r'\033\[([\d;]+)m')
RE_SPLIT = re.compile(r'(\033\[[\d;]+m)')


def parse_input(tagged_string, disable_colors):
    """Perform the actual conversion of tags to ANSI escaped codes.

    Provides a version of the input without any colors for len() and other methods.

    :param str tagged_string: The input unicode value.
    :param bool disable_colors: Strip all colors in both outputs.

    :return: 2-item tuple. First item is the parsed output. Second item is a version of the input without any colors.
    :rtype: tuple
    """
    codes = ANSICodeMapping(tagged_string)
    output_colors = getattr(tagged_string, 'value_colors', tagged_string)

    # Convert: '{b}{red}' -> '\033[1m\033[31m'
    for tag, replacement in (('{' + k + '}', '' if v is None else '\033[%dm' % v) for k, v in codes.items()):
        output_colors = output_colors.replace(tag, replacement)

    # Strip colors.
    output_no_colors = RE_ANSI.sub('', output_colors)
    if disable_colors:
        return output_no_colors, output_no_colors

    # Combine: '\033[1m\033[31m' -> '\033[1;31m'
    while True:
        simplified = RE_COMBINE.sub(r'\033[\1;\2m', output_colors)
        if simplified == output_colors:
            break
        output_colors = simplified

    return output_colors, output_no_colors
