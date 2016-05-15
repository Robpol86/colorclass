"""Test objects in module."""

import errno
import os
import subprocess
import sys
import time

import pytest

from colorclass.codes import ANSICodeMapping, BASE_CODES, list_tags
from colorclass.windows import IS_WINDOWS


def test_ansi_code_mapping_whitelist():
    """Test whitelist enforcement."""
    auto_codes = ANSICodeMapping('{green}{bgred}Test{/all}')

    # Test __getitem__.
    with pytest.raises(KeyError):
        assert not auto_codes['red']
    assert auto_codes['green'] == 32

    # Test iter and len.
    assert sorted(auto_codes) == ['/all', 'bgred', 'green']
    assert len(auto_codes) == 3


@pytest.mark.parametrize('toggle', ['light', 'dark', 'none'])
def test_auto_toggles(toggle):
    """Test auto colors and ANSICodeMapping class toggles.

    :param str toggle: Toggle method to call.
    """
    # Toggle.
    if toggle == 'light':
        ANSICodeMapping.enable_all_colors()
        ANSICodeMapping.set_light_background()
        assert ANSICodeMapping.DISABLE_COLORS is False
        assert ANSICodeMapping.LIGHT_BACKGROUND is True
    elif toggle == 'dark':
        ANSICodeMapping.enable_all_colors()
        ANSICodeMapping.set_dark_background()
        assert ANSICodeMapping.DISABLE_COLORS is False
        assert ANSICodeMapping.LIGHT_BACKGROUND is False
    else:
        ANSICodeMapping.disable_all_colors()
        assert ANSICodeMapping.DISABLE_COLORS is True
        assert ANSICodeMapping.LIGHT_BACKGROUND is False

    # Test iter and len.
    auto_codes = ANSICodeMapping('}{'.join([''] + list(BASE_CODES) + ['']))
    count = 0
    for k, v in auto_codes.items():
        count += 1
        assert str(k) == k
        assert v is None or int(v) == v
    assert len(auto_codes) == count

    # Test foreground properties.
    key_fg = '{autoblack}{autored}{autogreen}{autoyellow}{autoblue}{automagenta}{autocyan}{autowhite}'
    actual = key_fg.format(**auto_codes)
    if toggle == 'light':
        assert actual == '3031323334353637'
    elif toggle == 'dark':
        assert actual == '9091929394959697'
    else:
        assert actual == 'NoneNoneNoneNoneNoneNoneNoneNone'

    # Test background properties.
    key_fg = '{autobgblack}{autobgred}{autobggreen}{autobgyellow}{autobgblue}{autobgmagenta}{autobgcyan}{autobgwhite}'
    actual = key_fg.format(**auto_codes)
    if toggle == 'light':
        assert actual == '4041424344454647'
    elif toggle == 'dark':
        assert actual == '100101102103104105106107'
    else:
        assert actual == 'NoneNoneNoneNoneNoneNoneNoneNone'


def test_list_tags():
    """Test list_tags()."""
    actual = list_tags()
    assert ('red', '/red', 31, 39) in actual
    assert sorted(t for i in actual for t in i[:2] if t is not None) == sorted(BASE_CODES)


@pytest.mark.parametrize('tty', [False, True])
def test_disable_colors_piped(tty):
    """Verify colors enabled by default when piped to TTY and disabled when not.

    :param bool tty: Pipe to TTY/terminal?
    """
    assert_statement = 'assert __import__("colorclass").codes.ANSICodeMapping.disable_if_no_tty() is {bool}'
    command_colors_enabled = [sys.executable, '-c', assert_statement.format(bool='False')]
    command_colors_disabled = [sys.executable, '-c', assert_statement.format(bool='True')]

    # Run piped to this pytest process.
    if not tty:  # Outputs piped to non-terminal/non-tty. Colors disabled by default.
        proc = subprocess.Popen(command_colors_disabled, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        output = proc.communicate()
        assert not output[0]
        assert not output[1]
        assert proc.poll() == 0
        return

    # Run through a new console window (Windows).
    if IS_WINDOWS:
        c_flags = subprocess.CREATE_NEW_CONSOLE
        proc = subprocess.Popen(command_colors_enabled, close_fds=True, creationflags=c_flags)
        proc.communicate()  # Pipes directed towards new console window. Not worth doing screenshot image processing.
        assert proc.poll() == 0
        return

    # Run through pseudo tty (Linux/OSX).
    master, slave = __import__('pty').openpty()
    proc = subprocess.Popen(command_colors_enabled, stderr=subprocess.STDOUT, stdout=slave, close_fds=True)
    os.close(slave)

    # Read output.
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
        elif proc.poll() is None:
            time.sleep(0.01)
        else:
            break
    os.close(master)
    assert not output
    assert proc.poll() == 0
