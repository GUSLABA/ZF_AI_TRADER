"""
========================================================
ZF AI TRADER
File    : zf_rules.py
Folder  : strategy
Versi   : 0.2.0
Tanggal : 07 Juli 2026

Fungsi:
Kumpulan aturan (Rules) strategi ZF.

Dipanggil oleh:
- zf_strategy.py

Menggunakan:
- config.weights
========================================================
"""

from config.weights import (
    BUY_SCORE,
    SELL_SCORE,
    WAIT_MIN,
    WAIT_MAX,
)


class ZFRules:
    """
    Kumpulan aturan strategi ZF.
    """

    def __init__(self):
        pass

    # ==================================================
    # BUY RULE
    # ==================================================

    def allow_buy(self, score):

        return score >= BUY_SCORE

    # ==================================================
    # SELL RULE
    # ==================================================

    def allow_sell(self, score):

        return score <= SELL_SCORE

    # ==================================================
    # WAIT RULE
    # ==================================================

    def allow_wait(self, score):

        return WAIT_MIN <= score <= WAIT_MAX

    # ==================================================
    # VALIDASI TREND
    # ==================================================

    def valid_trend(self, trend):

        valid_trends = (
            "STRONG_BULLISH",
            "BULLISH",
            "STRONG_BEARISH",
            "BEARISH",
            "SIDEWAYS"
        )

        return trend in valid_trends

    # ==================================================
    # VALIDASI MOMENTUM
    # ==================================================

    def valid_momentum(self, momentum):

        valid_momentum = (
            "BULLISH",
            "BEARISH",
            "OVERBOUGHT",
            "OVERSOLD",
            "NEUTRAL"
        )

        return momentum in valid_momentum

    # ==================================================
    # VALIDASI VOLATILITY
    # ==================================================

    def valid_volatility(self, volatility):

        valid_volatility = (
            "LOW",
            "MEDIUM",
            "HIGH"
        )

        return volatility in valid_volatility

    # ==================================================
    # VALIDASI SIGNAL
    # ==================================================

    def validate_signal(self, signal):

        if "trend" not in signal:
            return False

        if "momentum" not in signal:
            return False

        if "volatility" not in signal:
            return False

        if not self.valid_trend(signal["trend"]):
            return False

        if not self.valid_momentum(signal["momentum"]):
            return False

        if not self.valid_volatility(signal["volatility"]):
            return False

        return True

    # ==================================================
    # KEPUTUSAN
    # ==================================================

    def get_decision(self, score):

        if self.allow_buy(score):
            return "BUY"

        if self.allow_sell(score):
            return "SELL"

        return "WAIT"