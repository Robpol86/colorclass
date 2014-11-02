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
    print(Color('    {autoblack}Black{/black} {autored}Red{/red} {autogreen}Green{/green} '), end='')
    print(Color('{autoyellow}Yellow{/yellow} {autoblue}Blue{/blue} {automagenta}Magenta{/magenta} '), end='')
    print(Color('{autocyan}Cyan{/cyan} {autowhite}White{/white}'))

    print(Color('    {autobgblack}{autoblack}Black{/black}{/bgblack} '), end='')
    print(Color('{autobgblack}{autored}Red{/red}{/bgblack} {autobgblack}{autogreen}Green{/green}{/bgblack} '), end='')
    print(Color('{autobgblack}{autoyellow}Yellow{/yellow}{/bgblack} '), end='')
    print(Color('{autobgblack}{autoblue}Blue{/blue}{/bgblack} '), end='')
    print(Color('{autobgblack}{automagenta}Magenta{/magenta}{/bgblack} '), end='')
    print(Color('{autobgblack}{autocyan}Cyan{/cyan}{/bgblack} {autobgblack}{autowhite}White{/white}{/bgblack}'))

    print(Color('    {autobgred}{autoblack}Black{/black}{/bgred} {autobgred}{autored}Red{/red}{/bgred} '), end='')
    print(Color('{autobgred}{autogreen}Green{/green}{/bgred} {autobgred}{autoyellow}Yellow{/yellow}{/bgred} '), end='')
    print(Color('{autobgred}{autoblue}Blue{/blue}{/bgred} {autobgred}{automagenta}Magenta{/magenta}{/bgred} '), end='')
    print(Color('{autobgred}{autocyan}Cyan{/cyan}{/bgred} {autobgred}{autowhite}White{/white}{/bgred}'))

    print(Color('    {autobggreen}{autoblack}Black{/black}{/bggreen} '), end='')
    print(Color('{autobggreen}{autored}Red{/red}{/bggreen} {autobggreen}{autogreen}Green{/green}{/bggreen} '), end='')
    print(Color('{autobggreen}{autoyellow}Yellow{/yellow}{/bggreen} '), end='')
    print(Color('{autobggreen}{autoblue}Blue{/blue}{/bggreen} '), end='')
    print(Color('{autobggreen}{automagenta}Magenta{/magenta}{/bggreen} '), end='')
    print(Color('{autobggreen}{autocyan}Cyan{/cyan}{/bggreen} {autobggreen}{autowhite}White{/white}{/bggreen}'))

    print(Color('    {autobgyellow}{autoblack}Black{/black}{/bgyellow} '), end='')
    print(Color('{autobgyellow}{autored}Red{/red}{/bgyellow} '), end='')
    print(Color('{autobgyellow}{autogreen}Green{/green}{/bgyellow} '), end='')
    print(Color('{autobgyellow}{autoyellow}Yellow{/yellow}{/bgyellow} '), end='')
    print(Color('{autobgyellow}{autoblue}Blue{/blue}{/bgyellow} '), end='')
    print(Color('{autobgyellow}{automagenta}Magenta{/magenta}{/bgyellow} '), end='')
    print(Color('{autobgyellow}{autocyan}Cyan{/cyan}{/bgyellow} {autobgyellow}{autowhite}White{/white}{/bgyellow}'))

    print(Color('    {autobgblue}{autoblack}Black{/black}{/bgblue} {autobgblue}{autored}Red{/red}{/bgblue} '), end='')
    print(Color('{autobgblue}{autogreen}Green{/green}{/bgblue} '), end='')
    print(Color('{autobgblue}{autoyellow}Yellow{/yellow}{/bgblue} {autobgblue}{autoblue}Blue{/blue}{/bgblue} '), end='')
    print(Color('{autobgblue}{automagenta}Magenta{/magenta}{/bgblue} '), end='')
    print(Color('{autobgblue}{autocyan}Cyan{/cyan}{/bgblue} {autobgblue}{autowhite}White{/white}{/bgblue}'))

    print(Color('    {autobgmagenta}{autoblack}Black{/black}{/bgmagenta} '), end='')
    print(Color('{autobgmagenta}{autored}Red{/red}{/bgmagenta} '), end='')
    print(Color('{autobgmagenta}{autogreen}Green{/green}{/bgmagenta} '), end='')
    print(Color('{autobgmagenta}{autoyellow}Yellow{/yellow}{/bgmagenta} '), end='')
    print(Color('{autobgmagenta}{autoblue}Blue{/blue}{/bgmagenta} '), end='')
    print(Color('{autobgmagenta}{automagenta}Magenta{/magenta}{/bgmagenta} '), end='')
    print(Color('{autobgmagenta}{autocyan}Cyan{/cyan}{/bgmagenta} '), end='')
    print(Color('{autobgmagenta}{autowhite}White{/white}{/bgmagenta}'))

    print(Color('    {autobgcyan}{autoblack}Black{/black}{/bgcyan} {autobgcyan}{autored}Red{/red}{/bgcyan} '), end='')
    print(Color('{autobgcyan}{autogreen}Green{/green}{/bgcyan} '), end='')
    print(Color('{autobgcyan}{autoyellow}Yellow{/yellow}{/bgcyan} {autobgcyan}{autoblue}Blue{/blue}{/bgcyan} '), end='')
    print(Color('{autobgcyan}{automagenta}Magenta{/magenta}{/bgcyan} '), end='')
    print(Color('{autobgcyan}{autocyan}Cyan{/cyan}{/bgcyan} {autobgcyan}{autowhite}White{/white}{/bgcyan}'))

    print(Color('    {autobgwhite}{autoblack}Black{/black}{/bgwhite} '), end='')
    print(Color('{autobgwhite}{autored}Red{/red}{/bgwhite} {autobgwhite}{autogreen}Green{/green}{/bgwhite} '), end='')
    print(Color('{autobgwhite}{autoyellow}Yellow{/yellow}{/bgwhite} '), end='')
    print(Color('{autobgwhite}{autoblue}Blue{/blue}{/bgwhite} '), end='')
    print(Color('{autobgwhite}{automagenta}Magenta{/magenta}{/bgwhite} '), end='')
    print(Color('{autobgwhite}{autocyan}Cyan{/cyan}{/bgwhite} {autobgwhite}{autowhite}White{/white}{/bgwhite}'))
    print()

    # Light colors.
    print('Light colors for dark backgrounds:')
    print(Color('    {hiblack}Black{/black} {hired}Red{/red} {higreen}Green{/green} '), end='')
    print(Color('{hiyellow}Yellow{/yellow} {hiblue}Blue{/blue} {himagenta}Magenta{/magenta} '), end='')
    print(Color('{hicyan}Cyan{/cyan} {hiwhite}White{/white}'))

    print(Color('    {hibgblack}{hiblack}Black{/black}{/bgblack} '), end='')
    print(Color('{hibgblack}{hired}Red{/red}{/bgblack} {hibgblack}{higreen}Green{/green}{/bgblack} '), end='')
    print(Color('{hibgblack}{hiyellow}Yellow{/yellow}{/bgblack} '), end='')
    print(Color('{hibgblack}{hiblue}Blue{/blue}{/bgblack} '), end='')
    print(Color('{hibgblack}{himagenta}Magenta{/magenta}{/bgblack} '), end='')
    print(Color('{hibgblack}{hicyan}Cyan{/cyan}{/bgblack} {hibgblack}{hiwhite}White{/white}{/bgblack}'))

    print(Color('    {hibgred}{hiblack}Black{/black}{/bgred} {hibgred}{hired}Red{/red}{/bgred} '), end='')
    print(Color('{hibgred}{higreen}Green{/green}{/bgred} {hibgred}{hiyellow}Yellow{/yellow}{/bgred} '), end='')
    print(Color('{hibgred}{hiblue}Blue{/blue}{/bgred} {hibgred}{himagenta}Magenta{/magenta}{/bgred} '), end='')
    print(Color('{hibgred}{hicyan}Cyan{/cyan}{/bgred} {hibgred}{hiwhite}White{/white}{/bgred}'))

    print(Color('    {hibggreen}{hiblack}Black{/black}{/bggreen} '), end='')
    print(Color('{hibggreen}{hired}Red{/red}{/bggreen} {hibggreen}{higreen}Green{/green}{/bggreen} '), end='')
    print(Color('{hibggreen}{hiyellow}Yellow{/yellow}{/bggreen} '), end='')
    print(Color('{hibggreen}{hiblue}Blue{/blue}{/bggreen} '), end='')
    print(Color('{hibggreen}{himagenta}Magenta{/magenta}{/bggreen} '), end='')
    print(Color('{hibggreen}{hicyan}Cyan{/cyan}{/bggreen} {hibggreen}{hiwhite}White{/white}{/bggreen}'))

    print(Color('    {hibgyellow}{hiblack}Black{/black}{/bgyellow} '), end='')
    print(Color('{hibgyellow}{hired}Red{/red}{/bgyellow} '), end='')
    print(Color('{hibgyellow}{higreen}Green{/green}{/bgyellow} '), end='')
    print(Color('{hibgyellow}{hiyellow}Yellow{/yellow}{/bgyellow} '), end='')
    print(Color('{hibgyellow}{hiblue}Blue{/blue}{/bgyellow} '), end='')
    print(Color('{hibgyellow}{himagenta}Magenta{/magenta}{/bgyellow} '), end='')
    print(Color('{hibgyellow}{hicyan}Cyan{/cyan}{/bgyellow} {hibgyellow}{hiwhite}White{/white}{/bgyellow}'))

    print(Color('    {hibgblue}{hiblack}Black{/black}{/bgblue} {hibgblue}{hired}Red{/red}{/bgblue} '), end='')
    print(Color('{hibgblue}{higreen}Green{/green}{/bgblue} '), end='')
    print(Color('{hibgblue}{hiyellow}Yellow{/yellow}{/bgblue} {hibgblue}{hiblue}Blue{/blue}{/bgblue} '), end='')
    print(Color('{hibgblue}{himagenta}Magenta{/magenta}{/bgblue} '), end='')
    print(Color('{hibgblue}{hicyan}Cyan{/cyan}{/bgblue} {hibgblue}{hiwhite}White{/white}{/bgblue}'))

    print(Color('    {hibgmagenta}{hiblack}Black{/black}{/bgmagenta} '), end='')
    print(Color('{hibgmagenta}{hired}Red{/red}{/bgmagenta} '), end='')
    print(Color('{hibgmagenta}{higreen}Green{/green}{/bgmagenta} '), end='')
    print(Color('{hibgmagenta}{hiyellow}Yellow{/yellow}{/bgmagenta} '), end='')
    print(Color('{hibgmagenta}{hiblue}Blue{/blue}{/bgmagenta} '), end='')
    print(Color('{hibgmagenta}{himagenta}Magenta{/magenta}{/bgmagenta} '), end='')
    print(Color('{hibgmagenta}{hicyan}Cyan{/cyan}{/bgmagenta} '), end='')
    print(Color('{hibgmagenta}{hiwhite}White{/white}{/bgmagenta}'))

    print(Color('    {hibgcyan}{hiblack}Black{/black}{/bgcyan} {hibgcyan}{hired}Red{/red}{/bgcyan} '), end='')
    print(Color('{hibgcyan}{higreen}Green{/green}{/bgcyan} '), end='')
    print(Color('{hibgcyan}{hiyellow}Yellow{/yellow}{/bgcyan} {hibgcyan}{hiblue}Blue{/blue}{/bgcyan} '), end='')
    print(Color('{hibgcyan}{himagenta}Magenta{/magenta}{/bgcyan} '), end='')
    print(Color('{hibgcyan}{hicyan}Cyan{/cyan}{/bgcyan} {hibgcyan}{hiwhite}White{/white}{/bgcyan}'))

    print(Color('    {hibgwhite}{hiblack}Black{/black}{/bgwhite} '), end='')
    print(Color('{hibgwhite}{hired}Red{/red}{/bgwhite} {hibgwhite}{higreen}Green{/green}{/bgwhite} '), end='')
    print(Color('{hibgwhite}{hiyellow}Yellow{/yellow}{/bgwhite} '), end='')
    print(Color('{hibgwhite}{hiblue}Blue{/blue}{/bgwhite} '), end='')
    print(Color('{hibgwhite}{himagenta}Magenta{/magenta}{/bgwhite} '), end='')
    print(Color('{hibgwhite}{hicyan}Cyan{/cyan}{/bgwhite} {hibgwhite}{hiwhite}White{/white}{/bgwhite}'))
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
