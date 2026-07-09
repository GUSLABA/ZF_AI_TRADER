"""
========================================================
ZF AI TRADER
File    : report_engine.py
Folder  : core/
Versi   : 0.1.0
Tanggal : 09 Juli 2026

Fungsi:
Menampilkan laporan analisis trading ZF AI TRADER
ke console.

Class:
- ReportEngine

Method:
- print_header()
- print_account()
- print_market()
- print_indicators()
- print_signal()
- print_strategy()
- print_trade_plan()
- print_footer()

Digunakan oleh:
- zf_master.py

Author:
ZF AI TRADER Project
========================================================
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional


class ReportEngine:
    """
    =====================================================
    Report Engine

    Bertugas menampilkan seluruh hasil analisis
    trading dalam format yang rapi dan mudah dibaca.

    ReportEngine TIDAK melakukan:

    - Perhitungan indikator
    - Analisis signal
    - Trading
    - Koneksi MT5

    ReportEngine HANYA menerima data kemudian
    menampilkannya ke console.
    =====================================================
    """

    # =====================================================
    # Constructor
    # =====================================================

    def __init__(self):

        self.width = 56
        self.separator = "=" * self.width
        self.line = "-" * self.width

    # =====================================================
    # Helper Method
    # =====================================================

    def _title(self, text: str) -> None:
        """
        Menampilkan judul section.
        """

        print(f"\n{self.separator}")
        print(text.upper())
        print(self.separator)

    def _line(self) -> None:
        """
        Menampilkan garis pemisah.
        """

        print(self.line)

    def _separator(self) -> None:
        """
        Menampilkan garis utama.
        """

        print(self.separator)

    def _row(
        self,
        label: str,
        value: Any
    ) -> None:
        """
        Menampilkan satu baris data.

        Contoh:
        Trend      : BULLISH
        """

        print(f"{label:<15}: {value}")

    def _empty(self) -> None:
        """
        Menampilkan satu baris kosong.
        """

        print()

    def _center(
        self,
        text: str
    ) -> None:
        """
        Menampilkan teks di tengah.
        """

        print(text.center(self.width))

    def _bool(
        self,
        value: bool
    ) -> str:
        """
        Konversi bool menjadi YES / NO.
        """

        return "YES" if value else "NO"

    def _time_now(self) -> str:
        """
        Mengembalikan waktu lokal.
        """

        return datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        )

    def _safe(
        self,
        value: Optional[Any],
        default: str = "-"
    ) -> Any:
        """
        Menghindari nilai None.
        """

        if value is None:
            return default

        return value

    def _number(
        self,
        value: Optional[float],
        digit: int = 2
    ) -> str:
        """
        Format angka desimal.
        """

        if value is None:
            return "-"

        return f"{value:.{digit}f}"

    def _money(
        self,
        value: Optional[float]
    ) -> str:
        """
        Format angka uang.
        """

        if value is None:
            return "-"

        return f"{value:,.2f}"

    def _section(
        self,
        title: str
    ) -> None:
        """
        Alias untuk title.
        """

        self._title(title)
    # =====================================================
    # Header Report
    # =====================================================

    def print_header(
        self,
        title: str = "MARKET ANALYSIS REPORT"
    ) -> None:
        """
        Menampilkan header laporan.
        """

        print()
        self._separator()
        self._center("ZF AI TRADER")
        self._center(title)
        self._separator()

        self._row("Tanggal", self._time_now())

        self._line()

    # =====================================================
    # Account Information
    # =====================================================

    def print_account(
        self,
        login: Any = "-",
        server: str = "-",
        balance: Optional[float] = None,
        equity: Optional[float] = None,
        leverage: Any = "-",
        company: str = "-"
    ) -> None:
        """
        Menampilkan informasi akun MT5.
        """

        self._section("ACCOUNT INFORMATION")

        self._row("Login", login)
        self._row("Server", server)

        if company != "-":
            self._row("Company", company)

        self._row(
            "Balance",
            self._money(balance)
        )

        self._row(
            "Equity",
            self._money(equity)
        )

        self._row(
            "Leverage",
            leverage
        )

        self._line()

    # =====================================================
    # Market Information
    # =====================================================

    def print_market(
        self,
        symbol: str = "-",
        timeframe: str = "-",
        bid: Optional[float] = None,
        ask: Optional[float] = None,
        spread: Optional[float] = None,
        candle_count: Optional[int] = None
    ) -> None:
        """
        Menampilkan informasi market.
        """

        self._section("MARKET INFORMATION")

        self._row("Symbol", symbol)
        self._row("Timeframe", timeframe)

        self._row(
            "Bid",
            self._number(bid)
        )

        self._row(
            "Ask",
            self._number(ask)
        )

        self._row(
            "Spread",
            self._number(spread)
        )

        self._row(
            "Candles",
            self._safe(candle_count)
        )

        self._line()       
    # =====================================================
    # Indicator Information
    # =====================================================

    def print_indicators(
        self,
        ema13: Optional[float] = None,
        ema20: Optional[float] = None,
        ema50: Optional[float] = None,
        ema200: Optional[float] = None,
        rsi: Optional[float] = None,
        macd: Optional[float] = None,
        atr: Optional[float] = None,
        bb_upper: Optional[float] = None,
        bb_middle: Optional[float] = None,
        bb_lower: Optional[float] = None,
        stoch_k: Optional[float] = None,
        stoch_d: Optional[float] = None
    ) -> None:
        """
        Menampilkan hasil seluruh indikator.
        """

        self._section("INDICATORS")

        self._row("EMA 13", self._number(ema13))
        self._row("EMA 20", self._number(ema20))
        self._row("EMA 50", self._number(ema50))
        self._row("EMA 200", self._number(ema200))

        self._line()

        self._row("RSI", self._number(rsi))
        self._row("MACD", self._number(macd))
        self._row("ATR", self._number(atr))

        self._line()

        self._row("BB Upper", self._number(bb_upper))
        self._row("BB Middle", self._number(bb_middle))
        self._row("BB Lower", self._number(bb_lower))

        self._line()

        self._row("STOCH K", self._number(stoch_k))
        self._row("STOCH D", self._number(stoch_d))

        self._line()

    # =====================================================
    # Signal Information
    # =====================================================

    def print_signal(
        self,
        trend: str = "-",
        momentum: str = "-",
        volatility: str = "-"
    ) -> None:
        """
        Menampilkan hasil Signal Engine.
        """

        self._section("SIGNAL ANALYSIS")

        self._row("Trend", trend)
        self._row("Momentum", momentum)
        self._row("Volatility", volatility)

        self._line()   
    # =====================================================
    # Strategy Information
    # =====================================================

    def print_strategy(
        self,
        decision: str = "-",
        zf_score: int = 0,
        reasons: Optional[list] = None
    ) -> None:
        """
        Menampilkan hasil ZF Strategy.
        """

        self._section("ZF STRATEGY")

        self._row("Decision", decision)
        self._row("ZF Score", zf_score)

        self._line()

        print("Reason :")

        if reasons:

            for reason in reasons:

                print(f"✓ {reason}")

        else:

            print("-")

        self._line()

    # =====================================================
    # Trade Plan
    # =====================================================

    def print_trade_plan(
        self,
        bias: str = "-",
        entry: Optional[float] = None,
        stop_loss: Optional[float] = None,
        take_profit: Optional[float] = None,
        risk_reward: str = "-",
        lot: Optional[float] = None
    ) -> None:
        """
        Menampilkan rencana trading.
        """

        self._section("TRADE PLAN")

        self._row("Bias", bias)
        self._row("Entry", self._number(entry))
        self._row("Stop Loss", self._number(stop_loss))
        self._row("Take Profit", self._number(take_profit))
        self._row("Risk Reward", risk_reward)
        self._row("Lot", self._number(lot))

        self._line()

    # =====================================================
    # Footer
    # =====================================================

    def print_footer(self) -> None:
        """
        Menampilkan footer laporan.
        """

        self._separator()
        self._center("END OF REPORT")
        self._center("ZF AI TRADER")
        self._separator()
        print()              