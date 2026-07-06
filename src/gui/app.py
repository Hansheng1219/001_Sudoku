# 專門用來存放「主視窗 (SudokuApp)」。
# 它的職責是把零件庫裡的盤面拿出來擺好，加上「解題」、「清空」等控制按鈕，並定義這些按鈕按下去會發生什麼事。

import json
import logging
from itertools import product
from pathlib import Path
import tkinter as tk

from Core.model import SudokuModel
from gui.widgets import SudokuBoard


class SudokuApp(tk.Tk):
    SAVE_FILE = Path(__file__).resolve().parent.parent / "last_board.json"

    def __init__(self):
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

    def _is_valid_board_data(self, data) -> bool:
        return (
            isinstance(data, list)
            and len(data) == 9
            and all(isinstance(row, list) and len(row) == 9 for row in data)
        )

    def load_last_puzzle(self) -> None:
        """啟動時嘗試從檔案讀取上次的題目。"""
        if not self.SAVE_FILE.exists():
            return

        try:
            with self.SAVE_FILE.open("r", encoding="utf-8") as handle:
                data = json.load(handle)

            if self._is_valid_board_data(data):
                self.board.set_board_data(data)
                self.logger.info("Loaded the last saved board")
            else:
                self.logger.warning("Saved board data format is invalid; skipped loading")
        except (OSError, json.JSONDecodeError, TypeError, ValueError) as exc:
            self.logger.exception("Failed to load saved board data: %s", exc)

    def save_current_puzzle(self) -> None:
        """將目前盤面資料存入檔案。"""
        data = self.board.get_board_data()
        try:
            with self.SAVE_FILE.open("w", encoding="utf-8") as handle:
                json.dump(data, handle, indent=2)
            self.logger.info("Saved current board data")
        except OSError as exc:
            self.logger.exception("Failed to save board data: %s", exc)

    def _create_controls(self) -> None:
        # 封裝方法：專門用來產生下方的按鈕群組
        control_frame = tk.Frame(self)
        control_frame.pack(pady=10)

        self.btn_solve = tk.Button(
            control_frame,
            text="Solving",
            font=("Arial", 14),
            bg="lightblue",
            command=self.on_solve_click,
        )
        self.btn_solve.grid(row=0, column=0, padx=10)

        self.btn_clear = tk.Button(
            control_frame,
            text="clear the borard",
            font=("Arial", 14),
            command=self.on_clear_click,
        )
        self.btn_clear.grid(row=0, column=1, padx=10)

    def _apply_updates(self, updates) -> None:
        for row, col, num in updates:
            target_cell = self.board.cells[row][col]
            target_cell.config(fg="blue")
            target_cell.delete(0, tk.END)
            target_cell.insert(0, str(num))

    # --- 以下是按鈕觸發的事件 (Event Handlers) ---

    def on_solve_click(self) -> None:
        """點擊解題按鈕時要執行的動作。"""
        self.logger.info("User requested solving")
        self.save_current_puzzle()
        current_data = self.board.get_board_data()

        model = SudokuModel(current_data)
        self.logger.info("Starting validation of the current board")
        is_all_pass = True
        invalid_positions = []
        for row, col in product(range(9), range(9)):
            value = current_data[row][col]
            if value != 0:
                model.board_data[row][col] = 0
                is_ok = model.is_valid(row, col, value)
                model.board_data[row][col] = value
                if not is_ok:
                    invalid_positions.append((row, col, value))
                    is_all_pass = False

        if is_all_pass:
            self.logger.info("All numbers on the board are valid")
        else:
            self.logger.warning(
                "Board validation found %s invalid placement(s)",
                len(invalid_positions),
            )

        updates = model.solve()
        if updates:
            self.logger.info("Solver produced %s updates", len(updates))
            self._apply_updates(updates)
        else:
            self.logger.warning("Solver produced no updates; the board may already be solved or unsolved")

    def on_clear_click(self) -> None:
        """點擊清空按鈕時要執行的動作。"""
        self.logger.info("User cleared the board")
        self.board.clear_board()
        if self.SAVE_FILE.exists():
            self.SAVE_FILE.unlink()
            self.logger.info("Removed saved board data")
        else:
            self.logger.debug("No saved board data to remove")