#!/usr/bin/env python

import ast
import atexit
from codecs import open
from distutils.spawn import find_executable
import os
import sys
import subprocess

import setuptools.command.sdist
from setuptools.command.test import test

DESCRIPTION = 'Colorful worry-free console applications for Linux, Mac OS X, and Windows.'
HERE = os.path.abspath(os.path.dirname(__file__))
KEYWORDS = 'Shell Bash ANSI ASCII terminal console colors automatic'
NAME = 'colorclass'
NAME_FILE = NAME
PACKAGE = False


def packages_or_py_modules():
    if not PACKAGE:
        return dict(py_modules=[NAME_FILE])
    packages = [NAME_FILE]
    packages.extend([os.path.join(r, s) for r, d, _ in os.walk(NAME_FILE) for s in d if s != '__pycache__'])
    return dict(packages=packages)


def get_metadata(main_file):
    """Get metadata about the package/module.

    Positional arguments:
    main_file -- python file path within `HERE` which has __author__ and the others defined as global variables.

    Returns:
    Dictionary to be passed into setuptools.setup().
    """
    install_requires, tests_require = list(), list()
    if os.path.isfile(os.path.join(HERE, 'requirements.txt')):
        with open(os.path.join(HERE, 'requirements.txt')) as f:
            data = f.read()
            install_requires = (data.decode('ascii', 'ignore') if hasattr(data, 'decode') else data).splitlines()
    if os.path.isfile(os.path.join(HERE, 'requirements-test.txt')):
        with open(os.path.join(HERE, 'requirements-test.txt')) as f:
            data = f.read()
            (data.decode('ascii', 'ignore') if hasattr(data, 'decode') else data).splitlines()

    with open(os.path.join(HERE, 'README.rst'), encoding='utf-8') as f:
        long_description = f.read(100000)

    with open(os.path.join(HERE, main_file), encoding='utf-8') as f:
        lines = [l.strip() for l in f if l.startswith('__')]
    metadata = ast.literal_eval("{'" + ", '".join([l.replace(' = ', "': ") for l in lines]) + '}')
    __author__, __license__, __version__ = [metadata[k] for k in ('__author__', '__license__', '__version__')]

    everything = dict(version=__version__, long_description=long_description, author=__author__, license=__license__)
    if not all(everything.values()):
        raise ValueError('Failed to obtain metadata from package/module.')

    everything.update(packages_or_py_modules())
    everything.update(dict(install_requires=install_requires, tests_require=tests_require))

    return everything


class PyTest(test):
    description = 'Run all tests.'
    user_options = []
    CMD = 'test'
    TEST_ARGS = ['--cov-report', 'term-missing', '--cov', NAME_FILE, 'tests']

    def finalize_options(self):
        overflow_args = sys.argv[sys.argv.index(self.CMD) + 1:]
        test.finalize_options(self)
        setattr(self, 'test_args', self.TEST_ARGS + overflow_args)
        setattr(self, 'test_suite', True)

    def run_tests(self):
        # Import here, cause outside the eggs aren't loaded.
        pytest = __import__('pytest')
        err_no = pytest.main(self.test_args)
        sys.exit(err_no)


class PyTestPdb(PyTest):
    description = 'Run all tests, drops to ipdb upon unhandled exception.'
    CMD = 'testpdb'
    TEST_ARGS = ['--ipdb', 'tests']


class PyTestCovWeb(PyTest):
    description = 'Generates HTML report on test coverage.'
    CMD = 'testcovweb'
    TEST_ARGS = ['--cov-report', 'html', '--cov', NAME_FILE, 'tests']

    def run_tests(self):
        if find_executable('open'):
            atexit.register(lambda: subprocess.call(['open', os.path.join(HERE, 'htmlcov', 'index.html')]))
        PyTest.run_tests(self)


ALL_DATA = dict(
    name=NAME,
    description=DESCRIPTION,
    url='https://github.com/Robpol86/{0}'.format(NAME),
    author_email='robpol86@gmail.com',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries',
        'Topic :: Terminals',
        'Topic :: Text Processing :: Markup',
    ],

    keywords=KEYWORDS,
    zip_safe=True,
    cmdclass={PyTest.CMD: PyTest, PyTestPdb.CMD: PyTestPdb, PyTestCovWeb.CMD: PyTestCovWeb},

    # Pass the rest from get_metadata().
    **get_metadata(os.path.join(NAME_FILE + ('/__init__.py' if PACKAGE else '.py')))
)


if __name__ == '__main__':
    setuptools.setup(**ALL_DATA)
