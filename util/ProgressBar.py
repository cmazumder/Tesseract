import sys
from random import choice

import progressbar
from colorama import Fore
from tqdm import tqdm


class ProgressBar:
    def __init__(self):
        self.bar = progressbar.ProgressBar(maxval=20,
                                           widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])


class ProgressBar2:
    color_bars = [Fore.BLACK,
                  Fore.RED,
                  Fore.GREEN,
                  Fore.YELLOW,
                  Fore.BLUE,
                  Fore.MAGENTA,
                  Fore.CYAN,
                  Fore.WHITE]

    def __init__(self, desc, total, position=None, leave=True, ascii=True, unit=" byte", colour=True):

        if colour:
            bar_format = "{l_bar}%s{bar}%s{r_bar}" % (choice(ProgressBar2.color_bars), Fore.RESET)
            self.bar = tqdm(desc=desc, total=total, position=position, unit=unit, unit_scale=True, ascii=ascii,
                            bar_format=bar_format, leave=leave, file=sys.stdout)
        else:
            self.bar = tqdm(desc=desc, total=total, position=position, unit=unit, unit_scale=True, ascii=ascii,
                            leave=leave, file=sys.stdout)