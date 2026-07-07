"""
Daftar simbol trading
"""

# Symbol utama
SYMBOL = "XAUUSD"

# Timeframe yang digunakan
TIMEFRAMES = [
    "M5",
    "M15",
    "H1"
]

# Jumlah candle yang diambil
CANDLE_COUNT = {
    "M5": 500,
    "M15": 500,
    "H1": 500
}

# Spread maksimal (point)
MAX_SPREAD = 30