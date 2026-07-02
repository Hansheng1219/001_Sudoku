# 儲存狀態：接收並儲存從前端（GUI）傳來的 9x9 二維陣列資料。
# 規則驗證：判斷某個數字填入某個座標時，是否符合數獨的規則（檢查該行、該列、該九宮格有沒有重複的數字）。
# 演算法解題：負責執行「回溯法 (Backtracking)」演算法，自動推算出正確的數獨解答。

import logging
from itertools import product, combinations
import copy


class SudokuModel:
    def __init__(self, board_data):
        self.board_data = board_data
        self.logger = logging.getLogger("SudokuModel")
        self.logger.info(
            "==SudokuModel already initialized, receiving the data on the board"
        )

    def is_valid(self, row, col, num):
        """檢查將數字 num 放入 (row, col) 是否合法"""
        if any(self.board_data[r][col] == num for r in range(9)):
            self.logger.error("find the same number in the column")
            return False
        if any(self.board_data[row][c] == num for c in range(9)):
            self.logger.error("find the same number in the row")
            return False
        b_row, b_col = (row // 3) * 3, (col // 3) * 3
        if any(
            self.board_data[r][c] == num
            for r in range(b_row, b_row + 3)
            for c in range(b_col, b_col + 3)
        ):
            self.logger.error(
                f"Found the same number {num} in the 3x3 area starting at ({b_row}, {b_col})"
            )
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
                used_nums = self.get_used_num(r, c)

                # 使用集合的差集 (-) 運算：全集合 減去 已使用的數字 = 剩下的候選數
                self.pencil_marks[r][c] = FULL_SET - used_nums
                self.logger.info(f"{self.pencil_marks[r][c]} mark in ({r + 1},{c + 1})")
        self.logger.info(f"---End of mark the numbers---")

    def delete_pencil_marks(self, updates) -> None:
        for row, col, num in updates:
            for r in range(9):
                if self.board_data[r][col] == 0:
                    self.pencil_marks[r][col].discard(num)
            for c in range(9):
                if self.board_data[row][c] == 0:
                    self.pencil_marks[row][c].discard(num)
            b_row, b_col = (row // 3) * 3, (col // 3) * 3
            for r, c in product(range(b_row,b_row + 3), range(b_col, b_col + 3)):
                if self.board_data[r][c] == 0:
                    self.pencil_marks[r][c].discard(num)


    def get_used_num(self, row, col):
        used_row_nums = {num for num in self.board_data[row][:] if num != 0}
        used_col_nums = {
            self.board_data[r][col] for r in range(9) if self.board_data[r][col] != 0
        }
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

    def fill_hidden_singles_in_blocks(self) -> list[tuple[int, int, int]]:
        update = []
        for b_row, b_col in product(range(3), range(3)):
            start_r = b_row * 3
            start_c = b_col * 3
            for num in range(1, 10):
                cell_with_num = [
                    (start_r + r, start_c + c)
                    for r in range(3)
                    for c in range(3)
                    if num in self.pencil_marks[start_r + r][start_c + c]
                ]
                if len(cell_with_num) == 1:
                    target_r, target_c = cell_with_num[0]
                    self.board_data[target_r][target_c] = num
                    self.pencil_marks[target_r][target_c].clear()

                    update.append((target_r, target_c, num))
                    # self.logger.info(
                    #     f"put the {num} in ({target_r + 1},{target_c})"
                    # )
        return update
        

    def fill_hidden_singles_in_rows(self) -> list[tuple[int, int, int]]:
        update = []
        for row, num in product(range(9), range(1, 10)):
            cell_with_num = [
                (row, col) for col in range(9)
                if num in self.pencil_marks[row][col]
            ]
            if len(cell_with_num) == 1:
                target_r, target_c = cell_with_num[0]
                self.board_data[target_r][target_c] = num
                self.pencil_marks[target_r][target_c].clear()
                update.append((target_r, target_c, num))
        return update

    def fill_hidden_singles_in_cols(self) -> list[tuple[int, int, int]]:
        update = []
        for col, num in product(range(9), range(1, 10)):
            cell_with_num = [
                (row, col) for row in range(9)
                if num in self.pencil_marks[row][col]
            ]
            if len(cell_with_num) == 1:
                target_r, target_c = cell_with_num[0]
                self.board_data[target_r][target_c] = num
                self.pencil_marks[target_r][target_c].clear()
                update.append((target_r, target_c, num))
        return update
    
    def apply_hypothesis(self) -> list[tuple[int, int, int]]:
        min_candidates_len = 1
        target_r, target_c = -1, -1

        while min_candidates_len < 10:
            for r, c in product(range(9), range(9)):
                if self.board_data[r][c] == 0 and len(self.pencil_marks[r][c]) == min_candidates_len:
                        target_r, target_c = r, c
                        break
            if target_r != -1:
                break
            min_candidates_len += 1
        candidates = list(self.pencil_marks[target_r][target_c])

        for guess_num in candidates:
            sendbox_board = copy.deepcopy(self.board_data)
            sendbox_board[target_r][target_c] = guess_num

            clone = SudokuModel(sendbox_board)
            update = clone.solve()
            

            if clone.is_solved():
                update_guess = (target_r, target_c, guess_num)
                update.append(update_guess)
                self.board_data = clone.board_data
                return update
            
            
        return []

    def is_solved(self) -> bool:
        for r, c in product(range(9), range(9)):
            if (current_num := self.board_data[r][c]) != 0:
                self.board_data[r][c] = 0
                is_ok = self.is_valid(r, c, current_num)
                self.board_data[r][c] = current_num
                if not is_ok: return is_ok
            if self.board_data[r][c] == 0 and self.pencil_marks[r][c] == set():
                return False
        return True          

    def solve(self):
        self.logger.info("start to solve the sodoku")
        all_updates = []
        self.init_pencil_marks()
        while True:
            updates = self.fill_naked_singles()
            if updates:
                self.delete_pencil_marks(updates)
                all_updates.extend(updates)
                continue

            updates = self.fill_hidden_singles_in_blocks()
            if updates:
                self.delete_pencil_marks(updates)
                all_updates.extend(updates)
                continue

            updates = self.fill_hidden_singles_in_rows()
            if updates:
                self.delete_pencil_marks(updates)
                all_updates.extend(updates)
                continue

            updates = self.fill_hidden_singles_in_cols()
            if updates:
                self.delete_pencil_marks(updates)
                all_updates.extend(updates)
                continue
            

            self.logger.info("Logic phase ended. No new updates")
            break
        all_updates.extend(updates)
        return all_updates