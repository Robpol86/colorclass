from __future__ import print_function
import os

import pytest

from colorclass import Color, Windows

pytestmark = pytest.mark.skipif(os.name != 'nt')


def test():
    with Windows(auto_colors=True, reset_atexit=True):
        print(Color('{autored}Test{/autored}.'))
