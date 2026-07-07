"""
========================================================
ZF AI TRADER
File    : logger.py
Folder  : core
Versi   : 0.1.0
Tanggal : 07 Juli 2026

Fungsi:
Mencatat seluruh aktivitas robot
ke terminal dan file log.

Dipanggil oleh:
- zf_master.py
- trade_executor.py
========================================================
"""

from pathlib import Path
from datetime import datetime


class ZFLogger:
    """
    Logger sederhana untuk ZF AI Trader.
    """

    def __init__(self):

        # Folder logs
        self.log_dir = Path("logs")
        self.log_dir.mkdir(exist_ok=True)

        # Nama file log per tanggal
        self.log_file = self.log_dir / (
            datetime.now().strftime("%Y-%m-%d") + ".log"
        )

    # ==================================================
    # Menulis log
    # ==================================================

    def write(self, level, message):

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        line = f"[{now}] {level.upper():<7} {message}"

        print(line)

        with open(
            self.log_file,
            "a",
            encoding="utf-8"
        ) as file:

            file.write(line + "\n")

    # ==================================================
    # INFO
    # ==================================================

    def info(self, message):

        self.write("INFO", message)

    # ==================================================
    # WARNING
    # ==================================================

    def warning(self, message):

        self.write("WARNING", message)

    # ==================================================
    # ERROR
    # ==================================================

    def error(self, message):

        self.write("ERROR", message)

    # ==================================================
    # SUCCESS
    # ==================================================

    def success(self, message):

        self.write("SUCCESS", message)