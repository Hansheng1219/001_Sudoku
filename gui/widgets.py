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