"""Convenience functions to enable/disable features."""

from colorclass.codes import ANSICodeMapping


def disable_all_colors():
    """Disable all colors. Strips any color tags or codes."""
    ANSICodeMapping.DISABLE_COLORS = True


def set_light_background():
    """Choose dark colors for all 'auto'-prefixed codes for readability on light backgrounds."""
    ANSICodeMapping.DISABLE_COLORS = False
    ANSICodeMapping.LIGHT_BACKGROUND = True


def set_dark_background():
    """Choose dark colors for all 'auto'-prefixed codes for readability on light backgrounds."""
    ANSICodeMapping.DISABLE_COLORS = False
    ANSICodeMapping.LIGHT_BACKGROUND = False
