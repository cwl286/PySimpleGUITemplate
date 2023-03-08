import pandas as pd

class SheetController:
    def __init__(self, path: str, sheet_name: str="", header: int=0, nrows:int|None=None) -> None:
        self.path = path
        self.sheet_name = sheet_name
        self.header = header
        self.nrows = nrows
        self.df = pd.DataFrame()
        self.max_row = 0

    def readExcel(self) -> None:
        # Read Excel file
        if self.sheet_name:
            self.df = pd.read_excel(io=self.path, sheet_name=self.sheet_name, header=self.header, engine='openpyxl', nrows=self.nrows)
        else:
            self.df = pd.read_excel(io=self.path, engine='openpyxl', nrows=self.nrows)

        self.max_row = self.df.shape[0] + self.header
    
    def readCsv(self) -> None:
        # Read CSV file
        self.df = pd.read_csv(self.path, header=self.header, nrows=self.nrows)    
        self.max_row = self.df.shape[0] + self.header
    
    def getRowbyIndex(self, index: int) -> dict:
        if index > 0:
            arr = self.df.iloc[[index]].values.flatten().tolist()
            header = list(self.df)
            return dict(zip(header, arr))
        return {}
    
    def getDfColumn(self, columnName) -> list:
        df = self.getSheet()
        if columnName in list(df):
            return df[columnName].values.flatten().tolist()
        return []

    def searchDFFirstRowIndex(self, colName: str, searchVal: str) -> int:
        ls = self.df.index[self.df[colName]==searchVal].tolist()
        if len(ls) > 0:
            return ls[0]
        return -1
    
    def replaceOneRowByIndex(self, row_arr: list, index: int) -> None:
        self.df.loc[index] = row_arr


    def getSheet(self) -> pd.DataFrame:
        return self.df
    
    def getMaxRow(self) -> int:
        return self.max_row
    

    def appendOneRow(self, row_arr):
        # Append to the last row
        self.max_row = self.max_row + 1
        self.df.loc[self.max_row] = row_arr

    def writeLastRow(self):
        writer =  pd.ExcelWriter(path=self.path, engine='openpyxl', if_sheet_exists="overlay", mode="a")
        self.df.loc[len(self.df) - 1].to_excel(writer, 
                                    sheet_name=self.sheet_name,
                                    startrow = self.max_row + 1,
                                    index=False,
                                    header=False)
        writer.close()
    
    def writeExcel(self):
        writer =  pd.ExcelWriter(path=self.path, engine='openpyxl', if_sheet_exists="overlay", mode="a")
        self.df.to_excel(writer, 
                                    sheet_name=self.sheet_name,
                                    startrow = self.header,
                                    index=False,
                                    header=True)
        writer.close()

    def appendCSV(self):
        self.df.to_csv(path_or_buf=self.path, mode='a', index=False, header=False)