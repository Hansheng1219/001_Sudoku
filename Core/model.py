# 儲存狀態：接收並儲存從前端（GUI）傳來的 9x9 二維陣列資料。
# 規則驗證：判斷某個數字填入某個座標時，是否符合數獨的規則（檢查該行、該列、該九宮格有沒有重複的數字）。
# 演算法解題：負責執行「回溯法 (Backtracking)」演算法，自動推算出正確的數獨解答。

import logging



class SudokuModel:
    def __init__(self, board_data):
        self.board_data = board_data
        # 2. 為這個類別建立專屬的 logger
        self.logger = logging.getLogger("SudokuModel")
        self.logger.info('==SudokuModel already initialized, receiving the data on the board')

    def is_valid(self, row, col, num):
        """檢查將數字 num 放入 (row, col) 是否合法"""
        self.logger.debug(f"cheching rule: trying to put the number {num} in the point({row},{col})")
        

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
    
    def solve(self):
        """回溯法解題核心"""
        self.logger.info('start the backtracking solving algorithm')
        
        # 這裡未來會寫入遞迴邏輯
        # 假設我們在某一步遇到死胡同要退回：
        # self.logger.debug(f"⚠️ 遇到死胡同，進行回溯 (Backtrack) 從座標 ({row}, {col}) 退回")

        return True
    
if __name__ == "__main__":
    # 1. 建立一個假的 9x9 數獨盤面（用 0 代表空白格子）
    # 這裡我們用簡單的串列推導式生成一個 9x9 的全 0 陣列
    dummy_board = [[0 for _ in range(9)] for _ in range(9)]

    # 2. 實例化大腦模型
    model = SudokuModel(dummy_board)

    # 3. 呼叫方法來觸發 Logging 紀錄
    model.is_valid(0,5,5)
    model.solve()

    print("Inside testing already done, please check the log file")