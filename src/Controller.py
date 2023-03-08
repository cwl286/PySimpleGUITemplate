from src.SheetController import SheetController
import os
import pandas as pd

class Controller():
    def __init__(self) -> None:
        self.FILE_PATH = os.getenv("FILE_PATH")
        self.SHEETNAME = os.getenv("SHEETNAME")
        if os.getenv("HEADER_INDEX"):
            self.HEADER_INDEX = int(os.getenv("HEADER_INDEX"))
        # Load ratio sheet
        self.sheet_con = SheetController(self.FILE_PATH, sheet_name=self.SHEETNAME, header=self.HEADER_INDEX)
        self.sheet_con.readExcel()

    def display(self):
        self.gui.display()

    # query and parse profile
    def addRow(self) -> pd.DataFrame:
        max_row = self.sheet_con.getMaxRow()
        arr = ['id' + str(max_row), 't' + str(max_row)]
        self.sheet_con.appendOneRow(arr)
        return self.sheet_con.getSheet()
   
    def SaveData(self) -> None:
        self.sheet_con.writeExcel()
    
    def getData(self) -> pd.DataFrame:
        return self.sheet_con.getSheet()