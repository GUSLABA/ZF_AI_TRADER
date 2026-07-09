"""
========================================================
ZF AI TRADER
File    : zf_score.py
Folder  : strategy
Versi   : 0.2.0
Tanggal : 07 Juli 2026

Fungsi:
Menghitung ZF Score berdasarkan hasil
Signal Engine menggunakan bobot dari
config/weights.py

Dipanggil oleh:
- zf_strategy.py
========================================================
"""

from config.weights import (
    # Trend
    TREND_STRONG_BULLISH,
    TREND_BULLISH,
    TREND_STRONG_BEARISH,
    TREND_BEARISH,
    TREND_SIDEWAYS,

    # Momentum
    MOMENTUM_BULLISH,
    MOMENTUM_BEARISH,
    MOMENTUM_OVERBOUGHT,
    MOMENTUM_OVERSOLD,
    MOMENTUM_NEUTRAL,

    # Volatility
    VOLATILITY_HIGH,
    VOLATILITY_MEDIUM,
    VOLATILITY_LOW,
)


class ZFScore:
    """
    Mesin perhitungan ZF Score.
    """

    def __init__(self):
        pass

    # ==================================================
    # HITUNG SCORE
    # ==================================================

    def calculate(self, signal):

        trend = signal["trend"]
        # ==========================================
        # LEVEL 1 : TREND ENGINE
        # ==========================================

        trend_score = 0

        if trend == "STRONG_BULLISH":

            trend_score += 40

        elif trend == "BULLISH":

            trend_score += 25

        elif trend == "STRONG_BEARISH":

            trend_score -= 40

        elif trend == "BEARISH":

            trend_score -= 25

        else:

            trend_score += 0
        momentum = signal["momentum"]
        volatility = signal["volatility"]
        # ==================================================
        # LEVEL 1 DATA
        # ==================================================

        ema13 = signal["ema13"]
        ema20 = signal["ema20"]
        ema50 = signal["ema50"]
        ema200 = signal["ema200"]           

        trend_score = 0
        momentum_score = 0
        volatility_score = 0

        reason = []

        # ==================================================
        # LEVEL 1 : EMA TREND SCORE
        # ==================================================

        if ema13 > ema20 > ema50 > ema200:

            trend_score = 40

            reason.append(

                f"EMA13 > EMA20 > EMA50 > EMA200 "

                f"({trend_score:+d})"

            )

        elif ema13 > ema20 > ema50:

            trend_score = 30

            reason.append(

                f"EMA13 > EMA20 > EMA50 "

                f"({trend_score:+d})"

            )

        elif ema13 > ema20:

            trend_score = 20

            reason.append(

                f"EMA13 > EMA20 "

                f"({trend_score:+d})"

            )

        elif ema13 < ema20 < ema50 < ema200:

            trend_score = -40

            reason.append(

                f"EMA13 < EMA20 < EMA50 < EMA200 "

                f"({trend_score:+d})"

            )

        elif ema13 < ema20 < ema50:

            trend_score = -30

            reason.append(

                f"EMA13 < EMA20 < EMA50 "

                f"({trend_score:+d})"

             )

        elif ema13 < ema20:

            trend_score = -20

            reason.append(

                f"EMA13 < EMA20 "

                f"({trend_score:+d})"

            )

        else:

            trend_score = 0

            reason.append(

                f"EMA Sideways ({trend_score:+d})"

            )

        # ==================================================
        # MOMENTUM
        # ==================================================

        if momentum == "BULLISH":

            momentum_score = MOMENTUM_BULLISH
            reason.append(
                f"Momentum Bullish ({momentum_score:+d})"
            )

        elif momentum == "BEARISH":

            momentum_score = MOMENTUM_BEARISH
            reason.append(
                f"Momentum Bearish ({momentum_score:+d})"
            )

        elif momentum == "OVERBOUGHT":

            momentum_score = MOMENTUM_OVERBOUGHT
            reason.append(
                f"Momentum Overbought ({momentum_score:+d})"
            )

        elif momentum == "OVERSOLD":

            momentum_score = MOMENTUM_OVERSOLD
            reason.append(
                f"Momentum Oversold ({momentum_score:+d})"
            )

        else:

            momentum_score = MOMENTUM_NEUTRAL
            reason.append(
                f"Momentum Neutral ({momentum_score:+d})"
            )

        # ==================================================
        # VOLATILITY
        # ==================================================

        if volatility == "HIGH":

            volatility_score = VOLATILITY_HIGH
            reason.append(
                f"Volatility High ({volatility_score:+d})"
            )

        elif volatility == "MEDIUM":

            volatility_score = VOLATILITY_MEDIUM
            reason.append(
                f"Volatility Medium ({volatility_score:+d})"
            )

        else:

            volatility_score = VOLATILITY_LOW
            reason.append(
                f"Volatility Low ({volatility_score:+d})"
            )

        # ==================================================
        # TOTAL SCORE
        # ==================================================

        total_score = (
            trend_score +
            momentum_score +
            volatility_score
        )

        # ==================================================
        # HASIL
        # ==================================================

        result = {

            "zf_score": total_score,

            "trend_score": trend_score,

            "momentum_score": momentum_score,

            "volatility_score": volatility_score,

            "reason": reason

        }

        return result