from src.model.Stat import Stat
from src.model.Note import Note


class Sheet:

    def __init__(self):
        self.stat_list: list[Stat] = []
        self.note_list: list[Note] = []
