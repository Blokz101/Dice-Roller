from src.model.Instruction import Instruction


class Note:

    def __init__(self, name: str = "", raw_text: str = ""):
        self.name: str = name
        self.raw_text: str = raw_text
        self.text: str = ""
        self.inst_list: list[Instruction] = []
