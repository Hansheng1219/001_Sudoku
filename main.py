import logging
from datetime import datetime
from pathlib import Path

from gui.app import SudokuApp


def configure_logging() -> None:
    """由主流程統一設定日誌，避免在不同模組中重複初始化。"""
    base_dir = Path(__file__).resolve().parent
    log_dir = base_dir / "logs"
    log_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = log_dir / f"sudoku_{timestamp}.log"

    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )

    file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.addHandler(file_handler)

    logging.getLogger(__name__).info("Logging initialized at %s", log_file)


def main() -> int:
    """應用程式進入點，統一負責初始化與啟動。"""
    configure_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting Sudoku application")

    app = SudokuApp()
    app.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())