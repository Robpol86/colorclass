"""Test example scripts."""

import errno
import os
import sys
import time
from subprocess import PIPE, Popen, STDOUT

import pytest

try:
    import pty
except ImportError:
    pty = None


@pytest.mark.parametrize('python_m', [True, False])
@pytest.mark.parametrize('colors', [True, False, None])
@pytest.mark.parametrize('light', [True, False, None])
def test_piped(python_m, colors, light):
    """Test example.py or "python -m" with output piped to subprocess. Leads to colors disabled by default.

    :param bool python_m: Pipe to python -m colorclass if True, otherwise run example.py.
    :param bool colors: Enable, disable, or don't touch colors using CLI args or env variables.
    :param bool light: Enable light, dark, or don't touch auto colors using CLI args or env variables.
    """
    env = dict(os.environ, PYTHONIOENCODING='utf-8')
    if python_m:
        stdin = '{autored}Red{/autored} {red}Red{/red} {hired}Red{/hired}'.encode()
        command = [sys.executable, '-m', 'colorclass' if sys.version_info >= (2, 7) else 'colorclass.__main__']
    else:
        stdin = None
        script = os.path.join(os.path.dirname(__file__), '..', 'example.py')
        assert os.path.isfile(script)
        command = [sys.executable, script, 'print']
    if colors is True:
        env.update({'COLOR_ENABLE': 'true'}) if python_m else command.append('--colors')
    elif colors is False:
        env.update({'COLOR_DISABLE': 'true'}) if python_m else command.append('--no-colors')
    if light is True:
        env.update({'COLOR_LIGHT': 'true'}) if python_m else command.append('--light-bg')
    elif light is False:
        env.update({'COLOR_DARK': 'true'}) if python_m else command.append('--dark-bg')

    # Run.
    proc_handle = Popen(command, env=env, stderr=STDOUT, stdout=PIPE, stdin=PIPE if stdin else None)
    output = proc_handle.communicate(stdin)[0].decode()
    assert proc_handle.poll() == 0

    # Just check that it runs on Windows. output is always stripped of all colors on Windows.
    if os.name == 'nt':
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


@pytest.mark.skipif("os.name == 'nt'")
@pytest.mark.parametrize('colors', [True, False, None])
def test_pty(colors):
    """Test example.py through a pseudo TTY, having it think it's writing to a stream. Colors enabled by default.

    From http://stackoverflow.com/a/12471855/1198943.

    :param bool colors: Use --colors, --no-colors, or don't specify either (None).
    """
    env = dict(PYTHONIOENCODING='utf-8')
    if 'SystemRoot' in os.environ:
        env['SystemRoot'] = os.environ['SystemRoot']
    script = os.path.join(os.path.dirname(__file__), '..', 'example.py')
    command = [sys.executable, script, 'print']
    if colors is True:
        command.append('--colors')
    elif colors is False:
        command.append('--no-colors')

    # Run.
    master, slave = pty.openpty()
    proc_handle = Popen(command, env=env, stderr=STDOUT, stdout=slave, close_fds=True)
    os.close(slave)

    # Stream output.
    output = ''
    while True:
        try:
            data = os.read(master, 1024).decode()
        except OSError as exc:
            if exc.errno != errno.EIO:  # EIO means EOF on some systems.
                raise
            data = None
        if data:
            output += data
        elif proc_handle.poll() is None:
            time.sleep(0.01)
        else:
            break

    # Cleanup.
    os.close(master)

    # Verify exited 0.
    assert proc_handle.poll() == 0

    # Verify colors.
    if colors is False:
        assert '\033[' not in output
        return
    assert '\033[' in output
