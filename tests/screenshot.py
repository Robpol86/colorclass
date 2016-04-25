"""Take screenshots and search for subimages in images."""

import time

try:
    from itertools import izip
except ImportError:
    izip = zip  # Py3


def iter_rows(pil_image):
    """Yield tuple of pixels for each row in the image.

    itertools.izip in Python 2.x and zip in Python 3.x are writen in C. Much faster than anything else I've found
    written in pure Python.

    From:
    http://stackoverflow.com/questions/1624883/alternative-way-to-split-a-list-into-groups-of-n/1625023#1625023

    :param PIL.Image.Image pil_image: Image to read from.

    :return: Yields rows.
    :rtype: tuple
    """
    iterator = izip(*(iter(pil_image.getdata()),) * pil_image.width)
    for row in iterator:
        yield row


def get_most_interesting_row(pil_image):
    """Look for a row in the image that has the most unique pixels.

    :param PIL.Image.Image pil_image: Image to read from.

    :return: Row (tuple of pixel tuples), row as a set, first pixel tuple, y offset from top.
    :rtype: tuple
    """
    final = (None, set(), None, None)  # row, row_set, first_pixel, y_pos
    for y_pos, row in enumerate(iter_rows(pil_image)):
        row_set = set(row)
        if len(row_set) > len(final[1]):
            final = row, row_set, row[0], y_pos
        if len(row_set) == pil_image.width:
            break  # Can't get bigger.
    return final


def count_subimages(screenshot, subimg):
    """Check how often subimg appears in the screenshot image.

    :param PIL.Image.Image screenshot: Screen shot to search through.
    :param PIL.Image.Image subimg: Subimage to search for.

    :return: Number of times subimg appears in the screenshot.
    :rtype: int
    """
    # Get row to search for.
    si_pixels = list(subimg.getdata())  # Load entire subimg into memory.
    si_width = subimg.width
    si_height = subimg.height
    si_row, si_row_set, si_pixel, si_y = get_most_interesting_row(subimg)
    occurrences = 0

    # Look for subimg row in screenshot, then crop and compare pixel arrays.
    for y_pos, row in enumerate(iter_rows(screenshot)):
        if si_row_set - set(row):
            continue  # Some pixels not found.
        for x_pos in range(screenshot.width - si_width + 1):
            if row[x_pos] != si_pixel:
                continue  # First pixel does not match.
            if row[x_pos:x_pos + si_width] != si_row:
                continue  # Row does not match.
            # Found match for interesting row of subimg in screenshot.
            y_corrected = y_pos - si_y
            with screenshot.crop((x_pos, y_corrected, x_pos + si_width, y_corrected + si_height)) as cropped:
                if list(cropped.getdata()) == si_pixels:
                    occurrences += 1

    return occurrences


def screenshot_until_match(save_to, timeout, subimg_candidates, expected_count):
    """Take screenshots until one of the 'done' subimages is found. Image is saved when subimage found or at timeout.

    If you get ImportError run "pip install pillow". Only OSX and Windows is supported.

    :param str save_to: Save screenshot to this PNG file path when expected count found or timeout.
    :param int timeout: Give up after these many seconds.
    :param iter subimg_candidates: Subimage paths to look for. List of strings.
    :param int expected_count: Keep trying until any of subimg_candidates is found this many times.

    :return: If one of the 'done' subimages was found somewhere in the screenshot.
    :rtype: bool
    """
    from PIL import Image, ImageGrab
    assert save_to.endswith('.png')
    stop_after = time.time() + timeout

    # Take screenshots until subimage is found.
    while True:
        with ImageGrab.grab() as rgba:
            with rgba.convert(mode='RGB') as screenshot:
                for subimg_path in subimg_candidates:
                    with Image.open(subimg_path) as rgba_s:
                        with rgba_s.convert(mode='RGB') as subimg:
                            assert subimg.width < 128
                            assert subimg.height < 128
                            if count_subimages(screenshot, subimg) == expected_count:
                                screenshot.save(save_to)
                                return True
                if time.time() > stop_after:
                    screenshot.save(save_to)
                    return False
        time.sleep(0.5)
