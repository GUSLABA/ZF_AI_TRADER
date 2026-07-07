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

        return {

            "passed": status,

            "reason": filters

        }