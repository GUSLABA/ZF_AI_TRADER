"""
========================================================
ZF AI TRADER
File    : backtest_engine.py
Folder  : core
Versi   : 0.1.0
Tanggal : 09 Juli 2026

Fungsi:
Melakukan simulasi backtest menggunakan
data historis MetaTrader 5.

Dipanggil oleh:
- zf_master.py
- main.py (versi berikutnya)

Menggunakan:
- core.mt5_connector
- core.data_loader
- core.indicator_engine
- core.signal_engine
- strategy.zf_strategy
========================================================
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List

import MetaTrader5 as mt5
import pandas as pd

from core.mt5_connector import MT5Connector
from core.data_loader import DataLoader
from core.indicator_engine import IndicatorEngine
from core.signal_engine import SignalEngine
from core.logger import ZFLogger

from strategy.zf_strategy import ZFStrategy


class BacktestEngine:
    """
    Engine simulasi backtest ZF AI Trader.
    """

    # ==================================================
    # CONSTRUCTOR
    # ==================================================

    def __init__(
        self,
        mt5_connector: Optional[MT5Connector] = None,
        data_loader: Optional[DataLoader] = None,
        indicator_engine: Optional[IndicatorEngine] = None,
        signal_engine: Optional[SignalEngine] = None,
        strategy_engine: Optional[ZFStrategy] = None,
        logger: Optional[ZFLogger] = None
    ):

        self.mt5 = mt5_connector or MT5Connector()
        self.loader = data_loader or DataLoader()
        self.indicator = indicator_engine or IndicatorEngine()
        self.signal = signal_engine or SignalEngine()
        self.strategy = strategy_engine or ZFStrategy()
        self.logger = logger or ZFLogger()

        self._initialize_config()

    # ==================================================
    # CONFIG
    # ==================================================

    def _initialize_config(self):

        self.symbol = "XAUUSD"

        self.timeframe = mt5.TIMEFRAME_M5

        self.candle_limit = 500

        self.history_years = 2

        self.initial_balance = 10000.0

        self.default_lot = 0.01

        self.default_sl = 300

        self.default_tp = 600

        self.spread = 0.0

        self.slippage = 0

        self.enable_log = True

        self.enable_report = True

        self.start_date = datetime.now() - timedelta(
            days=365 * self.history_years
        )

        self.end_date = datetime.now()

        self.results: List[Dict[str, Any]] = []

        self.statistics: Dict[str, Any] = {}

    # ==================================================
    # SET CONFIG
    # ==================================================

    def set_symbol(self, symbol: str):

        self.symbol = symbol

    def set_timeframe(self, timeframe: int):

        self.timeframe = timeframe

    def set_period(
        self,
        start_date: datetime,
        end_date: datetime
    ):

        self.start_date = start_date
        self.end_date = end_date

    def set_lot(self, lot: float):

        self.default_lot = lot

    def set_stop_loss(self, points: float):

        self.default_sl = points

    def set_take_profit(self, points: float):

        self.default_tp = points

    def set_initial_balance(self, balance: float):

        self.initial_balance = balance

    # ==================================================
    # HELPER
    # ==================================================

    def log(self, message: str):

        if self.enable_log:

            self.logger.info(message)

    def reset(self):

        self.results.clear()

        self.statistics.clear()

    def get_config(self) -> Dict[str, Any]:

        return {

            "symbol": self.symbol,

            "timeframe": self.timeframe,

            "history_years": self.history_years,

            "start_date": self.start_date,

            "end_date": self.end_date,

            "initial_balance": self.initial_balance,

            "lot": self.default_lot,

            "stop_loss": self.default_sl,

            "take_profit": self.default_tp,

            "spread": self.spread,

            "slippage": self.slippage,

            "candle_limit": self.candle_limit

        }

    def print_config(self):

        print("\n========================================================")
        print("BACKTEST CONFIGURATION")
        print("========================================================")
        print(f"Symbol           : {self.symbol}")
        print(f"Timeframe        : {self.timeframe}")
        print(f"History          : {self.history_years} Year(s)")
        print(f"Start Date       : {self.start_date}")
        print(f"End Date         : {self.end_date}")
        print(f"Initial Balance  : {self.initial_balance:,.2f}")
        print(f"Lot              : {self.default_lot}")
        print(f"Stop Loss        : {self.default_sl}")
        print(f"Take Profit      : {self.default_tp}")
        print(f"Spread           : {self.spread}")
        print(f"Slippage         : {self.slippage}")
        print(f"Candle Limit     : {self.candle_limit}")
        print("========================================================")
    # ==================================================
    # LOAD HISTORICAL DATA
    # ==================================================

    def load_history(self) -> pd.DataFrame:
        """
        Mengambil data historis dari MT5.
        """

        self.log("Mengambil data historis...")

        if not mt5.initialize():

            raise RuntimeError(
                "MT5 belum terhubung."
            )
        print("Symbol    :", self.symbol)
        print("Timeframe :", self.timeframe)
        print("Start     :", self.start_date)
        print("End       :", self.end_date)
        rates = mt5.copy_rates_from(
            self.symbol,
            self.timeframe,
            self.end_date,
            1000
        )

        print("MT5 Last Error :", mt5.last_error())
        print("Rates          :", rates)

        if rates is None:

            raise RuntimeError(
                f"Gagal mengambil data historis {self.symbol}"
            )

        if len(rates) == 0:

            raise RuntimeError(
                "Data historis kosong."
            )

        df = pd.DataFrame(rates)

        df["time"] = pd.to_datetime(
            df["time"],
            unit="s"
        )

        df.rename(
            columns={
                "tick_volume": "volume"
            },
            inplace=True
        )

        self.log(
            f"Berhasil mengambil {len(df):,} candle."
        )

        return df

    # ==================================================
    # DATE RANGE
    # ==================================================

    def get_date_range(self) -> Dict[str, datetime]:

        return {

            "start": self.start_date,

            "end": self.end_date,

            "days": (
                self.end_date -
                self.start_date
            ).days

        }

    # ==================================================
    # MT5 HISTORY INFORMATION
    # ==================================================

    def print_history_info(
        self,
        df: pd.DataFrame
    ):

        print("\n========================================================")
        print("HISTORICAL DATA")
        print("========================================================")
        print(f"Symbol         : {self.symbol}")
        print(f"Timeframe      : {self.timeframe}")
        print(f"Start          : {df.iloc[0]['time']}")
        print(f"End            : {df.iloc[-1]['time']}")
        print(f"Total Candle   : {len(df):,}")
        print("========================================================")

    # ==================================================
    # VALIDATION
    # ==================================================

    def validate_history(
        self,
        df: pd.DataFrame
    ) -> bool:

        required_columns = (

            "time",

            "open",

            "high",

            "low",

            "close",

            "volume"

        )

        for column in required_columns:

            if column not in df.columns:

                raise ValueError(
                    f"Kolom '{column}' tidak ditemukan."
                )

        if len(df) < 300:

            raise ValueError(
                "Jumlah candle terlalu sedikit untuk backtest."
            )

        if df.isnull().values.any():

            raise ValueError(
                "Data historis mengandung nilai NULL."
            )

        self.log(
            "Validasi data historis berhasil."
        )

        return True
    # ==================================================
    # SIMULATION ENGINE
    # ==================================================

    def run_simulation(self):

        self.log("Memulai simulasi backtest...")

        self.reset()

        df = self.load_history()

        self.validate_history(df)

        self.print_history_info(df)

        total_candle = len(df)

        self.log(
            f"Total candle : {total_candle:,}"
        )

        self.simulate(df)

        self.log("Simulasi selesai.")

        return self.results

    # ==================================================
    # LOOP CANDLE
    # ==================================================

    def simulate(
        self,
        df: pd.DataFrame
    ):

        start_index = max(
            200,
            self.candle_limit
        )

        for index in range(
            start_index,
            len(df)
        ):

            history = df.iloc[
                index - self.candle_limit:index
            ].copy()

            current = df.iloc[index]

            self.process_candle(
                history,
                current,
                index
            )

       # ==================================================
    # PROCESS CANDLE
    # ==================================================

    def process_candle(
        self,
        history: pd.DataFrame,
        current: pd.Series,
        index: int,
        df: pd.DataFrame
    ):

        indikator = self.calculate_indicator(
            history
        )

        signal = self.generate_signal(
            indikator
        )

        strategy = self.generate_strategy(
            signal
        )

        trade = {

            "index": index,

            "time": current["time"],

            "open": current["open"],

            "high": current["high"],

            "low": current["low"],

            "close": current["close"],

            "signal": signal,

            "strategy": strategy

        }

        result = self.simulate_trade(
            trade,
            df
        )

        if result is not None:

            trade.update(result)

            trade["result"] = result["result"]

        else:

            trade["result"] = "WAIT"

        self.results.append(trade)

    # ==================================================
    # INDICATOR
    # ==================================================

    def calculate_indicator(
        self,
        history: pd.DataFrame
    ) -> dict:

        indikator = self.indicator.calculate_all(
            history
        )

        return indikator

    # ==================================================
    # SIGNAL
    # ==================================================

    def generate_signal(
        self,
        indikator: dict
    ) -> dict:

        signal = self.signal.analyze(
            indikator
        )

        return signal

    # ==================================================
    # STRATEGY
    # ==================================================

    def generate_strategy(
        self,
        signal: dict
    ) -> dict:

        strategy = self.strategy.analyze(
            signal
        )

        return strategy   
    # ==================================================
    # ENTRY SIMULATOR
    # ==================================================

    def simulate_trade(
        self,
        trade: dict,
        df: pd.DataFrame
    ):

        decision = trade["strategy"]["decision"]

        if decision == "BUY":

            return self.simulate_buy(
                trade,
                df
            )

        elif decision == "SELL":

            return self.simulate_sell(
                trade,
                df
            )

        return None

    # ==================================================
    # BUY
    # ==================================================

    def simulate_buy(
        self,
        trade: dict,
        df: pd.DataFrame
    ):

        entry = trade["close"]

        sl = entry - (
            self.default_sl * mt5.symbol_info(
                self.symbol
            ).point
        )

        tp = entry + (
            self.default_tp * mt5.symbol_info(
                self.symbol
            ).point
        )

        return self.check_exit(
            trade,
            df,
            "BUY",
            entry,
            sl,
            tp
        )

    # ==================================================
    # SELL
    # ==================================================

    def simulate_sell(
        self,
        trade: dict,
        df: pd.DataFrame
    ):

        entry = trade["close"]

        sl = entry + (
            self.default_sl * mt5.symbol_info(
                self.symbol
            ).point
        )

        tp = entry - (
            self.default_tp * mt5.symbol_info(
                self.symbol
            ).point
        )

        return self.check_exit(
            trade,
            df,
            "SELL",
            entry,
            sl,
            tp
        )

    # ==================================================
    # TP / SL
    # ==================================================

    def check_exit(
        self,
        trade: dict,
        df: pd.DataFrame,
        side: str,
        entry: float,
        sl: float,
        tp: float
    ):

        start = trade["index"] + 1

        for i in range(
            start,
            len(df)
        ):

            candle = df.iloc[i]

            high = candle["high"]

            low = candle["low"]

            if side == "BUY":

                if low <= sl:

                    return self.close_trade(
                        trade,
                        "LOSS",
                        entry,
                        sl,
                        candle["time"],
                        i
                    )

                if high >= tp:

                    return self.close_trade(
                        trade,
                        "WIN",
                        entry,
                        tp,
                        candle["time"],
                        i
                    )

            else:

                if high >= sl:

                    return self.close_trade(
                        trade,
                        "LOSS",
                        entry,
                        sl,
                        candle["time"],
                        i
                    )

                if low <= tp:

                    return self.close_trade(
                        trade,
                        "WIN",
                        entry,
                        tp,
                        candle["time"],
                        i
                    )

        return self.close_trade(
            trade,
            "OPEN",
            entry,
            trade["close"],
            df.iloc[-1]["time"],
            len(df) - 1
        )

    # ==================================================
    # CLOSE TRADE
    # ==================================================

    def close_trade(
        self,
        trade: dict,
        result: str,
        entry: float,
        exit_price: float,
        exit_time,
        exit_index: int
    ):

        return {

            "time_in": trade["time"],

            "time_out": exit_time,

            "index_in": trade["index"],

            "index_out": exit_index,

            "symbol": self.symbol,

            "side": trade["strategy"]["decision"],

            "entry": entry,

            "exit": exit_price,

            "stop_loss": (
                entry - self.default_sl * mt5.symbol_info(self.symbol).point
                if trade["strategy"]["decision"] == "BUY"
                else entry + self.default_sl * mt5.symbol_info(self.symbol).point
            ),

            "take_profit": (
                entry + self.default_tp * mt5.symbol_info(self.symbol).point
                if trade["strategy"]["decision"] == "BUY"
                else entry - self.default_tp * mt5.symbol_info(self.symbol).point
            ),

            "lot": self.default_lot,

            "result": result

        }
    # ==================================================
    # STATISTICS ENGINE
    # ==================================================

    def calculate_statistics(self):

        self.log("Menghitung statistik backtest...")

        total_buy = 0
        total_sell = 0
        total_wait = 0

        total_win = 0
        total_loss = 0

        gross_profit = 0.0
        gross_loss = 0.0

        net_profit = 0.0

        balance = self.initial_balance
        peak_balance = balance
        max_drawdown = 0.0

        total_trade = len(self.results)

        for trade in self.results:

            decision = trade["strategy"]["decision"]

            if decision == "BUY":
                total_buy += 1

            elif decision == "SELL":
                total_sell += 1

            else:
                total_wait += 1

            if "result" not in trade:
                continue

            result = trade["result"]

            if result == "WIN":

                total_win += 1

                profit = self.default_tp

                gross_profit += profit

                net_profit += profit

                balance += profit

            elif result == "LOSS":

                total_loss += 1

                loss = self.default_sl

                gross_loss += loss

                net_profit -= loss

                balance -= loss

            if balance > peak_balance:

                peak_balance = balance

            drawdown = peak_balance - balance

            if drawdown > max_drawdown:

                max_drawdown = drawdown

        executed_trade = total_win + total_loss

        if executed_trade > 0:

            win_rate = (
                total_win /
                executed_trade
            ) * 100

        else:

            win_rate = 0.0

        if gross_loss > 0:

            profit_factor = (
                gross_profit /
                gross_loss
            )

        else:

            profit_factor = 0.0

        if peak_balance > 0:

            drawdown_percent = (
                max_drawdown /
                peak_balance
            ) * 100

        else:

            drawdown_percent = 0.0

        self.statistics = {

            "total_trade": total_trade,

            "buy": total_buy,

            "sell": total_sell,

            "wait": total_wait,

            "executed_trade": executed_trade,

            "win": total_win,

            "loss": total_loss,

            "win_rate": win_rate,

            "gross_profit": gross_profit,

            "gross_loss": gross_loss,

            "net_profit": net_profit,

            "balance": balance,

            "max_drawdown": max_drawdown,

            "drawdown_percent": drawdown_percent,

            "profit_factor": profit_factor

        }

        return self.statistics

    # ==================================================
    # GET STATISTICS
    # ==================================================

    def get_statistics(self):

        return self.statistics

    # ==================================================
    # RESET STATISTICS
    # ==================================================

    def reset_statistics(self):

        self.statistics = {}

    # ==================================================
    # PRINT STATISTICS
    # ==================================================

    def print_statistics(self):

        if not self.statistics:

            print("\nBelum ada hasil statistik.")

            return

        s = self.statistics

        print("\n========================================================")
        print("BACKTEST STATISTICS")
        print("========================================================")
        print(f"Total Trade     : {s['total_trade']}")
        print(f"BUY             : {s['buy']}")
        print(f"SELL            : {s['sell']}")
        print(f"WAIT            : {s['wait']}")
        print("--------------------------------------------------------")
        print(f"Executed Trade  : {s['executed_trade']}")
        print(f"WIN             : {s['win']}")
        print(f"LOSS            : {s['loss']}")
        print(f"Win Rate        : {s['win_rate']:.2f}%")
        print("--------------------------------------------------------")
        print(f"Gross Profit    : {s['gross_profit']:.2f}")
        print(f"Gross Loss      : {s['gross_loss']:.2f}")
        print(f"Net Profit      : {s['net_profit']:.2f}")
        print("--------------------------------------------------------")
        print(f"Balance         : {s['balance']:.2f}")
        print(f"Max Drawdown    : {s['max_drawdown']:.2f}")
        print(f"Drawdown (%)    : {s['drawdown_percent']:.2f}%")
        print(f"Profit Factor   : {s['profit_factor']:.2f}")
        print("========================================================")
    # ==================================================
    # REPORT
    # ==================================================

    def generate_report(self):

        if not self.statistics:

            self.calculate_statistics()

        self.print_report()

    # ==================================================
    # CONSOLE REPORT
    # ==================================================

    def print_report(self):

        s = self.statistics

        print("\n========================================================")
        print("                 ZF AI BACKTEST REPORT")
        print("========================================================")

        print(f"Symbol           : {self.symbol}")
        print(f"Timeframe        : {self.timeframe}")
        print(f"Start Date       : {self.start_date}")
        print(f"End Date         : {self.end_date}")

        print("--------------------------------------------------------")

        print(f"Initial Balance  : {self.initial_balance:,.2f}")
        print(f"Final Balance    : {s['balance']:,.2f}")

        print("--------------------------------------------------------")

        print(f"Total Trade      : {s['total_trade']}")
        print(f"BUY              : {s['buy']}")
        print(f"SELL             : {s['sell']}")
        print(f"WAIT             : {s['wait']}")

        print("--------------------------------------------------------")

        print(f"Executed Trade   : {s['executed_trade']}")
        print(f"WIN              : {s['win']}")
        print(f"LOSS             : {s['loss']}")
        print(f"Win Rate         : {s['win_rate']:.2f}%")

        print("--------------------------------------------------------")

        print(f"Gross Profit     : {s['gross_profit']:,.2f}")
        print(f"Gross Loss       : {s['gross_loss']:,.2f}")
        print(f"Net Profit       : {s['net_profit']:,.2f}")

        print("--------------------------------------------------------")

        print(f"Profit Factor    : {s['profit_factor']:.2f}")
        print(f"Max Drawdown     : {s['drawdown_percent']:.2f}%")

        self.print_summary()

        self.print_footer()

    # ==================================================
    # SUMMARY
    # ==================================================

    def print_summary(self):

        s = self.statistics

        print("--------------------------------------------------------")
        print("SUMMARY")
        print("--------------------------------------------------------")

        if s["net_profit"] > 0:

            print("Status           : PROFIT")

        elif s["net_profit"] < 0:

            print("Status           : LOSS")

        else:

            print("Status           : BREAKEVEN")

        if s["win_rate"] >= 70:

            quality = "EXCELLENT"

        elif s["win_rate"] >= 60:

            quality = "GOOD"

        elif s["win_rate"] >= 50:

            quality = "AVERAGE"

        else:

            quality = "NEEDS IMPROVEMENT"

        print(f"Strategy Quality : {quality}")

        print(f"Ending Balance   : {s['balance']:,.2f}")

        print("--------------------------------------------------------")

    # ==================================================
    # FOOTER
    # ==================================================

    def print_footer(self):

        print("========================================================")
        print("             END OF BACKTEST REPORT")
        print("                  ZF AI TRADER")
        print("========================================================\n")
        # ==================================================
    # FULL BACKTEST ENGINE
    # ==================================================

        # ==================================================
    # RUN BACKTEST
    # ==================================================

    def run(self):

        self.log("===== BACKTEST START =====")

        self.reset()

        # ----------------------------------------------
        # Load Historical Data
        # ----------------------------------------------

        df = self.load_history()

        self.validate_history(df)

        self.print_history_info(df)

        # ----------------------------------------------
        # Simulation Loop
        # ----------------------------------------------

        self.log("Memulai simulasi candle...")

        total = len(df)

        start = max(
            self.candle_limit,
            200
        )

        for index in range(start, total):

            history = df.iloc[
                index - self.candle_limit:index
            ].copy()

            current = df.iloc[index]

            indikator = self.calculate_indicator(
                history
            )

            signal = self.generate_signal(
                indikator
            )

            strategy = self.generate_strategy(
                signal
            )

            self.results.append({

                "index": index,

                "time": current["time"],

                "open": current["open"],

                "high": current["high"],

                "low": current["low"],

                "close": current["close"],

                "signal": signal,

                "strategy": strategy

            })

            if index % 1000 == 0:

                self.log(
                    f"Progress : {index:,}/{total:,}"
                )

        self.calculate_statistics()

        self.print_statistics()
        self.log(
            f"Simulation selesai ({len(self.results):,} candle dianalisis)."
        )

        return self.results

    # ==================================================
    # QUICK TEST
    # ==================================================

    def quick_test(self):

        stats = self.run()

        return stats     