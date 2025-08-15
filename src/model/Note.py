from src.model.Instruction import Instruction
import re

class Note:

    def __init__(self, name: str = "", raw_text: str = ""):
        self.name: str = name
        #self.raw_text: str = raw_text
        self.text: str = ""
        self.inst_list: list[Instruction] = []

        #----------------------------------
        #This is a temporary patch that should be replaced with more thorough parsing
        x = re.split("[\[].*[\]]", raw_text)
        self.raw_text: str = x[0]

        #-----------------------------------

        


