"""Test example scripts."""

import os
import sys
from subprocess import PIPE, Popen, STDOUT

import pytest

from tests.conftest import IS_WINDOWS


@pytest.mark.parametrize('python_m', [True, False])
@pytest.mark.parametrize('colors', [True, False, None])
@pytest.mark.parametrize('light', [True, False, None])
def test_piped(monkeypatch, python_m, colors, light):
    """Test example.py or "python -m" with output piped to subprocess. Leads to colors disabled by default.

    :param monkeypatch: pytest fixture.
    :param bool python_m: Pipe to python -m colorclass if True, otherwise run example.py.
    :param bool colors: Enable, disable, or don't touch colors using CLI args or env variables.
    :param bool light: Enable light, dark, or don't touch auto colors using CLI args or env variables.
    """
    if python_m:
        stdin = '{autored}Red{/autored} {red}Red{/red} {hired}Red{/hired}'.encode()
        command = [sys.executable, '-m', 'colorclass' if sys.version_info >= (2, 7) else 'colorclass.__main__']
    else:
        stdin = None
        script = os.path.join(os.path.dirname(__file__), '..', 'example.py')
        assert os.path.isfile(script)
        command = [sys.executable, script, 'print']
    if colors is True:
        monkeypatch.setenv('COLOR_ENABLE', 'true') if python_m else command.append('--colors')
    elif colors is False:
        monkeypatch.setenv('COLOR_DISABLE', 'true') if python_m else command.append('--no-colors')
    if light is True:
        monkeypatch.setenv('COLOR_LIGHT', 'true') if python_m else command.append('--light-bg')
    elif light is False:
        monkeypatch.setenv('COLOR_DARK', 'true') if python_m else command.append('--dark-bg')

    # Run.
    proc = Popen(command, stderr=STDOUT, stdout=PIPE, stdin=PIPE if stdin else None)
    output = proc.communicate(stdin)[0].decode()
    assert proc.poll() == 0
    assert 'Red' in output

    # Just check that it runs on Windows. output is always stripped of all colors on Windows.
    if IS_WINDOWS:
        return

    # Verify colors.
    if not colors:
        assert '\033[' not in output
        return
    assert '\033[' in output

    # Verify light bg.
    count_dark_fg = output.count('\033[31mRed')
    count_light_fg = output.count('\033[91mRed')
    if light is True:
        assert count_dark_fg == 2
        assert count_light_fg == 1
    else:
        assert count_dark_fg == 1
        assert count_light_fg == 2


def test_import_do_nothing():
    """Make sure importing __main__ doesn't print anything."""
    command = [sys.executable, '-c', "from colorclass.__main__ import TRUTHY; assert TRUTHY"]

    proc_handle = Popen(command, stderr=STDOUT, stdout=PIPE)
    output = proc_handle.communicate()[0].decode()
    assert proc_handle.poll() == 0

    assert not output
