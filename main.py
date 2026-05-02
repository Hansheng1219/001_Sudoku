import tkinter as tk
from gui.widgets import SudokuCell, SudokuBoard
from gui.app import SudokuApp

import logging

# 1. 設定日誌基礎配置 (只會執行一次)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    datefmt='%H:%M:%S',
    filename='sudoku_debug.log',
    filemode='w'
)

def test_cell():
    root = tk.Tk()
    root.title('test mission 1')
    root.geometry('200x200')

    cell = SudokuCell(root, row=0, col=0)
    cell.pack(padx=50)

    print(f'Cell 座標設定成功 ({cell.row}, {cell.col})')

    root.mainloop()

def test_board():
    root = tk.Tk()
    root.title("test mission 2: Sudoku board")
    root.geometry("450x450")

    # 1. 實例化整個盤面，並放在視窗中間
    board = SudokuBoard(root)
    board.pack(pady=20)

    # 2. 測試用的按鈕事件：點擊時呼叫 board.get_board_data()
    def on_click_get_data():
        current_data = board.get_board_data()
        print("current data on the board")
        for row in current_data:
            print(row)
        print("==============\n")
    
    # 3. 建立一個按鈕來觸發抓取資料
    btn = tk.Button(root, text="print the data on the board", font=("Arial",14), command=on_click_get_data)
    btn.pack(pady=10)

    root.mainloop()
    

if __name__ == "__main__":
    app = SudokuApp()
    app.mainloop()