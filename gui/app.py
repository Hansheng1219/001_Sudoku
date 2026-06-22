# 專門用來存放「主視窗 (SudokuApp)」。
# 它的職責是把零件庫裡的盤面拿出來擺好，加上「解題」、「清空」等控制按鈕，並定義這些按鈕按下去會發生什麼事。

import tkinter as tk
from gui.widgets import SudokuBoard

import json
import os
import logging


class SudokuApp(tk.Tk):
    SAVE_FILE = "last_board.json"

    def __init__(
        self,
    ):
        super().__init__()
        self.logger = logging.getLogger("SudokuApp")

        # 設定主視窗的屬性
        self.title("Solvd Sodoku automatically")
        self.geometry("500x600")

        # 1. 實例化盤面 (從零件庫拿出來用)
        self.board = SudokuBoard(self)
        self.board.pack(pady=20)

        # 2. 建立控制按鈕區塊
        self._create_controls()
        self.load_last_puzzle()

    def load_last_puzzle(self):
        """啟動嘗試從檔案讀取上次的題目"""
        if os.path.exists(self.SAVE_FILE):
            try:
                with open(self.SAVE_FILE, "r") as f:
                    data = json.load(f)
                    self.board.set_board_data(data)
                self.logger.info("success to load the last data")
            except:
                self.logger.error("fail to load the data")

    def save_current_puzzle(self):
        """將目前盤面資料存入檔案"""
        data = self.board.get_board_data()
        try:
            with open(self.SAVE_FILE, "w") as f:
                json.dump(data, f)
            self.logger.info("already saved the board data")
        except Exception as e:
            self.logger.error(f"fail to save: {e}")

    def _create_controls(self):
        # 封裝方法：專門用來產生下方的按鈕群組

        # 建立一個 Frame 來把按鈕橫向排好
        control_frame = tk.Frame(self)
        control_frame.pack(pady=10)

        # 解題按鈕
        self.btn_solve = tk.Button(
            control_frame,
            text="Solving",
            font=("Arial", 14),
            bg="lightblue",
            command=self.on_solve_click,
        )
        self.btn_solve.grid(row=0, column=0, padx=10)

        # 清空按鈕 (目前先放著當裝飾，之後再實作功能)
        self.btn_clear = tk.Button(
            control_frame,
            text="clear the borard",
            font=("Arial", 14),
            command=self.on_clear_click,
        )
        self.btn_clear.grid(row=0, column=1, padx=10)

    # --- 以下是按鈕觸發的事件 (Event Handlers) ---

    def on_solve_click(self):
        """點擊解題按鈕時要執行的動作"""
        self.logger.info("User press, solving")
        self.save_current_puzzle()  # <--- 點擊 Solving 時自動存檔
        # 呼叫盤面交出資料

        current_data = self.board.get_board_data()
        from Core.model import SudokuModel

        model = SudokuModel(current_data)

        self.logger.info("---Starting to validate the current board---")
        is_all_pass = True
        for r in range(9):
            for c in range(9):
                val = current_data[r][c]

                if val != 0:
                    model.board_data[r][c] = 0
                    is_ok = model.is_valid(r, c, val)
                    model.board_data[r][c] = val

                    if not is_ok:
                        self.logger.error(f"{val} in ({r}:{c}) is not ok")
                        is_all_pass == False
        if is_all_pass:
            self.logger.info(f"---all number are ok---")
        else:
            self.logger.warning(f"---test fail: the number on the board is not ok---")

        updates = model.solve()
        if updates:
            for r, c, num in updates:
                target_cell = self.board.cells[r][c]

                target_cell.config(fg="blue")
                target_cell.delete(0, "end")
                target_cell.insert(0, str(num))

    def on_clear_click(self):
        """點擊清空按鈕時要執行的動作"""
        self.logger.info("User clear the board")
        self.board.clear_board()

        if os.path.exists(self.SAVE_FILE):
            os.remove(self.SAVE_FILE)
            self.logger.info("already clear the data")
