# colorclass

Yet another ANSI color text library for Python. Provides "auto colors" for dark/light terminals.

In Python2.x this library subclasses `unicode`, while on Python3.x it subclasses `str`.

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
