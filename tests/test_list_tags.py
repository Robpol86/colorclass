"""Test list_tags()."""

from colorclass.codes import BASE_CODES, list_tags


def test_list_tags():
    """Test list_tags()."""
    actual = list_tags()
    assert ('red', '/red', 31, 39) in actual
    assert sorted(t for i in actual for t in i[:2] if t is not None) == sorted(BASE_CODES)
