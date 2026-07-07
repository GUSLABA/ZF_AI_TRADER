"""
========================================================
ZF AI TRADER
File    : order_manager.py
Folder  : core
Versi   : 0.2.0
Tanggal : 07 Juli 2026

Fungsi:
Mengelola seluruh proses order sebelum
dikirim ke Trade Executor.

Dipanggil oleh:
- zf_master.py

Menggunakan:
- core.trade_executor
- core.logger
========================================================
"""

from core.trade_executor import TradeExecutor
from core.logger import ZFLogger


class OrderManager:
    """
    Mengelola seluruh proses order.
    """

    def __init__(self):

        self.logger = ZFLogger()
        self.executor = TradeExecutor()

    # ==================================================
    # ENTRY POINT
    # ==================================================

    def process(self, strategy_result):
        """
        Fungsi utama Order Manager.
        """

        self.logger.info("========================================")
        self.logger.info("ORDER MANAGER")
        self.logger.info("========================================")

        # ----------------------------------------------
        # Validasi Decision
        # ----------------------------------------------

        if not self.validate_decision(strategy_result):

            self.logger.warning(
                "Order dibatalkan."
            )

            return False

        # ----------------------------------------------
        # Validasi Posisi
        # ----------------------------------------------

        if not self.check_position():

            self.logger.warning(
                "Masih ada posisi terbuka."
            )

            return False

        # ----------------------------------------------
        # Validasi Session
        # ----------------------------------------------

        if not self.check_session():

            self.logger.warning(
                "Di luar jam trading."
            )

            return False

        # ----------------------------------------------
        # Validasi Trade
        # ----------------------------------------------

        if not self.check_trade():

            self.logger.warning(
                "Trade tidak valid."
            )

            return False

        # ----------------------------------------------
        # Membuat Order
        # ----------------------------------------------

        order = self.create_order(strategy_result)

        self.show_order(order)

        # ----------------------------------------------
        # Eksekusi
        # ----------------------------------------------

        return self.execute_order(order)

    # ==================================================
    # VALIDASI DECISION
    # ==================================================

    def validate_decision(self, strategy_result):

        decision = strategy_result["decision"]

        if decision not in ("BUY", "SELL"):

            self.logger.warning(
                "Decision = WAIT"
            )

            return False

        return True

    # ==================================================
    # POSITION CHECK
    # ==================================================

    def check_position(self):
        """
        Placeholder.
        Nanti dipindah ke PositionManager.
        """

        if self.executor.has_open_position():

            return False

        return True

    # ==================================================
    # SESSION CHECK
    # ==================================================

    def check_session(self):
        """
        Placeholder.
        Nanti dipindah ke SessionManager.
        """

        return True

    # ==================================================
    # TRADE VALIDATOR
    # ==================================================

    def check_trade(self):
        """
        Placeholder.
        Nanti dipindah ke TradeValidator.
        """

        return True

    # ==================================================
    # CREATE ORDER
    # ==================================================

    def create_order(self, strategy_result):

        order = {

            "decision": strategy_result["decision"],

            "symbol": self.executor.symbol,

            "lot": 0.01,

            "entry": 0.0,

            "stop_loss": 0.0,

            "take_profit": 0.0,

            "comment": "ZF_AI_TRADER",

            "magic": 10001

        }

        return order

    # ==================================================
    # SHOW ORDER
    # ==================================================

    def show_order(self, order):

        self.logger.info("----------------------------------------")
        self.logger.info("ORDER DETAIL")
        self.logger.info("----------------------------------------")

        self.logger.info(
            f"Decision : {order['decision']}"
        )

        self.logger.info(
            f"Symbol   : {order['symbol']}"
        )

        self.logger.info(
            f"Lot      : {order['lot']}"
        )

        self.logger.info(
            f"Entry    : {order['entry']}"
        )

        self.logger.info(
            f"SL       : {order['stop_loss']}"
        )

        self.logger.info(
            f"TP       : {order['take_profit']}"
        )

        self.logger.info(
            f"Magic    : {order['magic']}"
        )

        self.logger.info(
            f"Comment  : {order['comment']}"
        )

        self.logger.info("----------------------------------------")

    # ==================================================
    # EXECUTE ORDER
    # ==================================================

    def execute_order(self, order):

        decision = order["decision"]

        if decision == "BUY":

            return self.executor.execute_buy(

                lot=order["lot"],

                sl=order["stop_loss"],

                tp=order["take_profit"]

            )

        elif decision == "SELL":

            return self.executor.execute_sell(

                lot=order["lot"],

                sl=order["stop_loss"],

                tp=order["take_profit"]

            )

        return False