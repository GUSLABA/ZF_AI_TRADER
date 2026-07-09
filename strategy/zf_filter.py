"""
========================================================
ZF AI TRADER
File    : zf_filter.py
Folder  : strategy
Versi   : 0.1.0
Tanggal : 07 Juli 2026

Fungsi:
Melakukan filter sebelum robot
mengambil keputusan trading.

Dipanggil oleh:
- zf_strategy.py
========================================================
"""


class ZFFilter:
    """
    Filter kondisi market.
    """

    def __init__(self):
        pass

    # ==================================================
    # FILTER VOLATILITY
    # ==================================================

    def filter_volatility(self, signal):

        volatility = signal["volatility"]

        if volatility == "LOW":

            return False, "Volatility terlalu rendah"

        return True, "Volatility OK"
    # ==================================================
    # FILTER ATR
    # ==================================================

    def filter_atr(self, signal):

        atr = signal["atr"]

        if atr < 5:

            return False, "ATR terlalu kecil"

        return True, "ATR OK"

    # ==================================================
    # FILTER STOCHASTIC
    # ==================================================

    def filter_stochastic(self, signal):

        stoch_k = signal["stoch_k"]

        trend = signal["trend"]

        if trend in ("BULLISH", "STRONG_BULLISH"):

            if stoch_k > 85:

                return False, "Stochastic terlalu tinggi"

        if trend in ("BEARISH", "STRONG_BEARISH"):

            if stoch_k < 15:

                return False, "Stochastic terlalu rendah"

        return True, "Stochastic OK"
    # ==================================================
    # FILTER MOMENTUM
    # ==================================================

    def filter_momentum(self, signal):

        momentum = signal["momentum"]

        if momentum == "NEUTRAL":

            return False, "Momentum belum jelas"

        return True, "Momentum OK"

    # ==================================================
    # FILTER TREND
    # ==================================================

    def filter_trend(self, signal):

        trend = signal["trend"]

        if trend == "SIDEWAYS":

            return False, "Market Sideways"

        return True, "Trend OK"

    # ==================================================
    # FILTER UTAMA
    # ==================================================

    def apply(self, signal):

        filters = []

        status = True

        ok, reason = self.filter_trend(signal)

        filters.append(reason)

        if not ok:
            status = False

        ok, reason = self.filter_momentum(signal)

        filters.append(reason)

        if not ok:
            status = False

        ok, reason = self.filter_volatility(signal)
        
        filters.append(reason)

        if not ok:
            status = False
        ok, reason = self.filter_atr(signal)

        filters.append(reason)

        if not ok:
            status = False
        ok, reason = self.filter_stochastic(signal)

        filters.append(reason)
        if not ok:
            status = False
        return {

            "passed": status,

            "reason": filters

        }