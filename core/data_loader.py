"""
========================================================
ZF AI TRADER
File    : data_loader.py
Folder  : core
Versi   : 0.1.0

Fungsi:
Mengambil data market dari MetaTrader 5.

Dipanggil oleh:
- zf_master.py
- indicator_engine.py

Menggunakan:
- MetaTrader5
- config.symbols
========================================================
"""

import MetaTrader5 as mt5
import pandas as pd

from config.symbols import SYMBOL


class DataLoader:
    """
    Class untuk mengambil data market dari MT5.
    """

    def __init__(self):
        pass

    # =====================================================
    # Mengambil data candle
    # =====================================================

    def get_candles(self, timeframe, candle_count):
        """
        Mengambil data candle.

        Parameter:
            timeframe     : MT5.TIMEFRAME_M5 dll
            candle_count  : jumlah candle

        Return:
            pandas.DataFrame
        """

        rates = mt5.copy_rates_from_pos(
            SYMBOL,
            timeframe,
            0,
            candle_count
        )

        if rates is None:
            print("❌ Gagal mengambil data candle.")
            return None

        df = pd.DataFrame(rates)

        df["time"] = pd.to_datetime(
            df["time"],
            unit="s"
        )

        return df

    # =====================================================
    # Harga Bid
    # =====================================================

    def get_bid(self):

        tick = mt5.symbol_info_tick(SYMBOL)

        if tick is None:
            return None

        return tick.bid

    # =====================================================
    # Harga Ask
    # =====================================================

    def get_ask(self):

        tick = mt5.symbol_info_tick(SYMBOL)

        if tick is None:
            return None

        return tick.ask

    # =====================================================
    # Spread
    # =====================================================

    def get_spread(self):

        tick = mt5.symbol_info_tick(SYMBOL)

        if tick is None:
            return None

        return tick.ask - tick.bid

    # =====================================================
    # Informasi Symbol
    # =====================================================

    def get_symbol_info(self):

        return mt5.symbol_info(SYMBOL)

    # =====================================================
    # Tick Terbaru
    # =====================================================

    def get_tick(self):

        return mt5.symbol_info_tick(SYMBOL)