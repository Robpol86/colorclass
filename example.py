#!/usr/bin/env python
"""Example usage of colorclass.

Just prints sample text and exits.

Windows support effortlessly provided with the help of colorama:
    https://github.com/tartley/colorama
Though only dark colors seem to work.

Usage:
    example.py print [--light-bg]
    example.py print -h | --help
    example.py print_windows --light-bg

Options:
    -h --help       Show this screen.
    --light-bg      Autocolors adapt to white/light backgrounds.
"""

from __future__ import print_function
from colorclass import Color, set_light_background
from docopt import docopt

OPTIONS = docopt(__doc__) if __name__ == '__main__' else dict()


def main():
    if OPTIONS.get('print_windows'):
        import colorama
        colorama.init()

    if OPTIONS.get('--light-bg'):
        set_light_background()

    print('Autocolors for all backgrounds:')
    print(Color('    {autoblack}Black{/autoblack} {autored}Red{/autored} {autogreen}Green{/autogreen} '), end='')
    print(Color('{autoyellow}Yellow{/autoyellow} {autoblue}Blue{/autoblue} '), end='')
    print(Color('{automagenta}Magenta{/automagenta} {autocyan}Cyan{/autocyan} {autowhite}White{/autowhite}'))
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
