#!/usr/bin/env python
"""Example usage of colorclass.

Just prints sample text and exits.

Usage:
    example.py print [--light-bg|--no-colors]
    example.py -h | --help

Options:
    -h --help       Show this screen.
    --light-bg      Autocolors adapt to white/light backgrounds for Linux/OSX.
    --no-colors     Strip out any foreground or background colors.
"""

from __future__ import print_function
from colorclass import Color, disable_all_colors, set_light_background, Windows
from docopt import docopt
import os

OPTIONS = docopt(__doc__) if __name__ == '__main__' else dict()


def main():
    if OPTIONS.get('--no-colors'):
        disable_all_colors()
    elif os.name == 'nt':
        Windows.enable(auto_colors=True, reset_atexit=True)
    elif OPTIONS.get('--light-bg'):
        set_light_background()

    # Light or dark colors.
    print('Autocolors for all backgrounds:')
    print(Color('    {autoblack}Black{/hiblack} {autored}Red{/hired} {autogreen}Green{/higreen} '), end='')
    print(Color('{autoyellow}Yellow{/hiyellow} {autoblue}Blue{/hiblue} {automagenta}Magenta{/himagenta} '), end='')
    print(Color('{autocyan}Cyan{/hicyan} {autowhite}White{/hiwhite}'))

    print(Color('    {autobgblack}{autoblack}Black{/hiblack}{/hibgblack} '), end='')
    print(Color('{autobgblack}{autored}Red{/hired}{/hibgblack} {autobgblack}{autogreen}Green{/higreen}{/hibgblack} '), end='')
    print(Color('{autobgblack}{autoyellow}Yellow{/hiyellow}{/hibgblack} '), end='')
    print(Color('{autobgblack}{autoblue}Blue{/hiblue}{/hibgblack} '), end='')
    print(Color('{autobgblack}{automagenta}Magenta{/himagenta}{/hibgblack} '), end='')
    print(Color('{autobgblack}{autocyan}Cyan{/hicyan}{/hibgblack} {autobgblack}{autowhite}White{/hiwhite}{/hibgblack}'))

    print(Color('    {autobgred}{autoblack}Black{/hiblack}{/hibgred} {autobgred}{autored}Red{/hired}{/hibgred} '), end='')
    print(Color('{autobgred}{autogreen}Green{/higreen}{/hibgred} {autobgred}{autoyellow}Yellow{/hiyellow}{/hibgred} '), end='')
    print(Color('{autobgred}{autoblue}Blue{/hiblue}{/hibgred} {autobgred}{automagenta}Magenta{/himagenta}{/hibgred} '), end='')
    print(Color('{autobgred}{autocyan}Cyan{/hicyan}{/hibgred} {autobgred}{autowhite}White{/hiwhite}{/hibgred}'))

    print(Color('    {autobggreen}{autoblack}Black{/hiblack}{/hibggreen} '), end='')
    print(Color('{autobggreen}{autored}Red{/hired}{/hibggreen} {autobggreen}{autogreen}Green{/higreen}{/hibggreen} '), end='')
    print(Color('{autobggreen}{autoyellow}Yellow{/hiyellow}{/hibggreen} '), end='')
    print(Color('{autobggreen}{autoblue}Blue{/hiblue}{/hibggreen} '), end='')
    print(Color('{autobggreen}{automagenta}Magenta{/himagenta}{/hibggreen} '), end='')
    print(Color('{autobggreen}{autocyan}Cyan{/hicyan}{/hibggreen} {autobggreen}{autowhite}White{/hiwhite}{/hibggreen}'))

    print(Color('    {autobgyellow}{autoblack}Black{/hiblack}{/hibgyellow} '), end='')
    print(Color('{autobgyellow}{autored}Red{/hired}{/hibgyellow} '), end='')
    print(Color('{autobgyellow}{autogreen}Green{/higreen}{/hibgyellow} '), end='')
    print(Color('{autobgyellow}{autoyellow}Yellow{/hiyellow}{/hibgyellow} '), end='')
    print(Color('{autobgyellow}{autoblue}Blue{/hiblue}{/hibgyellow} '), end='')
    print(Color('{autobgyellow}{automagenta}Magenta{/himagenta}{/hibgyellow} '), end='')
    print(Color('{autobgyellow}{autocyan}Cyan{/hicyan}{/hibgyellow} {autobgyellow}{autowhite}White{/hiwhite}{/hibgyellow}'))

    print(Color('    {autobgblue}{autoblack}Black{/hiblack}{/hibgblue} {autobgblue}{autored}Red{/hired}{/hibgblue} '), end='')
    print(Color('{autobgblue}{autogreen}Green{/higreen}{/hibgblue} '), end='')
    print(Color('{autobgblue}{autoyellow}Yellow{/hiyellow}{/hibgblue} {autobgblue}{autoblue}Blue{/hiblue}{/hibgblue} '), end='')
    print(Color('{autobgblue}{automagenta}Magenta{/himagenta}{/hibgblue} '), end='')
    print(Color('{autobgblue}{autocyan}Cyan{/hicyan}{/hibgblue} {autobgblue}{autowhite}White{/hiwhite}{/hibgblue}'))

    print(Color('    {autobgmagenta}{autoblack}Black{/hiblack}{/hibgmagenta} '), end='')
    print(Color('{autobgmagenta}{autored}Red{/hired}{/hibgmagenta} '), end='')
    print(Color('{autobgmagenta}{autogreen}Green{/higreen}{/hibgmagenta} '), end='')
    print(Color('{autobgmagenta}{autoyellow}Yellow{/hiyellow}{/hibgmagenta} '), end='')
    print(Color('{autobgmagenta}{autoblue}Blue{/hiblue}{/hibgmagenta} '), end='')
    print(Color('{autobgmagenta}{automagenta}Magenta{/himagenta}{/hibgmagenta} '), end='')
    print(Color('{autobgmagenta}{autocyan}Cyan{/hicyan}{/hibgmagenta} '), end='')
    print(Color('{autobgmagenta}{autowhite}White{/hiwhite}{/hibgmagenta}'))

    print(Color('    {autobgcyan}{autoblack}Black{/hiblack}{/hibgcyan} {autobgcyan}{autored}Red{/hired}{/hibgcyan} '), end='')
    print(Color('{autobgcyan}{autogreen}Green{/higreen}{/hibgcyan} '), end='')
    print(Color('{autobgcyan}{autoyellow}Yellow{/hiyellow}{/hibgcyan} {autobgcyan}{autoblue}Blue{/hiblue}{/hibgcyan} '), end='')
    print(Color('{autobgcyan}{automagenta}Magenta{/himagenta}{/hibgcyan} '), end='')
    print(Color('{autobgcyan}{autocyan}Cyan{/hicyan}{/hibgcyan} {autobgcyan}{autowhite}White{/hiwhite}{/hibgcyan}'))

    print(Color('    {autobgwhite}{autoblack}Black{/hiblack}{/hibgwhite} '), end='')
    print(Color('{autobgwhite}{autored}Red{/hired}{/hibgwhite} {autobgwhite}{autogreen}Green{/higreen}{/hibgwhite} '), end='')
    print(Color('{autobgwhite}{autoyellow}Yellow{/hiyellow}{/hibgwhite} '), end='')
    print(Color('{autobgwhite}{autoblue}Blue{/hiblue}{/hibgwhite} '), end='')
    print(Color('{autobgwhite}{automagenta}Magenta{/himagenta}{/hibgwhite} '), end='')
    print(Color('{autobgwhite}{autocyan}Cyan{/hicyan}{/hibgwhite} {autobgwhite}{autowhite}White{/hiwhite}{/hibgwhite}'))
    print()

    # Light colors.
    print('Light colors for dark backgrounds:')
    print(Color('    {hiblack}Black{/hiblack} {hired}Red{/hired} {higreen}Green{/higreen} '), end='')
    print(Color('{hiyellow}Yellow{/hiyellow} {hiblue}Blue{/hiblue} {himagenta}Magenta{/himagenta} '), end='')
    print(Color('{hicyan}Cyan{/hicyan} {hiwhite}White{/hiwhite}'))

    print(Color('    {hibgblack}{hiblack}Black{/hiblack}{/hibgblack} '), end='')
    print(Color('{hibgblack}{hired}Red{/hired}{/hibgblack} {hibgblack}{higreen}Green{/higreen}{/hibgblack} '), end='')
    print(Color('{hibgblack}{hiyellow}Yellow{/hiyellow}{/hibgblack} '), end='')
    print(Color('{hibgblack}{hiblue}Blue{/hiblue}{/hibgblack} '), end='')
    print(Color('{hibgblack}{himagenta}Magenta{/himagenta}{/hibgblack} '), end='')
    print(Color('{hibgblack}{hicyan}Cyan{/hicyan}{/hibgblack} {hibgblack}{hiwhite}White{/hiwhite}{/hibgblack}'))

    print(Color('    {hibgred}{hiblack}Black{/hiblack}{/hibgred} {hibgred}{hired}Red{/hired}{/hibgred} '), end='')
    print(Color('{hibgred}{higreen}Green{/higreen}{/hibgred} {hibgred}{hiyellow}Yellow{/hiyellow}{/hibgred} '), end='')
    print(Color('{hibgred}{hiblue}Blue{/hiblue}{/hibgred} {hibgred}{himagenta}Magenta{/himagenta}{/hibgred} '), end='')
    print(Color('{hibgred}{hicyan}Cyan{/hicyan}{/hibgred} {hibgred}{hiwhite}White{/hiwhite}{/hibgred}'))

    print(Color('    {hibggreen}{hiblack}Black{/hiblack}{/hibggreen} '), end='')
    print(Color('{hibggreen}{hired}Red{/hired}{/hibggreen} {hibggreen}{higreen}Green{/higreen}{/hibggreen} '), end='')
    print(Color('{hibggreen}{hiyellow}Yellow{/hiyellow}{/hibggreen} '), end='')
    print(Color('{hibggreen}{hiblue}Blue{/hiblue}{/hibggreen} '), end='')
    print(Color('{hibggreen}{himagenta}Magenta{/himagenta}{/hibggreen} '), end='')
    print(Color('{hibggreen}{hicyan}Cyan{/hicyan}{/hibggreen} {hibggreen}{hiwhite}White{/hiwhite}{/hibggreen}'))

    print(Color('    {hibgyellow}{hiblack}Black{/hiblack}{/hibgyellow} '), end='')
    print(Color('{hibgyellow}{hired}Red{/hired}{/hibgyellow} '), end='')
    print(Color('{hibgyellow}{higreen}Green{/higreen}{/hibgyellow} '), end='')
    print(Color('{hibgyellow}{hiyellow}Yellow{/hiyellow}{/hibgyellow} '), end='')
    print(Color('{hibgyellow}{hiblue}Blue{/hiblue}{/hibgyellow} '), end='')
    print(Color('{hibgyellow}{himagenta}Magenta{/himagenta}{/hibgyellow} '), end='')
    print(Color('{hibgyellow}{hicyan}Cyan{/hicyan}{/hibgyellow} {hibgyellow}{hiwhite}White{/hiwhite}{/hibgyellow}'))

    print(Color('    {hibgblue}{hiblack}Black{/hiblack}{/hibgblue} {hibgblue}{hired}Red{/hired}{/hibgblue} '), end='')
    print(Color('{hibgblue}{higreen}Green{/higreen}{/hibgblue} '), end='')
    print(Color('{hibgblue}{hiyellow}Yellow{/hiyellow}{/hibgblue} {hibgblue}{hiblue}Blue{/hiblue}{/hibgblue} '), end='')
    print(Color('{hibgblue}{himagenta}Magenta{/himagenta}{/hibgblue} '), end='')
    print(Color('{hibgblue}{hicyan}Cyan{/hicyan}{/hibgblue} {hibgblue}{hiwhite}White{/hiwhite}{/hibgblue}'))

    print(Color('    {hibgmagenta}{hiblack}Black{/hiblack}{/hibgmagenta} '), end='')
    print(Color('{hibgmagenta}{hired}Red{/hired}{/hibgmagenta} '), end='')
    print(Color('{hibgmagenta}{higreen}Green{/higreen}{/hibgmagenta} '), end='')
    print(Color('{hibgmagenta}{hiyellow}Yellow{/hiyellow}{/hibgmagenta} '), end='')
    print(Color('{hibgmagenta}{hiblue}Blue{/hiblue}{/hibgmagenta} '), end='')
    print(Color('{hibgmagenta}{himagenta}Magenta{/himagenta}{/hibgmagenta} '), end='')
    print(Color('{hibgmagenta}{hicyan}Cyan{/hicyan}{/hibgmagenta} '), end='')
    print(Color('{hibgmagenta}{hiwhite}White{/hiwhite}{/hibgmagenta}'))

    print(Color('    {hibgcyan}{hiblack}Black{/hiblack}{/hibgcyan} {hibgcyan}{hired}Red{/hired}{/hibgcyan} '), end='')
    print(Color('{hibgcyan}{higreen}Green{/higreen}{/hibgcyan} '), end='')
    print(Color('{hibgcyan}{hiyellow}Yellow{/hiyellow}{/hibgcyan} {hibgcyan}{hiblue}Blue{/hiblue}{/hibgcyan} '), end='')
    print(Color('{hibgcyan}{himagenta}Magenta{/himagenta}{/hibgcyan} '), end='')
    print(Color('{hibgcyan}{hicyan}Cyan{/hicyan}{/hibgcyan} {hibgcyan}{hiwhite}White{/hiwhite}{/hibgcyan}'))

    print(Color('    {hibgwhite}{hiblack}Black{/hiblack}{/hibgwhite} '), end='')
    print(Color('{hibgwhite}{hired}Red{/hired}{/hibgwhite} {hibgwhite}{higreen}Green{/higreen}{/hibgwhite} '), end='')
    print(Color('{hibgwhite}{hiyellow}Yellow{/hiyellow}{/hibgwhite} '), end='')
    print(Color('{hibgwhite}{hiblue}Blue{/hiblue}{/hibgwhite} '), end='')
    print(Color('{hibgwhite}{himagenta}Magenta{/himagenta}{/hibgwhite} '), end='')
    print(Color('{hibgwhite}{hicyan}Cyan{/hicyan}{/hibgwhite} {hibgwhite}{hiwhite}White{/hiwhite}{/hibgwhite}'))
    print()

    # Dark colors.
    print('Dark colors for light backgrounds:')
    print(Color('    {black}Black{/black} {red}Red{/red} {green}Green{/green} {yellow}Yellow{/yellow} '), end='')
    print(Color('{blue}Blue{/blue} {magenta}Magenta{/magenta} {cyan}Cyan{/cyan} {white}White{/white}'))

    print(Color('    {bgblack}{black}Black{/black}{/bgblack} {bgblack}{red}Red{/red}{/bgblack} '), end='')
    print(Color('{bgblack}{green}Green{/green}{/bgblack} {bgblack}{yellow}Yellow{/yellow}{/bgblack} '), end='')
    print(Color('{bgblack}{blue}Blue{/blue}{/bgblack} {bgblack}{magenta}Magenta{/magenta}{/bgblack} '), end='')
    print(Color('{bgblack}{cyan}Cyan{/cyan}{/bgblack} {bgblack}{white}White{/white}{/bgblack}'))

    print(Color('    {bgred}{black}Black{/black}{/bgred} {bgred}{red}Red{/red}{/bgred} '), end='')
    print(Color('{bgred}{green}Green{/green}{/bgred} {bgred}{yellow}Yellow{/yellow}{/bgred} '), end='')
    print(Color('{bgred}{blue}Blue{/blue}{/bgred} {bgred}{magenta}Magenta{/magenta}{/bgred} '), end='')
    print(Color('{bgred}{cyan}Cyan{/cyan}{/bgred} {bgred}{white}White{/white}{/bgred}'))

    print(Color('    {bggreen}{black}Black{/black}{/bggreen} {bggreen}{red}Red{/red}{/bggreen} '), end='')
    print(Color('{bggreen}{green}Green{/green}{/bggreen} {bggreen}{yellow}Yellow{/yellow}{/bggreen} '), end='')
    print(Color('{bggreen}{blue}Blue{/blue}{/bggreen} {bggreen}{magenta}Magenta{/magenta}{/bggreen} '), end='')
    print(Color('{bggreen}{cyan}Cyan{/cyan}{/bggreen} {bggreen}{white}White{/white}{/bggreen}'))

    print(Color('    {bgyellow}{black}Black{/black}{/bgyellow} {bgyellow}{red}Red{/red}{/bgyellow} '), end='')
    print(Color('{bgyellow}{green}Green{/green}{/bgyellow} {bgyellow}{yellow}Yellow{/yellow}{/bgyellow} '), end='')
    print(Color('{bgyellow}{blue}Blue{/blue}{/bgyellow} {bgyellow}{magenta}Magenta{/magenta}{/bgyellow} '), end='')
    print(Color('{bgyellow}{cyan}Cyan{/cyan}{/bgyellow} {bgyellow}{white}White{/white}{/bgyellow}'))

    print(Color('    {bgblue}{black}Black{/black}{/bgblue} {bgblue}{red}Red{/red}{/bgblue} '), end='')
    print(Color('{bgblue}{green}Green{/green}{/bgblue} {bgblue}{yellow}Yellow{/yellow}{/bgblue} '), end='')
    print(Color('{bgblue}{blue}Blue{/blue}{/bgblue} {bgblue}{magenta}Magenta{/magenta}{/bgblue} '), end='')
    print(Color('{bgblue}{cyan}Cyan{/cyan}{/bgblue} {bgblue}{white}White{/white}{/bgblue}'))

    print(Color('    {bgmagenta}{black}Black{/black}{/bgmagenta} {bgmagenta}{red}Red{/red}{/bgmagenta} '), end='')
    print(Color('{bgmagenta}{green}Green{/green}{/bgmagenta} {bgmagenta}{yellow}Yellow{/yellow}{/bgmagenta} '), end='')
    print(Color('{bgmagenta}{blue}Blue{/blue}{/bgmagenta} {bgmagenta}{magenta}Magenta{/magenta}{/bgmagenta} '), end='')
    print(Color('{bgmagenta}{cyan}Cyan{/cyan}{/bgmagenta} {bgmagenta}{white}White{/white}{/bgmagenta}'))

    print(Color('    {bgcyan}{black}Black{/black}{/bgcyan} {bgcyan}{red}Red{/red}{/bgcyan} '), end='')
    print(Color('{bgcyan}{green}Green{/green}{/bgcyan} {bgcyan}{yellow}Yellow{/yellow}{/bgcyan} '), end='')
    print(Color('{bgcyan}{blue}Blue{/blue}{/bgcyan} {bgcyan}{magenta}Magenta{/magenta}{/bgcyan} '), end='')
    print(Color('{bgcyan}{cyan}Cyan{/cyan}{/bgcyan} {bgcyan}{white}White{/white}{/bgcyan}'))

    print(Color('    {bgwhite}{black}Black{/black}{/bgwhite} {bgwhite}{red}Red{/red}{/bgwhite} '), end='')
    print(Color('{bgwhite}{green}Green{/green}{/bgwhite} {bgwhite}{yellow}Yellow{/yellow}{/bgwhite} '), end='')
    print(Color('{bgwhite}{blue}Blue{/blue}{/bgwhite} {bgwhite}{magenta}Magenta{/magenta}{/bgwhite} '), end='')
    print(Color('{bgwhite}{cyan}Cyan{/cyan}{/bgwhite} {bgwhite}{white}White{/white}{/bgwhite}'))


if __name__ == '__main__':
    main()
