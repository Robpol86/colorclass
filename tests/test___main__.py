"""Test objects in module."""

import sys
from subprocess import PIPE, Popen, STDOUT


def test_import_do_nothing():
    """Make sure importing __main__ doesn't print anything."""
    command = [sys.executable, '-c', "from colorclass.__main__ import TRUTHY; assert TRUTHY"]
    proc = Popen(command, stderr=STDOUT, stdout=PIPE)
    output = proc.communicate()
    assert proc.poll() == 0
    assert not output[0]
    assert not output[1]
