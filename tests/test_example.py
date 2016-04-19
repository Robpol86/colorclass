"""Test example script."""

import subprocess
import sys

import pytest

from tests.conftest import IS_WINDOWS, PROJECT_ROOT


@pytest.mark.parametrize('colors', [True, False, None])
@pytest.mark.parametrize('light', [True, False, None])
def test_piped(colors, light):
    """Test script with output piped to non-tty (this pytest process).

    :param bool colors: Enable, disable, or omit color arguments (default is no colors due to no tty).
    :param bool light: Enable light, dark, or omit light/dark arguments.
    """
    command = [sys.executable, str(PROJECT_ROOT.join('example.py')), 'print']

    # Set options.
    if colors is True:
        command.append('--colors')
    elif colors is False:
        command.append('--no-colors')
    if light is True:
        command.append('--light-bg')
    elif light is False:
        command.append('--dark-bg')

    # Run.
    proc = subprocess.Popen(command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    output = proc.communicate()[0].decode()
    assert proc.poll() == 0
    assert 'Autocolors for all backgrounds' in output
    assert 'Red' in output

    # Verify colors. Output is always stripped of all colors on Windows when piped to non-console (e.g. pytest).
    if not colors or IS_WINDOWS:
        assert '\033[' not in output
        assert 'Black Red Green Yellow Blue Magenta Cyan White' in output
        return
    assert '\033[' in output

    # Verify light bg.
    count_dark_fg = output.count('\033[31mRed')
    count_light_fg = output.count('\033[91mRed')
    if light:
        assert count_dark_fg == 2
        assert count_light_fg == 1
    else:
        assert count_dark_fg == 1
        assert count_light_fg == 2
