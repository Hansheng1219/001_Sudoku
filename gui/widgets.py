import tkinter as tk


class SudokuCell(tk.Entry):
    def __init__(self, master, row, col, **kwargs):
        super().__init__(master, **kwargs)
        self.row = row
        self.col = col

        self.config(
            width=2,
            font=("Arial", 18, "bold"),
            justify="center",
            validate="key",
            # bg='lightellow',
            # relief='solid',
            # borderwidth=1
        )

        vcmd = (self.register(self._validate_input), "%P")
        self.config(validatecommand=vcmd)

    def _validate_input(self, P):
        if P == "":
            return True
        if P.isdigit() and len(P) == 1 and P in "132456789":
            return True
        return False


class SudokuBoard(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(
            master, highlightbackground="black", highlightthickness=2, **kwargs
        )

        # 建立一個二維陣列來儲存 81 個 SudokuCell 物件
        self.cells = [[None for _ in range(9)] for _ in range(9)]

        # --- 四層迴圈邏輯 ---
        # b_row, b_col 代表 3x3 個「大區塊」的座標 (0~2)
        for b_row in range(3):
            for b_col in range(3):
                # 1. 建立一個 3x3 的大區塊容器
                # highlightbackground="black" 設定外框顏色
                # highlightthickness=2 設定外框粗細 (這就是你要的粗線)

                block_frame = tk.Frame(
                    self, highlightbackground="black", highlightthickness=2, bd=0
                )
                block_frame.grid(row=b_row, column=b_col)

                # row, col 代表該區塊內「小格子」的相對座標 (0~2)
                for r in range(3):
                    for c in range(3):
                        # 2. 計算這格在 9x9 盤面上的「絕對座標」
                        actual_row = b_row * 3 + r
                        actula_col = b_col * 3 + c

                        # 3. 建立格子，注意！master 要設為 block_frame 而非 self
                        cell = SudokuCell(block_frame, actual_row, actula_col)
                        cell.grid(row=r, column=c)

                        # 4. 依然存入 9x9 陣列中，確保 get/set_board_data 功能不受影響
                        self.cells[actual_row][actula_col] = cell

            # self.cells.append(row_cell)

    def get_board_data(self):
        """
        封裝方法：讀取介面上所有的數字，回傳給未來的邏輯層使用。
        空白的格子會轉換為 0。
        """
        data = []
        for row in range(9):
            row_data = []
            for col in range(9):
                # 呼叫 tk.Entry 內建的 get() 方法來取得輸入框內容
                val = self.cells[row][col].get()
                if val == "":
                    row_data.append(0)
                else:
                    row_data.append(int(val))
            data.append(row_data)
        return data

    def clear_board(self):
        for row in range(9):
            for col in range(9):
                # 使用 Tkinter Entry 內建的 delete 方法
                # 0 代表從第一個字元開始，tk.END 代表到最後一個字元
                self.cells[row][col].delete(0, tk.END)

    def set_board_data(self, data):
        """將二維陣列的資料填入介面中的格子中"""
        for r in range(9):
            for c in range(9):
                self.cells[r][c].delete(0, tk.END)
                val = data[r][c]
                if val != 0:
                    self.cells[r][c].insert(0, str(val))
