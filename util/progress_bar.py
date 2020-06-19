import progressbar
from time import sleep


class ProgressBar:
    def __init__(self):
        self.bar = progressbar.ProgressBar(maxval=20, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])


