"""Parse color markup tags into ANSI escape sequences."""

import re

from colorclass.codes import ANSICodeMapping, BASE_CODES

RE_GROUP_SEARCH = re.compile(r'(?:\033\[[\d;]+m)+')
RE_NUMBER_SEARCH = re.compile(r'\033\[([\d;]+)m')
RE_SPLIT = re.compile(r'(\033\[[\d;]+m)')


def pad_input(incoming):
    """Avoid IndexError and KeyError by ignoring un-related fields.

    Example: '{0}{autored}' becomes '{{0}}{autored}'.

    :param str incoming: The input unicode value.

    :return: Padded unicode value.
    :rtype: str
    """
    incoming_expanded = incoming.replace('{', '{{').replace('}', '}}')
    for key in BASE_CODES:
        before, after = '{{%s}}' % key, '{%s}' % key
        if before in incoming_expanded:
            incoming_expanded = incoming_expanded.replace(before, after)
    return incoming_expanded


def parse_input(incoming):
    """Perform the actual conversion of tags to ANSI escaped codes.

    Provides a version of the input without any colors for len() and other methods.

    :param str incoming: The input unicode value.

    :return: 2-item tuple. First item is the parsed output. Second item is a version of the input without any colors.
    :rtype: tuple
    """
    codes_ = dict((k, v) for k, v in ANSICodeMapping(incoming).items() if '{%s}' % k in incoming)
    color_codes = dict((k, '' if ANSICodeMapping.DISABLE_COLORS else '\033[{0}m'.format(v)) for k, v in codes_.items())
    incoming_padded = pad_input(incoming)
    output_colors = incoming_padded.format(**color_codes)

    # Simplify: '{b}{red}' -> '\033[1m\033[31m' -> '\033[1;31m'
    groups = sorted(set(RE_GROUP_SEARCH.findall(output_colors)), key=len, reverse=True)  # Get codes, grouped adjacent.
    groups_simplified = [[x for n in RE_NUMBER_SEARCH.findall(i) for x in n.split(';')] for i in groups]
    groups_compiled = ['\033[{0}m'.format(';'.join(g)) for g in groups_simplified]  # Final codes.
    assert len(groups_compiled) == len(groups)  # For testing.
    output_colors_simplified = output_colors
    for i, group in enumerate(groups):
        output_colors_simplified = output_colors_simplified.replace(group, groups_compiled[i])
    output_no_colors = RE_SPLIT.sub('', output_colors_simplified)

    # Strip any remaining color codes.
    if ANSICodeMapping.DISABLE_COLORS:
        output_colors_simplified = RE_NUMBER_SEARCH.sub('', output_colors_simplified)

    return output_colors_simplified, output_no_colors
