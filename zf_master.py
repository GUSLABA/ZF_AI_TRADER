"""
========================================================
ZF AI TRADER
File    : zf_master.py
Folder  : Root Project
Versi   : 0.1.6
Tanggal : 07 Juli 2026

Fungsi:
Mengatur seluruh alur kerja robot trading.

Dipanggil oleh:
- main.py

Menggunakan:
- core.mt5_connector
- core.data_loader
- core.indicator_engine
- core.signal_engine
- core.trade_executor
- core.logger
- strategy.zf_strategy
========================================================
"""

import MetaTrader5 as mt5

from core.mt5_connector import MT5Connector
from core.data_loader import DataLoader
from core.indicator_engine import IndicatorEngine
from core.signal_engine import SignalEngine
from core.trade_executor import TradeExecutor
from core.logger import ZFLogger

from strategy.zf_strategy import ZFStrategy


class ZFMaster:
    """
    Master Controller ZF AI Trader
    """

    def __init__(self):

        print("\n========================================")
        print("          ZF AI TRADER")
        print("========================================\n")

        self.logger = ZFLogger()

        self.mt5 = MT5Connector()
        self.loader = DataLoader()
        self.indicator = IndicatorEngine()
        self.signal = SignalEngine()
        self.strategy = ZFStrategy()
        self.executor = TradeExecutor()

    # ==================================================
    # Menjalankan Robot
    # ==================================================

    def run(self):

        self.logger.info("Memulai sistem...")

        # ==================================================
        # Koneksi MT5
        # ==================================================

        if not self.mt5.connect():
            self.logger.error("Robot dihentikan.")
            return

        self.logger.success("Koneksi MT5 berhasil.")

        # ==================================================
        # Ambil Data Market
        # ==================================================

        self.logger.info("Mengambil data M5...")

        df = self.loader.get_candles(
            mt5.TIMEFRAME_M5,
            500
        )

        if df is None:
            self.logger.error("Data market gagal diambil.")
            self.mt5.disconnect()
            return

        self.logger.success(f"Jumlah Candle : {len(df)}")

        # ==================================================
        # Hitung Indikator
        # ==================================================

        self.logger.info("Menghitung indikator...")

        indikator = self.indicator.calculate_all(df)

        self.logger.success("EMA13  : OK")
        self.logger.success("EMA20  : OK")
        self.logger.success("EMA50  : OK")
        self.logger.success("EMA200 : OK")
        self.logger.success("RSI    : OK")
        self.logger.success("MACD   : OK")
        self.logger.success("ATR    : OK")
        self.logger.success("BB     : OK")
        self.logger.success("STOCH  : OK")

        # ==================================================
        # Signal Engine
        # ==================================================

        self.logger.info("Menganalisis Signal...")

        signal = self.signal.analyze(indikator)

        print("\n========================================")
        print("SIGNAL ANALYSIS")
        print("========================================")
        print(f"Trend      : {signal['trend']}")
        print(f"Momentum   : {signal['momentum']}")
        print(f"Volatility : {signal['volatility']}")
        print("========================================")

        self.logger.info(
            f"Signal -> Trend={signal['trend']} | "
            f"Momentum={signal['momentum']} | "
            f"Volatility={signal['volatility']}"
        )

        # ==================================================
        # ZF Strategy
        # ==================================================

        self.logger.info("Menjalankan ZF Strategy...")

        strategy = self.strategy.analyze(signal)

        print("\n========================================")
        print("ZF STRATEGY")
        print("========================================")
        print(f"Decision : {strategy['decision']}")
        print(f"ZF Score : {strategy['zf_score']}")

        print("\nReason :")

        for reason in strategy["reason"]:
            print(f"✓ {reason}")
            self.logger.info(reason)

        print("========================================")

        self.logger.success(
            f"Decision={strategy['decision']} | "
            f"ZF Score={strategy['zf_score']}"
        )

        # ==================================================
        # Trade Executor
        # ==================================================

        self.logger.info("Menjalankan Trade Executor...")

        if strategy["decision"] == "BUY":

            self.executor.execute_buy(
                lot=0.01,
                sl=0.0,
                tp=0.0
            )

        elif strategy["decision"] == "SELL":

            self.executor.execute_sell(
                lot=0.01,
                sl=0.0,
                tp=0.0
            )

        else:

            self.logger.warning("Decision = WAIT")

        # ==================================================
        # Selesai
        # ==================================================

        self.logger.success("Analisis selesai.")

        self.mt5.disconnect()

        self.logger.info("MT5 Disconnect")