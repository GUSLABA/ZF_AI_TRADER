from core.mt5_connector import MT5Connector
from core.backtest_engine import BacktestEngine

mt5 = MT5Connector()

if mt5.connect():

    engine = BacktestEngine(
        mt5_connector=mt5
    )

    engine.run()

    mt5.disconnect()