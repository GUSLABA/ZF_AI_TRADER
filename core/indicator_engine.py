"""
========================================================
ZF AI TRADER
File    : indicator_engine.py
Folder  : core
Versi   : 0.1.0

Fungsi:
Menghitung seluruh indikator teknikal
yang dibutuhkan oleh strategi ZF.

Dipanggil oleh:
- zf_master.py
- zf_strategy.py

Menggunakan:
- pandas
- ta
========================================================
"""

import pandas as pd

from ta.trend import EMAIndicator
from ta.trend import SMAIndicator
from ta.trend import MACD

from ta.momentum import RSIIndicator
from ta.momentum import StochasticOscillator

from ta.volatility import AverageTrueRange
from ta.volatility import BollingerBands


class IndicatorEngine:
    """
    Mesin perhitungan indikator.
    """

    def __init__(self):
        pass

    # ==================================================
    # EMA
    # ==================================================

    def ema(self, close, period):

        ema = EMAIndicator(
            close=close,
            window=period
        )

        return ema.ema_indicator()

    # ==================================================
    # SMA
    # ==================================================

    def sma(self, close, period):

        sma = SMAIndicator(
            close=close,
            window=period
        )

        return sma.sma_indicator()

    # ==================================================
    # RSI
    # ==================================================

    def rsi(self, close, period=14):

        rsi = RSIIndicator(
            close=close,
            window=period
        )

        return rsi.rsi()

    # ==================================================
    # MACD
    # ==================================================

    def macd(self, close):

        macd = MACD(close)

        return {
            "macd": macd.macd(),
            "signal": macd.macd_signal(),
            "histogram": macd.macd_diff()
        }

    # ==================================================
    # ATR
    # ==================================================

    def atr(self, high, low, close, period=14):

        atr = AverageTrueRange(
            high,
            low,
            close,
            window=period
        )

        return atr.average_true_range()

    # ==================================================
    # Bollinger Bands
    # ==================================================

    def bollinger(self, close, period=20):

        bb = BollingerBands(
            close=close,
            window=period
        )

        return {
            "upper": bb.bollinger_hband(),
            "middle": bb.bollinger_mavg(),
            "lower": bb.bollinger_lband()
        }

    # ==================================================
    # Stochastic
    # ==================================================

    def stochastic(self, high, low, close):

        stoch = StochasticOscillator(
            high,
            low,
            close
        )

        return {
            "k": stoch.stoch(),
            "d": stoch.stoch_signal()
        }

    # ==================================================
    # Menghitung seluruh indikator
    # ==================================================

    def calculate_all(self, df: pd.DataFrame):

        result = {}

        result["EMA13"] = self.ema(df["close"], 13)
        result["EMA20"] = self.ema(df["close"], 20)
        result["EMA50"] = self.ema(df["close"], 50)
        result["EMA200"] = self.ema(df["close"], 200)

        result["RSI"] = self.rsi(df["close"])

        result["MACD"] = self.macd(df["close"])

        result["ATR"] = self.atr(
            df["high"],
            df["low"],
            df["close"]
        )

        result["BB"] = self.bollinger(df["close"])

        result["STOCH"] = self.stochastic(
            df["high"],
            df["low"],
            df["close"]
        )

        return result