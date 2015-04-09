"""Test list_tags()."""

from colorclass import _AutoCodes, list_tags


def test_main():
    """Test list_tags()."""
    codes = _AutoCodes()
    tags = list_tags()

    for group in tags:
        if group[0]:
            assert group[2] == codes[group[0]]
        assert group[3] == codes[group[1]]
