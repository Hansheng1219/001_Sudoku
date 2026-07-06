import tkinter as tk
from itertools import product


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
        )

        vcmd = (self.register(self._validate_input), "%P")
        self.config(validatecommand=vcmd)

    def _validate_input(self, value: str) -> bool:
        if value == "":
            return True
        return value.isdigit() and len(value) == 1 and value in "123456789"


class SudokuBoard(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(
            master, highlightbackground="black", highlightthickness=2, **kwargs
        )

        self.cells = [[None for _ in range(9)] for _ in range(9)]

        for block_row, block_col in product(range(3), range(3)):
            block_frame = tk.Frame(
                self, highlightbackground="black", highlightthickness=2, bd=0
            )
            block_frame.grid(row=block_row, column=block_col)

            for row_offset, col_offset in product(range(3), range(3)):
                actual_row = block_row * 3 + row_offset
                actual_col = block_col * 3 + col_offset

                cell = SudokuCell(block_frame, actual_row, actual_col)
                cell.grid(row=row_offset, column=col_offset)
                self.cells[actual_row][actual_col] = cell

                cell.bind(
                    "<Up>",
                    lambda event, r=actual_row, c=actual_col: self.move_focus(r - 1, c),
                )
                cell.bind(
                    "<Down>",
                    lambda event, r=actual_row, c=actual_col: self.move_focus(r + 1, c),
                )
                cell.bind(
                    "<Left>",
                    lambda event, r=actual_row, c=actual_col: self.move_focus(r, c - 1),
                )
                cell.bind(
                    "<Right>",
                    lambda event, r=actual_row, c=actual_col: self.move_focus(r, c + 1),
                )

    def get_board_data(self):
        data = []
        for row in range(9):
            row_data = [int(cell.get()) if cell.get() else 0 for cell in self.cells[row]]
            data.append(row_data)
        return data

    def clear_board(self):
        for row, col in product(range(9), range(9)):
            self.cells[row][col].delete(0, tk.END)
            self.cells[row][col].config(fg="black")

    def set_board_data(self, data):
        for row, col in product(range(9), range(9)):
            self.cells[row][col].delete(0, tk.END)
            value = data[row][col]
            if value != 0:
                self.cells[row][col].insert(0, str(value))

    def move_focus(self, row, col):
        new_r = max(0, min(8, row))
        new_c = max(0, min(8, col))

        target_cell = self.cells[new_r][new_c]
        target_cell.focus_set()