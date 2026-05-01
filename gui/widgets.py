import tkinter as tk

class SudokuCell(tk.Entry):
    def __init__(self, master, row,  col, **kwargs):
        super().__init__(master, **kwargs)
        self.row = row
        self.col = col

        self.config(
            width=2,
            font=('Arial', 18, 'bold'),
            justify='center',
            validate='key',
            # bg='lightellow',
            # relief='solid',
            # borderwidth=1
        )

        vcmd = (self.register(self._validate_input), '%P')
        self.config(validatecommand=vcmd)

    def _validate_input(self, P):
        if P == "":
            return True
        if P.isdigit() and len(P) == 1 and P in '132456789':
            return True
        return False
    
class SudokuBoard(tk.Frame):
    def __init__(self, master, **kwargs):
        # 繼承 Frame 的特性，並加上一點邊框
        super().__init__(master, bd=2, relief="solid", **kwargs)

        # 建立一個二維陣列來儲存 81 個 SudokuCell 物件
        self.cells = []

        for row in  range(9):
            row_cell = []
            for col in range(9):
                # 1. 實例化單一格子
                cell = SudokuCell(self, row = row, col = col)

                # 2. 視覺排版：製造 3x3 的區塊感
                # 如果是第 2 或第 5 個索引 (
                pad_x = (1,3) if col in (2,5) else (1,1)
                pad_y = (1,3) if row in (2,5) else (1,1)

                # 3. 使用 grid 排版系統將格子放上底板
                cell.grid(row = row, column=col, padx=pad_x, pady=pad_y)

                row_cell.append(cell)
            self.cells.append(row_cell)
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
                if val == '':
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
                self.cells[row][col].delete(0,tk.END)