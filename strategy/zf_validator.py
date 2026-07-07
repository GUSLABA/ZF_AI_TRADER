"""
========================================================
ZF AI TRADER
File    : zf_validator.py
Folder  : strategy
Versi   : 0.1.0
Tanggal : 07 Juli 2026

Fungsi:
Melakukan validasi terakhir sebelum
robot membuka posisi trading.

Dipanggil oleh:
- zf_strategy.py
========================================================
"""


class ZFValidator:
    """
    Validator terakhir sebelum entry.
    """

    def __init__(self):
        pass

    # ==================================================
    # VALIDASI SCORE
    # ==================================================

    def validate_score(self, score):

        if score >= 40:
            return True, "ZF Score valid untuk BUY"

        if score <= -40:
            return True, "ZF Score valid untuk SELL"

        return False, "ZF Score belum memenuhi syarat"

    # ==================================================
    # VALIDASI FILTER
    # ==================================================

    def validate_filter(self, filter_result):

        if filter_result["passed"]:
            return True, "Semua filter lolos"

        return False, "Masih ada filter yang gagal"

    # ==================================================
    # VALIDASI SIGNAL
    # ==================================================

    def validate_signal(self, signal):

        required = (
            "trend",
            "momentum",
            "volatility"
        )

        for item in required:

            if item not in signal:

                return False, f"{item} tidak ditemukan"

        return True, "Signal valid"

    # ==================================================
    # VALIDASI DATA SCORE
    # ==================================================

    def validate_score_result(self, score_result):

        if "zf_score" not in score_result:
            return False, "ZF Score tidak ditemukan"

        return True, "ZF Score valid"

    # ==================================================
    # VALIDASI AKHIR
    # ==================================================

    def validate(
        self,
        signal,
        score_result,
        filter_result
    ):

        report = []

        valid = True

        ok, msg = self.validate_signal(signal)
        report.append(msg)

        if not ok:
            valid = False

        ok, msg = self.validate_score_result(score_result)
        report.append(msg)

        if not ok:
            valid = False

        ok, msg = self.validate_filter(filter_result)
        report.append(msg)

        if not ok:
            valid = False

        ok, msg = self.validate_score(
            score_result["zf_score"]
        )

        report.append(msg)

        if not ok:
            valid = False

        return {

            "valid": valid,

            "report": report

        }