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
from core.report_engine import ReportEngine

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
        self.report = ReportEngine()

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
        account = mt5.account_info()

        if account:

            self.report.print_account(
                login=account.login,
                server=account.server,
                balance=account.balance,
                equity=account.equity,
                leverage=f"1:{account.leverage}",
                company=getattr(account, "company", "-")
            )
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
        tick = mt5.symbol_info_tick("XAUUSD")

        if tick:

            spread = (tick.ask - tick.bid) * 100

            self.report.print_market(
                symbol="XAUUSD",
                timeframe="M5",
                bid=tick.bid,
                ask=tick.ask,
                spread=spread,
                candle_count=len(df)
        )

        # ==================================================
        # Hitung Indikator
        # ==================================================

        
        self.logger.info("Menghitung indikator...")

        indikator = self.indicator.calculate_all(df)

        self.report.print_indicators(

            ema13=indikator["EMA13"].iloc[-1],

            ema20=indikator["EMA20"].iloc[-1],

            ema50=indikator["EMA50"].iloc[-1],

            ema200=indikator["EMA200"].iloc[-1],

            rsi=indikator["RSI"].iloc[-1],

            macd=indikator["MACD"]["macd"].iloc[-1],

            atr=indikator["ATR"].iloc[-1],

            bb_upper=indikator["BB"]["upper"].iloc[-1],

            bb_middle=indikator["BB"]["middle"].iloc[-1],

            bb_lower=indikator["BB"]["lower"].iloc[-1],

            stoch_k=indikator["STOCH"]["k"].iloc[-1],

            stoch_d=indikator["STOCH"]["d"].iloc[-1]
        )

        # ==================================================
        # Signal Engine
        # ==================================================

        self.logger.info("Menganalisis Signal...")

        signal = self.signal.analyze(indikator)

        self.report.print_header()

        self.report.print_signal(
            trend=signal["trend"],
            momentum=signal["momentum"],
            volatility=signal["volatility"]
        )

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
                
        self.report.print_strategy(
            decision=strategy["decision"],
            zf_score=strategy["zf_score"],
            reasons=strategy["reason"]
        )

        for reason in strategy["reason"]:
            self.logger.info(reason)

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
        self.report.print_footer()
        self.logger.success("Analisis selesai.")

        self.mt5.disconnect()

        self.logger.info("MT5 Disconnect")