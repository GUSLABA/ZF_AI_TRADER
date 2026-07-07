"""
========================================================
ZF AI TRADER
File    : signal_engine.py
Folder  : core
Versi   : 0.1.0

Fungsi:
Membaca hasil indikator dan mengubahnya
menjadi sinyal teknikal.

Dipanggil oleh:
- zf_master.py
- strategy/zf_strategy.py

Menggunakan:
- indicator_engine.py
========================================================
"""


class SignalEngine:
    """
    Mesin pembaca sinyal teknikal.
    """

    def __init__(self):
        pass

    # ==================================================
    # Membaca Trend
    # ==================================================

    def detect_trend(self, ema13, ema20, ema50, ema200):

        if ema13 > ema20 > ema50 > ema200:
            return "STRONG_BULLISH"

        elif ema13 > ema20:
            return "BULLISH"

        elif ema13 < ema20 < ema50 < ema200:
            return "STRONG_BEARISH"

        elif ema13 < ema20:
            return "BEARISH"

        return "SIDEWAYS"

    # ==================================================
    # Membaca Momentum
    # ==================================================

    def detect_momentum(self, rsi):

        if rsi >= 70:
            return "OVERBOUGHT"

        elif rsi <= 30:
            return "OVERSOLD"

        elif rsi >= 55:
            return "BULLISH"

        elif rsi <= 45:
            return "BEARISH"

        return "NEUTRAL"

    # ==================================================
    # Membaca Volatilitas
    # ==================================================

    def detect_volatility(self, atr):

        if atr > 10:
            return "HIGH"

        elif atr > 5:
            return "MEDIUM"

        return "LOW"

    # ==================================================
    # Membaca Kondisi Lengkap
    # ==================================================

    def analyze(self, indicators):

        trend = self.detect_trend(
            indicators["EMA13"].iloc[-1],
            indicators["EMA20"].iloc[-1],
            indicators["EMA50"].iloc[-1],
            indicators["EMA200"].iloc[-1],
        )

        momentum = self.detect_momentum(
            indicators["RSI"].iloc[-1]
        )

        volatility = self.detect_volatility(
            indicators["ATR"].iloc[-1]
        )

        return {
            "trend": trend,
            "momentum": momentum,
            "volatility": volatility
        }