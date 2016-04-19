"""Test objects in module."""

import subprocess
import sys

import pytest

from tests.conftest import IS_WINDOWS


def test_import_do_nothing():
    """Make sure importing __main__ doesn't print anything."""
    command = [sys.executable, '-c', "from colorclass.__main__ import TRUTHY; assert TRUTHY"]
    proc = subprocess.Popen(command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    output = proc.communicate()
    assert proc.poll() == 0
    assert not output[0]
    assert not output[1]


@pytest.mark.parametrize('colors', [True, False, None])
@pytest.mark.parametrize('light', [True, False, None])
def test(monkeypatch, colors, light):
    """Test package as a script.

    :param monkeypatch: pytest fixture.
    :param bool colors: Enable, disable, or don't touch colors using CLI args or env variables.
    :param bool light: Enable light, dark, or don't touch auto colors using CLI args or env variables.
    """
    command = [sys.executable, '-m', 'colorclass' if sys.version_info >= (2, 7) else 'colorclass.__main__']
    stdin = '{autored}Red{/autored} {red}Red{/red} {hired}Red{/hired}'.encode()

    # Set options.
    if colors is True:
        monkeypatch.setenv('COLOR_ENABLE', 'true')
    elif colors is False:
        monkeypatch.setenv('COLOR_DISABLE', 'true')
    if light is True:
        monkeypatch.setenv('COLOR_LIGHT', 'true')
    elif light is False:
        monkeypatch.setenv('COLOR_DARK', 'true')

    # Run.
    proc = subprocess.Popen(command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    output = proc.communicate(stdin)[0].decode()
    assert proc.poll() == 0
    assert 'Red' in output

    # Verify colors. Output is always stripped of all colors on Windows when piped to non-console (e.g. pytest).
    if not colors or IS_WINDOWS:
        assert '\033[' not in output
        assert 'Red Red Red' in output
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
