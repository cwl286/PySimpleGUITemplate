import PySimpleGUI as sg
import pandas as pd
from typing import Callable

class GUI:
    def __init__(self) -> None:
        sg.theme('DarkAmber')   # Add a touch of color
        self.window = None
        self.tbl1 = pd.DataFrame()
        self.ascending = True

        self.addRow = None
        self.saveData = None

        self.menubar1 = ['Add Row',
                         '---',
                         'Exit'
                         ]
        self.menubar2 = ['Save',
                         ]

    def setTable1(self, df: pd.DataFrame) -> None:
        if not df.empty:
            self.tbl1 = df

    def setAddRow(self, func: Callable[[], None]) -> None:
        self.addRow = func

    
    def setSaveData(self, func: Callable[[], None]) -> None:
        self.saveData = func    

    def new_window(self, window: sg.Window) -> sg.Window:
        if window is not None:
            window.close()
        # Pass df to sg.table
        sg_tbl1 = self.parseDfToTable(self.tbl1)

        # custom menu bar
        tab1_layout = [[sg_tbl1]]
        
        layout = [
            [sg.MenubarCustom([
                ['Control',
                 self.menubar1],
                ['Save',
                 self.menubar2]
            ],
                k='-CUST MENUBAR-', p=0)],
            [sg.TabGroup(
                [[sg.Tab('Main', tab1_layout),
                  ]])]
        ]

        return sg.Window(title='Template GUI',
                         layout=layout, font=("Arial", 16))

    def display(self) -> None:

        # Init a Window
        self.window = self.new_window(None)

        # Event Loop to process "events" and get the "values" of the inputs
        while True:
            try:
                event, values = self.window.read()
                if event in (sg.WIN_CLOSED, 'Exit'):
                    break
                elif event in self.menubar1:
                    if event in 'Add Row':
                        self.tbl1 = self.addRow()
                elif event in self.menubar2:
                    if event in 'Save':
                        self.saveData()
                # to do update click a row
                elif '+CLICKED+' in event:
                    self.handleClick(event[0], event[2][0], event[2][1])
                else:
                    pass
            except Exception as e:
                sg.popup_error('Incorrect input', e, keep_on_top=True)
                self.window.close()

            self.updateWIndow()
        self.window.close()

    def updateWIndow(self) -> None:
        # update window
        self.window = self.new_window(self.window)

    def sortByColumn(self, df: pd.DataFrame, colName: str) -> pd.DataFrame:
        df.sort_values(colName)
        return df

    def handleClick(self, tableName, rowIndex: int, colIndex: int) -> None:
        if (rowIndex == -1):  # Sort headers
            match tableName:
                case '-TABLE-':
                    headers = list(self.tbl1)
                    self.tbl1[headers[colIndex]
                              ] = self.tbl1[headers[colIndex]].astype('str')
                    self.tbl1 = self.tbl1.sort_values(headers[colIndex], ascending=self.ascending)
                    self.ascending = not self.ascending
                case _:
                    pass

    # Parse a dataframe to table
    def parseDfToTable(self, df: pd.DataFrame) -> sg.Table:
        headers = []
        rows = []
        if not df.empty:
            headers = list(df)
            rows = df.values.tolist()
        tbl1 = sg.Table(values=rows, headings=headers,
                        auto_size_columns=True,
                        display_row_numbers=False,
                        justification='center', key='-TABLE-',
                        selected_row_colors='red on yellow',
                        enable_events=True,
                        expand_x=True,
                        expand_y=True,
                        enable_click_events=True,
                        select_mode=sg.TABLE_SELECT_MODE_BROWSE
                        )
        return tbl1
