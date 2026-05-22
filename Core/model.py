# 儲存狀態：接收並儲存從前端（GUI）傳來的 9x9 二維陣列資料。
# 規則驗證：判斷某個數字填入某個座標時，是否符合數獨的規則（檢查該行、該列、該九宮格有沒有重複的數字）。
# 演算法解題：負責執行「回溯法 (Backtracking)」演算法，自動推算出正確的數獨解答。

import logging
from itertools import product



class SudokuModel:
    def __init__(self, board_data):
        self.board_data = board_data
        # 2. 為這個類別建立專屬的 logger
        self.logger = logging.getLogger("SudokuModel")
        self.logger.info('==SudokuModel already initialized, receiving the data on the board')

    def is_valid(self, row, col, num):
        """檢查將數字 num 放入 (row, col) 是否合法"""
        if any(self.board_data[r][col] == num for r in range(9)):
            self.logger.error("find the same number in the column")
            return False
        if any(self.board_data[row][c] == num for c in range(9)):
            self.logger.error("find the same number in the row")
            return False
        b_row, b_col = (row // 3) * 3, (col // 3) * 3
        if any(self.board_data[r][c] == num 
                for r in range(b_row, b_row + 3) 
                for c in range(b_col, b_col + 3)):
            self.logger.error(f"Found the same number {num} in the 3x3 area starting at ({b_row}, {b_col})")
            return False
        
        return True
        
    def init_pencil_marks(self):
        """將候選數字放入筆記中"""
        self.logger.info(f"---start to mark the numbers---")
        self.pencil_marks = [[set() for _ in range(9)] for _ in range(9)]
        FULL_SET = {1, 2, 3, 4, 5, 6, 7, 8, 9}

        for r, c in product(range(9), range(9)):
            if self.board_data[r][c] == 0:
                # 取得同行、同列、同九宮格「已經存在」的數字集合 (假設您有寫這些輔助函數)
                used_nums = self.get_used_num(r,c)
                
                # 使用集合的差集 (-) 運算：全集合 減去 已使用的數字 = 剩下的候選數
                self.pencil_marks[r][c] = FULL_SET - used_nums
                self.logger.info(f"{self.pencil_marks[r][c]} mark in ({r + 1},{c + 1})")
        self.logger.info(f"---End of mark the numbers---")

    def get_used_num(self, row, col):
        used_row_nums = {num for num in self.board_data[row][:] if num != 0}
        used_col_nums = {self.board_data[r][col] for r in range(9) if self.board_data[r][col] != 0}
        b_row, b_col = (row // 3) * 3, (col // 3) * 3
        used_box_nums = {
            self.board_data[r][c] 
            for r in range(b_row, b_row + 3) 
            for c in range(b_col, b_col + 3) 
            if self.board_data[r][c] != 0
        }
        used_nums = used_row_nums | used_col_nums | used_box_nums

        return used_nums
    
    def fill_naked_singles(self):
        updates = []

        for r, c in product(range(9), range(9)):
            if len(self.pencil_marks[r][c]) == 1:
                num = self.pencil_marks[r][c].pop()
                self.board_data[r][c] = num
                updates.append((r, c, num))
        
        return updates
                
    # def eliminate_naked_subset(self, subsize: int) -> None:
        
    
    def solve(self):
        self.logger.info('start to solve the sodoku')
        all_updates = []
        while True:
            self.init_pencil_marks()
            updates = self.fill_naked_singles()
            if not updates:
                self.logger.info("Logic phase ended. No new updates")
                break
            all_updates.extend(updates)

        # for r, c in product(range(9), range(9)):
        #     if self.pencil_marks[r][c]:
        #         self.logger.info(f"{(r + 1,c + 1)} have {self.pencil_marks[r][c]}")

        

        # 這裡未來會寫入遞迴邏輯
        # 假設我們在某一步遇到死胡同要退回：
        # self.logger.debug(f"⚠️ 遇到死胡同，進行回溯 (Backtrack) 從座標 ({row}, {col}) 退回")

        return all_updates