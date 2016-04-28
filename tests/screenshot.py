"""Take screenshots and search for subimages in images."""

import ctypes
import os
import random
import struct
import subprocess
import time

try:
    from itertools import izip
except ImportError:
    izip = zip  # Py3

from colorclass.windows import WINDOWS_CODES
from tests.conftest import PROJECT_ROOT

HANDLE_FLAG_INHERIT = 0x00000001
STARTF_USEFILLATTRIBUTE = 0x00000010
STARTF_USESHOWWINDOW = getattr(subprocess, 'STARTF_USESHOWWINDOW', 1)
STARTF_USESTDHANDLES = getattr(subprocess, 'STARTF_USESTDHANDLES', 256)
STILL_ACTIVE = 259
SW_MAXIMIZE = 3


class StartupInfo(ctypes.Structure):
    """STARTUPINFO structure."""

    _fields_ = [
        ('cb', ctypes.c_ulong),
        ('lpReserved', ctypes.c_char_p),
        ('lpDesktop', ctypes.c_char_p),
        ('lpTitle', ctypes.c_char_p),
        ('dwX', ctypes.c_ulong),
        ('dwY', ctypes.c_ulong),
        ('dwXSize', ctypes.c_ulong),
        ('dwYSize', ctypes.c_ulong),
        ('dwXCountChars', ctypes.c_ulong),
        ('dwYCountChars', ctypes.c_ulong),
        ('dwFillAttribute', ctypes.c_ulong),
        ('dwFlags', ctypes.c_ulong),
        ('wShowWindow', ctypes.c_ushort),
        ('cbReserved2', ctypes.c_ushort),
        ('lpReserved2', ctypes.c_char_p),
        ('hStdInput', ctypes.c_ulong),
        ('hStdOutput', ctypes.c_ulong),
        ('hStdError', ctypes.c_ulong),
    ]

    def __init__(self, new_max_window=False, title=None, white_bg=False):
        """Constructor.

        :param bool new_max_window: Start process in new console window, maximized.
        :param bool white_bg: New console window will be black text on white background.
        :param bytes title: Set new window title to this instead of exe path.
        """
        super(StartupInfo, self).__init__()
        self.cb = ctypes.sizeof(self)
        if new_max_window:
            self.dwFlags |= STARTF_USESHOWWINDOW
            self.wShowWindow = SW_MAXIMIZE
        if title:
            self.lpTitle = ctypes.c_char_p(title)
        if white_bg:
            self.dwFlags |= STARTF_USEFILLATTRIBUTE
            self.dwFillAttribute = WINDOWS_CODES['hibgwhite'] | WINDOWS_CODES['black']


class ProcessInfo(ctypes.Structure):
    """PROCESS_INFORMATION structure."""

    _fields_ = [
        ('hProcess', ctypes.c_void_p),
        ('hThread', ctypes.c_void_p),
        ('dwProcessId', ctypes.c_ulong),
        ('dwThreadId', ctypes.c_ulong),
    ]


class RunNewConsole(object):
    """Run the command in a new console window. Windows only. Use in a with statement.

    subprocess sucks and really limits your access to the win32 API. Its implementation is half-assed. Using this so
    that STARTUPINFO.lpTitle actually works and STARTUPINFO.dwFillAttribute produce the expected result.
    """

    def __init__(self, command, new_max_window=True, title=None, white_bg=False):
        """Constructor.

        :param iter command: Command to run.
        :param bool new_max_window: Start process in new console window, maximized.
        :param bool white_bg: New console window will be black text on white background.
        :param bytes title: Set new window title to this. Needed by user32.FindWindow.
        """
        if title is None:
            title = 'pytest-{0}-{1}'.format(os.getpid(), random.randint(1000, 9999)).encode('ascii')
        self.startup_info = StartupInfo(new_max_window=new_max_window, title=title, white_bg=white_bg)
        self.process_info = ProcessInfo()
        self.command_str = subprocess.list2cmdline(command).encode('ascii')
        self._handles = list()
        self._stdin = self._setup_stdin()

    def __del__(self):
        """Close win32 handles."""
        while self._handles:
            try:
                ctypes.windll.kernel32.CloseHandle(self._handles.pop(0))  # .pop() is thread safe.
            except IndexError:
                break

    def __enter__(self):
        """Entering the `with` block. Runs the process."""
        res = ctypes.windll.kernel32.CreateProcessA(
            None,  # lpApplicationName
            self.command_str,  # lpCommandLine
            None,  # lpProcessAttributes
            None,  # lpThreadAttributes
            False,  # bInheritHandles
            subprocess.CREATE_NEW_CONSOLE,  # dwCreationFlags
            None,  # lpEnvironment
            str(PROJECT_ROOT).encode('ascii'),  # lpCurrentDirectory
            ctypes.byref(self.startup_info),  # lpStartupInfo
            ctypes.byref(self.process_info)  # lpProcessInformation
        )
        assert res

        # Add handles added by the OS.
        self._handles.append(self.process_info.hProcess)
        self._handles.append(self.process_info.hThread)

        # Get hWnd.
        self.hwnd = 0
        for _ in range(int(5 / 0.1)):
            # Takes time for console window to initialize.
            self.hwnd = ctypes.windll.user32.FindWindowA(None, self.startup_info.lpTitle)
            if self.hwnd:
                break
            time.sleep(0.1)
        assert self.hwnd

        # Return generator that yields window size/position.
        return self._iter_pos()

    def __exit__(self, *_):
        """Cleanup."""
        try:
            # Verify process exited 0.
            status = ctypes.c_ulong(STILL_ACTIVE)
            while status.value == STILL_ACTIVE:
                time.sleep(0.1)
                res = ctypes.windll.kernel32.GetExitCodeProcess(self.process_info.hProcess, ctypes.byref(status))
                assert res
            assert status.value == 0
        finally:
            # Close handles.
            self.__del__()

    def _setup_stdin(self):
        """Setup stdin pipe to allow Python to write to the window's stdin."""
        sec_attr = struct.pack('LPl', struct.Struct('LPl').size, True, 0)  # SECURITY_ATTRIBUTES

        # Create pipe.
        h_stdin_r, h_stdin_w = ctypes.c_ulong(), ctypes.c_ulong()
        res = ctypes.windll.kernel32.CreatePipe(
            ctypes.byref(h_stdin_r),
            ctypes.byref(h_stdin_w),
            ctypes.byref(sec_attr),  # Without this stdin drops everything.
            0,  # nSize (0 = system default).
        )
        assert res
        self._handles.append(h_stdin_r.value)
        self._handles.append(h_stdin_w.value)
        res = ctypes.windll.kernel32.SetHandleInformation(h_stdin_w, HANDLE_FLAG_INHERIT, 0)
        assert res

        # Update STARTUPINFO.
        self.startup_info.dwFlags |= STARTF_USESTDHANDLES
        self.startup_info.hStdInput = h_stdin_r

        return h_stdin_w.value

    def _iter_pos(self):
        """Yield new console window's current position and dimensions.

        If this generator's send method is called, data is sent to new console window's stdin handle.

        :return: Yields region the new window is in (left, upper, right, lower).
        :rtype: tuple
        """
        rect = ctypes.create_string_buffer(16)  # To be written to by GetWindowRect. RECT structure.
        while ctypes.windll.user32.GetWindowRect(self.hwnd, rect):
            left, top, right, bottom = struct.unpack('llll', rect.raw)
            width, height = right - left, bottom - top
            assert width > 1
            assert height > 1
            text = (yield left, top, right, bottom)
            if text:
                assert ctypes.windll.kernel32.WriteFile(self._stdin, text, len(text), None, None)
        raise StopIteration


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


def screenshot_until_match(save_to, timeout, subimg_candidates, expected_count, box=None):
    """Take screenshots until one of the 'done' subimages is found. Image is saved when subimage found or at timeout.

    If you get ImportError run "pip install pillow". Only OSX and Windows is supported.

    :param str save_to: Save screenshot to this PNG file path when expected count found or timeout.
    :param int timeout: Give up after these many seconds.
    :param iter subimg_candidates: Subimage paths to look for. List of strings.
    :param int expected_count: Keep trying until any of subimg_candidates is found this many times.
    :param tuple box: Crop screen shot to this region (left, upper, right, lower).

    :return: If one of the 'done' subimages was found somewhere in the screenshot.
    :rtype: bool
    """
    from PIL import Image, ImageGrab
    assert save_to.endswith('.png')
    stop_after = time.time() + timeout

    # Take screenshots until subimage is found.
    while True:
        with ImageGrab.grab(box) as rgba:
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
