"""
========================================================
ZF AI TRADER
File    : zf_strategy.py
Folder  : strategy
Versi   : 0.4.0
Tanggal : 07 Juli 2026

Fungsi:
Menggabungkan seluruh engine strategi ZF
dan menghasilkan keputusan akhir.

Dipanggil oleh:
- zf_master.py

Menggunakan:
- zf_score.py
- zf_rules.py
- zf_filter.py
- zf_validator.py
========================================================
"""

from strategy.zf_score import ZFScore
from strategy.zf_rules import ZFRules
from strategy.zf_filter import ZFFilter
from strategy.zf_validator import ZFValidator


class ZFStrategy:
    """
    Master Strategy ZF AI Trader.
    """

    def __init__(self):

        self.score_engine = ZFScore()
        self.rules = ZFRules()
        self.filter = ZFFilter()
        self.validator = ZFValidator()

    # ==================================================
    # ANALISIS STRATEGI
    # ==================================================

    def analyze(self, signal):

        # ----------------------------------------------
        # Hitung Score
        # ----------------------------------------------

        score_result = self.score_engine.calculate(signal)

        score = score_result["zf_score"]

        # ----------------------------------------------
        # Jalankan Filter
        # ----------------------------------------------

        filter_result = self.filter.apply(signal)

        # ----------------------------------------------
        # Jalankan Validator
        # ----------------------------------------------

        validator_result = self.validator.validate(
            signal,
            score_result,
            filter_result
        )

        # ----------------------------------------------
        # Tentukan Decision
        # ----------------------------------------------

        decision = "WAIT"

        if validator_result["valid"]:

            if self.rules.allow_buy(score):

                decision = "BUY"

            elif self.rules.allow_sell(score):

                decision = "SELL"

            else:

                decision = "WAIT"

        # ----------------------------------------------
        # Hasil Akhir
        # ----------------------------------------------

        result = {

            "decision": decision,

            "zf_score": score,

            "trend_score": score_result["trend_score"],

            "momentum_score": score_result["momentum_score"],

            "volatility_score": score_result["volatility_score"],

            "filter_passed": filter_result["passed"],

            "validator_passed": validator_result["valid"],

            "reason": score_result["reason"],

            "filter_report": filter_result["reason"],

            "validator_report": validator_result["report"]

        }
        #print(
        #   f"Filter={filter_result['passed']} | "
        #   f"Validator={validator_result['valid']} | "
        #   f"Decision={decision}"
        #)
        #print(

        #   f"EMA13={signal['ema13']:.2f} | "
        #   f"EMA20={signal['ema20']:.2f} | "
        #    f"RSI={signal['rsi']:.2f} | "
        #   f"MACD={signal['macd']:.2f}"

        #)
        return result