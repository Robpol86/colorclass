"""Test example script."""

import subprocess
import sys

import pytest

from colorclass.windows import IS_WINDOWS
from tests.conftest import PROJECT_ROOT
from tests.screenshot import RunNewConsole, screenshot_until_match


@pytest.mark.parametrize('colors', [True, False, None])
@pytest.mark.parametrize('light_bg', [True, False, None])
def test_piped(colors, light_bg):
    """Test script with output piped to non-tty (this pytest process).

    :param bool colors: Enable, disable, or omit color arguments (default is no colors due to no tty).
    :param bool light_bg: Enable light, dark, or omit light/dark arguments.
    """
    command = [sys.executable, str(PROJECT_ROOT.join('example.py')), 'print']

    # Set options.
    if colors is True:
        command.append('--colors')
    elif colors is False:
        command.append('--no-colors')
    if light_bg is True:
        command.append('--light-bg')
    elif light_bg is False:
        command.append('--dark-bg')

    # Run.
    proc = subprocess.Popen(command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    output = proc.communicate()[0].decode()
    assert proc.poll() == 0
    assert 'Autocolors for all backgrounds' in output
    assert 'Red' in output

    # Verify colors. Output is always stripped of all colors on Windows when piped to non-console (e.g. pytest).
    if colors is False or IS_WINDOWS:
        assert '\033[' not in output
        assert 'Black Red Green Yellow Blue Magenta Cyan White' in output
        return
    assert '\033[' in output

    # Verify light bg.
    count_dark_fg = output.count('\033[31mRed')
    count_light_fg = output.count('\033[91mRed')
    if light_bg:
        assert count_dark_fg == 2
        assert count_light_fg == 1
    else:
        assert count_dark_fg == 1
        assert count_light_fg == 2


@pytest.mark.skipif(str(not IS_WINDOWS))
@pytest.mark.parametrize('colors,light_bg', [
    (True, False),
    (True, True),
    (False, False),
    (None, False),
])
def test_windows_screenshot(colors, light_bg):
    """Test script on Windows in a new console window. Take a screenshot to verify colors work.

    :param bool colors: Enable, disable, or omit color arguments (default has colors).
    :param bool light_bg: Create console with white background color.
    """
    screenshot = PROJECT_ROOT.join('test_example_test_windows_screenshot.png')
    if screenshot.check():
        screenshot.remove()
    command = [sys.executable, str(PROJECT_ROOT.join('example.py')), 'print', '-w', str(screenshot)]

    # Set options.
    if colors is True:
        command.append('--colors')
    elif colors is False:
        command.append('--no-colors')

    # Setup expected.
    if colors is False:
        candidates = [str(p) for p in PROJECT_ROOT.join('tests').listdir('sub_red_sans_*.bmp')]
        expected_count = 27
    elif light_bg:
        candidates = [str(p) for p in PROJECT_ROOT.join('tests').listdir('sub_red_dark_fg_*.bmp')]
        expected_count = 2
    else:
        candidates = [str(p) for p in PROJECT_ROOT.join('tests').listdir('sub_red_light_fg_*.bmp')]
        expected_count = 2
    assert candidates

    # Run.
    with RunNewConsole(command, maximized=True, white_bg=light_bg) as gen:
        screenshot_until_match(str(screenshot), 15, candidates, expected_count, gen)
