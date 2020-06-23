import progressbar
from tqdm import tqdm
from time import sleep
from random import randrange


class ProgressBar:
    def __init__(self):
        self.bar = progressbar.ProgressBar(maxval=20, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])


class ProgressBar_2:
    @staticmethod
    def func_call(position, total):
        text = 'progressbar #{position}'.format(position=position)
        with tqdm(total=total, position=position, desc=text) as progress:
            for _ in range(0, total, 5):
                progress.update(5)
                sleep(randrange(3))
