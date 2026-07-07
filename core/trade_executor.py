"""
========================================================
ZF AI TRADER
File    : trade_executor.py
Folder  : core
Versi   : 0.1.1
Tanggal : 07 Juli 2026

Fungsi:
Melakukan eksekusi order ke MetaTrader 5.

Dipanggil oleh:
- zf_master.py

Menggunakan:
- config.symbols
- core.logger
========================================================
"""

import MetaTrader5 as mt5

from config.symbols import SYMBOL
from core.logger import ZFLogger


class TradeExecutor:
    """
    Kelas eksekusi order MT5.
    """

    def __init__(self):

        self.symbol = SYMBOL
        self.logger = ZFLogger()

    # ==================================================
    # Mengecek apakah simbol tersedia
    # ==================================================

    def check_symbol(self):

        info = mt5.symbol_info(self.symbol)

        if info is None:

            self.logger.error(
                f"Symbol {self.symbol} tidak ditemukan."
            )

            return False

        if not info.visible:

            mt5.symbol_select(self.symbol, True)

            self.logger.info(
                f"Symbol {self.symbol} diaktifkan."
            )

        return True

    # ==================================================
    # Mengecek posisi terbuka
    # ==================================================

    def has_open_position(self):

        positions = mt5.positions_get(symbol=self.symbol)

        if positions is None:
            return False

        return len(positions) > 0

    # ==================================================
    # BUY
    # ==================================================

    def execute_buy(self, lot, sl, tp):

        self.logger.info("========================================")
        self.logger.info("TRADE EXECUTOR")
        self.logger.info("========================================")

        if not self.check_symbol():
            return False

        if self.has_open_position():

            self.logger.warning(
                "Masih ada posisi BUY/SELL yang terbuka."
            )

            return False

        self.logger.success("BUY REQUEST")

        self.logger.info(f"Symbol : {self.symbol}")
        self.logger.info(f"Lot    : {lot}")
        self.logger.info(f"SL     : {sl}")
        self.logger.info(f"TP     : {tp}")

        self.logger.warning("MODE TEST")

        self.logger.info(
            "Order belum dikirim ke broker."
        )

        self.logger.info("========================================")

        return True

    # ==================================================
    # SELL
    # ==================================================

    def execute_sell(self, lot, sl, tp):

        self.logger.info("========================================")
        self.logger.info("TRADE EXECUTOR")
        self.logger.info("========================================")

        if not self.check_symbol():
            return False

        if self.has_open_position():

            self.logger.warning(
                "Masih ada posisi BUY/SELL yang terbuka."
            )

            return False

        self.logger.success("SELL REQUEST")

        self.logger.info(f"Symbol : {self.symbol}")
        self.logger.info(f"Lot    : {lot}")
        self.logger.info(f"SL     : {sl}")
        self.logger.info(f"TP     : {tp}")

        self.logger.warning("MODE TEST")

        self.logger.info(
            "Order belum dikirim ke broker."
        )

        self.logger.info("========================================")

        return True

    # ==================================================
    # Menampilkan posisi terbuka
    # ==================================================

    def show_positions(self):

        positions = mt5.positions_get(symbol=self.symbol)

        if positions is None:

            self.logger.info("Tidak ada posisi terbuka.")

            return

        self.logger.info("========================================")
        self.logger.info("OPEN POSITIONS")
        self.logger.info("========================================")

        for pos in positions:

            self.logger.info(
                f"Ticket={pos.ticket} | "
                f"Lot={pos.volume} | "
                f"Profit={pos.profit}"
            )

        self.logger.info("========================================")

    # ==================================================
    # Menutup semua posisi
    # ==================================================

    def close_all_positions(self):

        self.logger.warning(
            "Fitur close_all_positions() belum dibuat."
        )