"""
========================================================
ZF AI TRADER
File    : mt5_connector.py
Folder  : core
Versi   : 0.1.0

Fungsi:
Menghubungkan Python ke MetaTrader 5.

Dipanggil oleh:
- zf_master.py

Menggunakan:
- config.account
========================================================
"""

import MetaTrader5 as mt5

from config.account import (
    MT5_LOGIN,
    MT5_PASSWORD,
    MT5_SERVER,
    MT5_PATH,
)


class MT5Connector:
    """
    Class untuk menghubungkan Python ke MetaTrader 5.
    """

    def __init__(self):
        self.connected = False

    def connect(self):
        """
        Login ke MetaTrader 5.
        """

        print("=" * 50)
        print("ZF AI TRADER")
        print("Menghubungkan ke MetaTrader 5...")
        print("=" * 50)

        # Jalankan terminal MT5
        if not mt5.initialize(path=MT5_PATH):
            print("❌ Gagal membuka MetaTrader 5")
            print(mt5.last_error())
            return False

        # Login akun
        authorized = mt5.login(
            login=MT5_LOGIN,
            password=MT5_PASSWORD,
            server=MT5_SERVER
        )

        if not authorized:
            print("❌ Login gagal")
            print(mt5.last_error())
            mt5.shutdown()
            return False

        self.connected = True

        account = mt5.account_info()

        print("✅ MT5 Connected")
        print(f"Login   : {account.login}")
        print(f"Server  : {account.server}")
        print(f"Balance : {account.balance}")
        print(f"Equity  : {account.equity}")
        print(f"Leverage: 1:{account.leverage}")

        print("=" * 50)

        return True

    def disconnect(self):
        """
        Putus koneksi MT5.
        """

        mt5.shutdown()

        self.connected = False

        print("MT5 Disconnect")

    def is_connected(self):
        """
        Mengecek status koneksi.
        """

        return self.connected

    def get_account_info(self):
        """
        Mengambil informasi akun.
        """

        if not self.connected:
            return None

        return mt5.account_info()