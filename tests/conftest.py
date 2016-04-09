"""Configure tests."""

import pytest

from colorclass.codes import ANSICodeMapping


@pytest.fixture(autouse=True)
def set_defaults(monkeypatch):
    """Set ANSICodeMapping defaults before each test.

    :param monkeypatch: pytest fixture.
    """
    monkeypatch.setattr(ANSICodeMapping, 'DISABLE_COLORS', False)
    monkeypatch.setattr(ANSICodeMapping, 'LIGHT_BACKGROUND', False)
