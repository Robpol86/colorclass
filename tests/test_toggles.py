"""Test objects in module."""

from colorclass import toggles


def test_disable():
    """Test functions."""
    toggles.disable_all_colors()
    assert not toggles.is_enabled()
    toggles.enable_all_colors()
    assert toggles.is_enabled()
    toggles.disable_all_colors()
    assert not toggles.is_enabled()
    toggles.enable_all_colors()
    assert toggles.is_enabled()


def test_light_bg():
    """Test functions."""
    toggles.set_dark_background()
    assert not toggles.is_light()
    toggles.set_light_background()
    assert toggles.is_enabled()
    toggles.set_dark_background()
    assert not toggles.is_light()
    toggles.set_light_background()
    assert toggles.is_enabled()
