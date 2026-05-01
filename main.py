import tkinter as tk
from gui.widgets import SudokuCell

def test_cell():
    root = tk.Tk()
    root.title('test mission 1')
    root.geometry('200x200')

    cell = SudokuCell(root, row=0, col=0)
    cell.pack(padx=50)

    print(f'Cell 座標設定成功 ({cell.row}, {cell.col})')

    root.mainloop()

if __name__ == "__main__":
    test_cell()