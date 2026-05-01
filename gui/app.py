# 專門用來存放「主視窗 (SudokuApp)」。
# 它的職責是把零件庫裡的盤面拿出來擺好，加上「解題」、「清空」等控制按鈕，並定義這些按鈕按下去會發生什麼事。

import tkinter as tk
from gui.widgets import SudokuBoard

class SudokuApp(tk.Tk):
    def __init__(self,):
        super().__init__()

        # 設定主視窗的屬性
        self.title("Solvd Sodoku automatically")
        self.geometry("500x600")

        # 1. 實例化盤面 (從零件庫拿出來用)
        self.board = SudokuBoard(self)
        self.board.pack(pady=20)

        # 2. 建立控制按鈕區塊
        self._create_controls()

    def _create_controls(self):
        #封裝方法：專門用來產生下方的按鈕群組

        # 建立一個 Frame 來把按鈕橫向排好
        control_frame = tk.Frame(self)
        control_frame.pack(pady=10)

        # 解題按鈕
        self.btn_solve = tk.Button(
            control_frame,
            text="Solving",
            font=("Arial", 14),
            bg="lightblue",
            command=self.on_solve_click
        )
        self.btn_solve.grid(row=0, column=0, padx=10)

        # 清空按鈕 (目前先放著當裝飾，之後再實作功能)
        self.btn_clear = tk.Button(
            control_frame,
            text="clear the borard",
            font=("Arial", 14),
            command=self.on_clear_click
        )
        self.btn_clear.grid(row=0, column=1, padx=10)

    # --- 以下是按鈕觸發的事件 (Event Handlers) ---

    def on_solve_click(self):
        """點擊解題按鈕時要執行的動作"""
        print("User press, solving")
        # 呼叫盤面交出資料

        current_data = self.board.get_board_data()
        for row in current_data:
            print(row)

    def on_clear_click(self):
        """點擊清空按鈕時要執行的動作"""
        print("User clear the board")
        # 這裡未來會呼叫 board 裡面的 clear() 方法