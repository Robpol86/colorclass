"""Test example scripts."""

import os
import subprocess
import sys


def test_example():
    """Test example.py."""
    path = os.path.join(os.path.dirname(__file__), '..', 'example.py')
    env = dict(PYTHONIOENCODING='utf-8')
    if 'SystemRoot' in os.environ:
        env['SystemRoot'] = os.environ['SystemRoot']
    cmd = [sys.executable, path, 'print']
    assert 0 == subprocess.call(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
