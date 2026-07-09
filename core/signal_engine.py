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

    def detect_momentum(
        self,
        rsi,
        macd,
        macd_signal
    ):

            # ------------------------------------------
            # Sangat bullish
            # ------------------------------------------

            if (
                rsi >= 65
                and macd > macd_signal
            ):

                return "BULLISH"

            # ------------------------------------------
            # Sangat bearish
            # ------------------------------------------

            elif (
                rsi <= 35
                and macd < macd_signal
            ):

                return "BEARISH"

            # ------------------------------------------
            # Overbought
            # ------------------------------------------

            elif rsi >= 75:

                return "OVERBOUGHT"

            # ------------------------------------------
            # Oversold
            # ------------------------------------------

            elif rsi <= 25:

                return "OVERSOLD"

            # ------------------------------------------
            # Bias bullish
            # ------------------------------------------

            elif (
                rsi >= 55
                and macd > 0
            ):

                return "BULLISH"

            # ------------------------------------------
            # Bias bearish
            # ------------------------------------------

            elif (
                rsi <= 45
                and macd < 0
            ):

                return "BEARISH"

            return "NEUTRAL"
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

            indicators["RSI"].iloc[-1],

            indicators["MACD"]["macd"].iloc[-1],

            indicators["MACD"]["signal"].iloc[-1]

        )

        volatility = self.detect_volatility(
            indicators["ATR"].iloc[-1]
        )

        return {

            # ------------------------------------------
            # HASIL ANALISIS
            # ------------------------------------------

             "trend": trend,

            "momentum": momentum,

             "volatility": volatility,

            # ------------------------------------------
            # LEVEL 1
            # EMA
            # ------------------------------------------

            "ema13": indicators["EMA13"].iloc[-1],

             "ema20": indicators["EMA20"].iloc[-1],

             "ema50": indicators["EMA50"].iloc[-1],

             "ema200": indicators["EMA200"].iloc[-1],

            # ------------------------------------------
            # LEVEL 2
            # RSI + MACD
            # ------------------------------------------

            "rsi": indicators["RSI"].iloc[-1],

            "macd": indicators["MACD"]["macd"].iloc[-1],

            "macd_signal": indicators["MACD"]["signal"].iloc[-1],

            # ------------------------------------------
            # LEVEL 3
            # ATR + BB + STOCH
            # ------------------------------------------

            "atr": indicators["ATR"].iloc[-1],

            "bb_upper": indicators["BB"]["upper"].iloc[-1],

            "bb_middle": indicators["BB"]["middle"].iloc[-1],

            "bb_lower": indicators["BB"]["lower"].iloc[-1],

            "stoch_k": indicators["STOCH"]["k"].iloc[-1],

            "stoch_d": indicators["STOCH"]["d"].iloc[-1]

        }