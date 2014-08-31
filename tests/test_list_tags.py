from colorclass import _AutoCodes, list_tags


def test_main():
    codes = _AutoCodes()
    tags = list_tags()

    for group in tags:
        assert group[2] == codes[group[0]]
        assert group[3] == codes[group[1]]
