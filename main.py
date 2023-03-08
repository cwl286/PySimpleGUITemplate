from src.Controller import Controller
from src.GUI import GUI

def main():
    con = Controller()

    # Init GUI
    gui = GUI()
    gui.setTable1(con.getData())

    gui.setAddRow(con.addRow)
    
    gui.setSaveData(con.SaveData)

    gui.display() 

if __name__ == "__main__": 
    main()