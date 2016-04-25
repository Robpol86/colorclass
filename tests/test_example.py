"""Test example script."""

import subprocess
import sys

import pytest

from tests.conftest import IS_WINDOWS, PROJECT_ROOT
from tests.screenshot import screenshot_until_match

STARTF_USESHOWWINDOW = getattr(subprocess, 'STARTF_USESHOWWINDOW', 1)
SW_MAXIMIZE = 3


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
    if not colors or IS_WINDOWS:
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
@pytest.mark.parametrize('colors', [True, False, None])
def test_windows_screenshot(colors):
    """Test script on Windows in a new console window. Take a screenshot to verify colors work.

    :param bool colors: Enable, disable, or omit color arguments (default has colors).
    """
    screenshot = PROJECT_ROOT.join('image.png')
    if screenshot.check():
        screenshot.remove()
    command = [sys.executable, str(PROJECT_ROOT.join('example.py')), 'print', '-w', str(screenshot)]

    # Set options.
    if colors is True:
        command.append('--colors')
    elif colors is False:
        command.append('--no-colors')

    # Run.
    c_flags = subprocess.CREATE_NEW_CONSOLE
    startup_info = subprocess.STARTUPINFO()
    startup_info.dwFlags = STARTF_USESHOWWINDOW
    startup_info.wShowWindow = SW_MAXIMIZE  # Start CMD window maximized.
    proc = subprocess.Popen(command, close_fds=True, creationflags=c_flags, startupinfo=startup_info)

    # Verify.
    if colors is False:
        candidates = PROJECT_ROOT.join('tests').listdir('sub_sans_*.bmp')
        expected_count = 27
    else:
        candidates = PROJECT_ROOT.join('tests').listdir('sub_light_fg_*.bmp')
        expected_count = 2
    assert candidates
    assert screenshot_until_match(str(screenshot), 5, [str(p) for p in candidates], expected_count)
    proc.communicate()
    assert proc.poll() == 0
