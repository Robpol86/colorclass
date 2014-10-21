# colorclass

Yet another ANSI color text library for Python. Provides "auto colors" for dark/light terminals.

In Python2.x this library subclasses `unicode`, while on Python3.x it subclasses `str`. `colorclass` is supported on
Python 2.6, 2.7, 3.3, and 3.4.

[![Build Status](https://travis-ci.org/Robpol86/colorclass.svg?branch=master)]
(https://travis-ci.org/Robpol86/colorclass)
[![Coverage Status](https://img.shields.io/coveralls/Robpol86/colorclass.svg)]
(https://coveralls.io/r/Robpol86/colorclass)
[![Latest Version](https://pypip.in/version/colorclass/badge.png)]
(https://pypi.python.org/pypi/colorclass/)
[![Downloads](https://pypip.in/download/colorclass/badge.png)]
(https://pypi.python.org/pypi/colorclass/)
[![Download format](https://pypip.in/format/colorclass/badge.png)]
(https://pypi.python.org/pypi/colorclass/)
[![License](https://pypip.in/license/colorclass/badge.png)]
(https://pypi.python.org/pypi/colorclass/)

## Quickstart

Install:
```bash
pip install colorclass
```

## Example Implementation

![Example Script Screenshot](/example.png?raw=true "Example Script Screenshot")

Source code for the example code is: [example.py](example.py)

## Usage

Different colors are chosen using curly-bracket tags, such as `{red}{/red}`. For a list of available colors, call
`colorclass.list_tags()`.

The available "auto colors" tags are:

* autoblack
* autored
* autogreen
* autoyellow
* autoblue
* automagenta
* autocyan
* autowhite

Methods of Class instances try to return sane data, such as:

```python
from colorclass import Color
color_string = Color('{red}Test{/red}')

color_string
u'\x1b[31mTest\x1b[39m'

len(color_string)
4

color_string.istitle()
True
```

There are also a couple of helper attributes for all Color instances:

```python
color_string.value_colors
'\x1b[31mTest\x1b[39m'

color_string.value_no_colors
'Test'
```

## Changelog

#### 1.0.2

* Added ability to disable/strip out all colors.

#### 1.0.1

* Fixed splitlines() method.

#### 1.0.0

* Initial release.
